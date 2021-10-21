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
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ, error
from config import *


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
        raise Exception({'success': False,
                        'message': 'Missing Authorization',
                         'error': 401}, 401)

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise Exception({'success': False,
                         'message': 'Header not in format',
                         'error': '401'}, 401)

    elif header_parts[0].lower() != 'bearer':
        raise Exception({'success': False,
                         'message': 'Missian bearer',
                         'error': '401'}, 401)

    return header_parts[1]


# --------------------------------------------------------------------------------------#
# Check permissions.
#   implement check_permissions(permission, payload) method
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise Exception({'success': False,
                        'message': 'No Permissions in header',
                         'error': '401'}, 401)

    if permission not in payload['permissions']:
        raise Exception({'success': False,
                        'message': 'unauthorized',
                         'error': '401',
                         }, 401)
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
        raise Exception({'success': False,
                        'message': 'invalid Authorization malformed',
                         'error': 401
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
            raise AuthError({'success': False,
                             'message': 'session is expired',
                             'error': '401'
                             }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({'success': False,
                             'message': 'Invalid claims',
                             'error': '401'
                             }, 401)
        except Exception:
            raise AuthError({'success': False,
                             'message': 'Invalid header',
                             'error': '400'
                             }, 400)
    raise AuthError({'success': False,
                    'message': 'invalid appropriate key',
                     'error': '400'
                     }, 400)


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
