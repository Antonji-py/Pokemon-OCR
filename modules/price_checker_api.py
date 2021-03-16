import requests
import json
from requests_oauthlib import OAuth1
from oauthlib.oauth1 import Client
from requests.utils import to_native_string
from urllib.parse import unquote


APP_TOKEN = "u7BDU9wZxo3ve46L"
APP_SECRET = "MhKOoZgayQKZhz3UitUOnMAV0ByobLxk"
ACCESS_TOKEN = "sk8zhNZivKv5oG70ie7SA5mCokOYUoqs"
ACCESS_TOKEN_SECRET = "O3EtWRjT65pOCyTHXfttMNZuEor1wPgq"

url = "https://api.cardmarket.com/ws/v2.0/products/find?search=Springleaf&idGame=1&idLanguage=1"


class MKMOAuth1(OAuth1):
    def __call__(self, r):
        r = super(MKMOAuth1, self).__call__(r)

        r.prepare_headers(r.headers)

        correct_signature = self.decode_signature(r.headers)

        r.headers.__setitem__("Authorization", correct_signature)
        r.url = to_native_string(r.url)
        return r

    @staticmethod
    def decode_signature(given_header):
        authorization_byte = given_header["Authorization"]
        authorization_string = authorization_byte.decode()
        signature_position = authorization_string.find('oauth_signature="') + len('oauth_signature="')
        sub_string_signature = authorization_string[signature_position:]

        decoded_sub_string_signature = unquote(sub_string_signature)
        authorization_string = authorization_string[:signature_position]
        authorization_string = "{}{}".format(authorization_string, decoded_sub_string_signature)

        return authorization_string


class MKMClient(Client):
    def get_oauth_params(self, request):
        parameters = super(MKMClient, self).get_oauth_params(request)

        oauthParamExist = False

        for param in parameters:
            if "oauth_token" in param:
                oauthParamExist = True
                break

        if not oauthParamExist:
            parameters.append(("oauth_token", ""))

        return parameters


auth = MKMOAuth1(
            APP_TOKEN,
            client_secret=APP_SECRET,
            resource_owner_key=ACCESS_TOKEN,
            resource_owner_secret=ACCESS_TOKEN_SECRET,
            client_class=Client,
            realm=url,
        )

response = requests.get(url, auth=auth, allow_redirects=False)
print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))