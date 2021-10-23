"""
This file is to check autentcation users and connect with AUTH.
written partially by Obda Al Ahdab
project number 3 in NANO degree for Udacity.
I would like to refer to this page it helped me with decode header:'https://www.programcreek.com/python/example/118165/jose.jwt.JWTClaimsError'
"""
# --------------------------------------------------------------------------------------#
# Import dependencies.
# --------------------------------------------------------------------------------------#

import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ

'''
Default data for AUTH0
'''

# AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
# ALGORITHMS = ['RS256']
# API_AUDIENCE = 'dev'

# --------------------------------------------------------------------------------------#
# AUTH0 config.
# --------------------------------------------------------------------------------------#

AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN', 'dev-uiw51rx8.us.auth0.com')
ALGORITHMS = ['RS256']
API_AUDIENCE = environ.get('API_AUDIENCE', 'http://localhost:5000')


# --------------------------------------------------------------------------------------#
# AuthError Exception.
# A standardized way to communicate auth failure modes
# --------------------------------------------------------------------------------------#


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# --------------------------------------------------------------------------------------#
# Auth Header.
#   implement get_token_auth_header() method
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#


def get_token_auth_header():

    auth_header = request.headers.get('Authorization', '')

    if not auth_header:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or not header_parts:
        raise AuthError({'code': 'invalid_header',
                        'description': 'Authorization header must be in the format'
                         ' Bearer token'}, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'}, 401)

    return header_parts[1]


# --------------------------------------------------------------------------------------#
# Check permissions.
#   implement check_permissions(permission, payload) method
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 403)
    return True


# --------------------------------------------------------------------------------------#
# Verify JWT.
#   implement verify_decode_jwt(token) method.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#


def verify_decode_jwt(token):
    jsonurl = urlopen(
        f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, '
                'check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 403)


# --------------------------------------------------------------------------------------#
# The Wrapper
#   implement @requires_auth(permission) decorator method.
# --------------------------------------------------------------------------------------#


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

# --------------------------------------------------------------------------------------#
#           The END of CODE.
# --------------------------------------------------------------------------------------#
