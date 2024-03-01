# This function decodes the JWT token. We can get the information about the expiration, type, time that it was issued, and many others.

import jwt


def token_hs256(token):
    payload = jwt.decode(token, algorithms=['HS256'], options={'verify_signature': False})
    return payload

token_jwt_hs256 = "YOUR TOKEN HERE"

res_hs256 = token_hs256(token_jwt_hs256)

if res_hs256:
    print("HS256 token successfully decoded:")
    print(res_hs256)
else:
    print("HS256 token decoding failure.")
