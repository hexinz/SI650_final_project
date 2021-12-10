
# Copy this file to github_settings.py (don't check it into github)

# Go to https://github.com/settings/developers

# Add a New OAuth2 App

# Using ngrok is hard because the url changes every time you start ngrok

# If you are running on localhost, here are some settings:

# Application name: ChuckList Local
# Homepage Url: http://localhost:8000
# Application Description: Whatever
# Authorization callback URL: http://127.0.0.1:8000/oauth/complete/github/


# Using PythonAnywhere here are some settings:

# Application name: ChuckList PythonAnywhere
# Homepage Url: https://drchuck.pythonanywhere.com
# Application Description: Whatever
# Authorization callback URL: https://drchuck.pythonanywhere.com/oauth/complete/github/

# Also on PythonAnywhere, go into the Web tab and enable "Force HTTPS"
# so you don't get a redirect URI mismatch.

# Then copy the client_key and secret to this file

# SOCIAL_AUTH_GITHUB_KEY = '224642424242424230ee'
# SOCIAL_AUTH_GITHUB_SECRET = 'f1afce7ffa5424242424242424242412af40ec57'

# SOCIAL_AUTH_GITHUB_KEY = 'd2b18c51bbebf96491e0'
# SOCIAL_AUTH_GITHUB_SECRET = '5775de27b0fb2ca36aeaec3b66d442582f058d77'

# for python anywhere
# SOCIAL_AUTH_GITHUB_KEY = '4f8cbdcbe11fdf20dfe3'
# SOCIAL_AUTH_GITHUB_SECRET = '0538f664b3ec91f8fc612e3089894e64be8a66cb'

# for local access
SOCIAL_AUTH_GITHUB_KEY = '12e48ab1e690c6cb41b3'
SOCIAL_AUTH_GITHUB_SECRET = '35cb5b2521a2285cb1a495c92bb3f50ba3207934'

# For detail: https://readthedocs.org/projects/python-social-auth/downloads/pdf/latest/
