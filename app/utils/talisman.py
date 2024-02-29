# Content Security Policy (CSP) Header
csp = {
    'default-src': [
        '\'self\'',
        'https://code.jquery.com',
        'https://cdn.jsdelivr.net'
    ]
}

# HTTP Strict Transport Security (HSTS) Header
hsts = {
    'max-age': 31536000,
    'includeSubDomains': True
}

def setup_talisman(talisman):
    # Enforce HTTPS and other headers
    talisman.force_https = True # note: does not force HTTPS if flask app is in debug mode
    talisman.force_file_save = True
    talisman.x_xss_protection = True
    talisman.session_cookie_secure = True
    talisman.session_cookie_samesite = 'Lax'
    talisman.frame_options_allow_from = 'https://www.google.com'
    talisman.content_security_policy = csp
    talisman.strict_transport_security = hsts
