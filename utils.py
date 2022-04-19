import constants
import requests as requests


def authorized_api_request(_type='POST', **kwargs) -> requests.Response:
    TYPE_TO_METHOD = {
        'POST': requests.post,
    }
    return TYPE_TO_METHOD[_type](constants.API_URL, headers={'X-API-KEY': constants.API_KEY}, **kwargs)


def api_search(t: str):
    data = {
        "limit": 1000,
        "offset": 0,
        "address": t,
        "from": None,
        "till": None,
        "dateFormat": "%Y-%m"
    }
    r = authorized_api_request(json={
        'query': constants.SEARCH_QUERY,
        'variables': data,
    })
    if r.status_code == 200:
        return r.json()
    else:
        print(r.status_code)
        print(r.text)
        return None


if __name__ == '__main__':
    api_search('0xc68d4bd2932473659213d21c6bf788d04bafe6a8f2bc4f12c2032884cddec729')
