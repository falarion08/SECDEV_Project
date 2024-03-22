# Content Security Policy (CSP) Header
SELF = "\'self\'"

csp = {
   'default-src': ['\'self\'',
                   'https://www.google.com/recaptcha/api.js',
                    'https://www.gstatic.com/'],
    'script-src': ['\'self\'',
                   'https://www.google.com/recaptcha/api.js',
                   ' https://www.gstatic.com/'],
    'frame-src':['\'self\'',
                 'https://www.google.com/recaptcha/api.js',
                   ' https://www.gstatic.com/']


}

# HTTP Strict Transport Security (HSTS) Header
hsts = {
    'max-age': 31536000,
    'includeSubDomains': True
}

nonce_list = ['default-src', 'script-src']


def setup_talisman(talisman):
    # Enforce HTTPS and other headers
    talisman.force_https = True # note: does not force HTTPS if flask app is in debug mode
    talisman.force_file_save = True
    talisman.x_xss_protection = True
    talisman.session_cookie_secure = True
    talisman.session_cookie_samesite = 'Lax'
    talisman.content_security_policy = csp
    talisman.strict_transport_security = hsts
    talisman.content_security_policy_nonce_in = nonce_list
