"""
🎓 SI STUDENT ACCOUNT - ইমেইল ডোমেইন যাচাই
utils/email_domain.py

শিক্ষা প্রতিষ্ঠানের ইমেইল ডোমেইন পরিচালনা করুন
"""

# শিক্ষা প্রতিষ্ঠানের ডোমেইনস
EDUCATIONAL_DOMAINS = {
    '.edu': 'USA',
    '.ac.bd': 'Bangladesh',
    '.edu.bd': 'Bangladesh',
    '.ac.uk': 'UK',
    '.edu.au': 'Australia'
}


def get_domain_country(email):
    """
    ইমেইল থেকে ডোমেইন এবং দেশ পান
    
    Args:
        email (str): ইমেইল ঠিকানা
    
    Returns:
        tuple: (domain, country) অথবা (None, None)
    """
    if '@' not in email:
        return None, None
    
    domain_part = email.split('@')[1].lower()
    
    for edu_domain, country in EDUCATIONAL_DOMAINS.items():
        if domain_part.endswith(edu_domain):
            return edu_domain, country
    
    return None, None


def is_educational_email(email):
    """
    ইমেইল শিক্ষা প্রতিষ্ঠানের কিনা যাচাই করুন
    
    Args:
        email (str): ইমেইল ঠিকানা
    
    Returns:
        bool: সত্য হলে True
    """
    domain, country = get_domain_country(email)
    return domain is not None


def get_allowed_domains(country=None):
    """
    দেশের জন্য অনুমতিপ্রাপ্ত ডোমেইন পান
    
    Args:
        country (str): দেশের নাম
    
    Returns:
        list: ডোমেইনের তালিকা
    """
    if country is None:
        return list(EDUCATIONAL_DOMAINS.keys())
    
    return [domain for domain, c in EDUCATIONAL_DOMAINS.items() if c == country]
