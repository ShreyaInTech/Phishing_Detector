import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tld import get_tld
import whois
from datetime import datetime
import numpy as np

class URLFeatureExtractor:
    def __init__(self):
        self.features = {}
    
    def extract_features(self, url):
        """Extract features from URL for phishing detection"""
        self.features = {}
        try:
            self._extract_url_features(url)
            self._extract_domain_features(url)
            self._extract_content_features(url)
        except Exception as e:
            print(f"Error extracting features: {str(e)}")
            # Set default values if extraction fails
            self._set_default_features()
        
        return self._get_feature_vector()
    
    def _extract_url_features(self, url):
        """Extract features from URL string"""
        self.features['url_length'] = len(url)
        self.features['num_digits'] = sum(c.isdigit() for c in url)
        self.features['num_special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
        self.features['has_ip_address'] = 1 if re.search(
            r'(?:\d{1,3}\.){3}\d{1,3}', url
        ) else 0
        self.features['has_at_symbol'] = 1 if '@' in url else 0
        self.features['has_double_slash'] = 1 if '//' in url[7:] else 0
    
    def _extract_domain_features(self, url):
        """Extract domain-based features"""
        try:
            domain = get_tld(url, as_object=True)
            self.features['domain_length'] = len(domain.domain)
            self.features['is_subdomain'] = 1 if domain.subdomain else 0
            
            # WHOIS features
            try:
                whois_info = whois.whois(domain.fld)
                if whois_info.creation_date:
                    creation_date = whois_info.creation_date
                    if isinstance(creation_date, list):
                        creation_date = creation_date[0]
                    domain_age = (datetime.now() - creation_date).days
                    self.features['domain_age'] = domain_age
                else:
                    self.features['domain_age'] = -1
            except:
                self.features['domain_age'] = -1
                
        except:
            self.features['domain_length'] = -1
            self.features['is_subdomain'] = -1
            self.features['domain_age'] = -1
    
    def _extract_content_features(self, url):
        """Extract features from webpage content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            self.features['num_external_links'] = len([
                link for link in soup.find_all('a', href=True)
                if urlparse(link['href']).netloc 
                and urlparse(link['href']).netloc != urlparse(url).netloc
            ])
            
            self.features['has_form'] = 1 if soup.find('form') else 0
            self.features['num_iframes'] = len(soup.find_all('iframe'))
            
        except:
            self.features['num_external_links'] = -1
            self.features['has_form'] = -1
            self.features['num_iframes'] = -1
    
    def _set_default_features(self):
        """Set default feature values when extraction fails"""
        default_features = {
            'url_length': -1,
            'num_digits': -1,
            'num_special_chars': -1,
            'has_ip_address': -1,
            'has_at_symbol': -1,
            'has_double_slash': -1,
            'domain_length': -1,
            'is_subdomain': -1,
            'domain_age': -1,
            'num_external_links': -1,
            'has_form': -1,
            'num_iframes': -1
        }
        self.features.update(default_features)
    
    def _get_feature_vector(self):
        """Convert features dictionary to numpy array"""
        feature_names = [
            'url_length', 'num_digits', 'num_special_chars',
            'has_ip_address', 'has_at_symbol', 'has_double_slash',
            'domain_length', 'is_subdomain', 'domain_age',
            'num_external_links', 'has_form', 'num_iframes'
        ]
        return np.array([self.features[name] for name in feature_names]) 