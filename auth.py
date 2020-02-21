from urllib.request import urlopen
from jose import jwt
from functools import wraps
from flask import request, _request_ctx_stack
import json
import os

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''Auth Header'''

'''
    Get the header from the request
        it raises an AuthError if no header is present
        it splits bearer and the token
        it raises an AuthError if the header is malformed
    Return the token part of the header
'''


def get_token_auth_header():
    """Obtain the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'message': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


'''
    Check permissions
    @INPUTS
        permission: string permission (i.e. 'post:bootcamp')
        payload: decoded jwt payload
    it raises an AuthError if permissions are not included in the payload
    it raisese an AuthError if the requested permission
        string is not in the payload permissions array
    Return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'message': 'Permissions not included in JWT.'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'message': 'Permission not found.'
        }, 401)
    return True


'''
    Verify decoded JWT

    @INPUTS
        token: a json web token (string)

    an Auth0 token with key id (kid)
    it verifies the token using Auth0 /.well-known/jwks.json
    it decodes the payload from the token
    it validates the claims

    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    '''Retrieve the JWKS from the Auth0 endpoint /.well-known/jwks.json'''
    print(token)
    # print(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    '''Grab the kid property from the Header of the decoded JWT'''
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'message': 'Authorization malformed.'
        }, 401)
    '''Search your filtered JWKS for the key with the matching kid property'''
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    '''Build a certificate using the corresponding x5c property in your JWKS'''
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            '''Use the certificate to verify the JWT's signature'''
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'message': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'message': 'Incorrect claims. '
                + 'Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'message': 'Unable to parse authentication token.'
            }, 401)
    raise AuthError({
        'code': 'invalid_header',
        'message': 'Unable to find the appropriate key.'
    }, 401)


'''
    Decorator method for endpoints that need authorization
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it uses the get_token_auth_header method to get the token
    it uses the verify_decode_jwt method to decode the jwt
    it uses the check_permissions method validate
      claims and check the requested permission
    return the decorator which passes the decoded payload
'''


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
