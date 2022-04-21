from types import SimpleNamespace

import requests as requests

import constants
from models import Vertex, Edge


def authorized_api_request(_type='POST', **kwargs) -> requests.Response:
    TYPE_TO_METHOD = {
        'POST': requests.post,
    }
    return TYPE_TO_METHOD[_type](constants.API_URL, headers={'X-API-KEY': constants.API_KEY}, **kwargs)


def api_search(t: str):
    data = {
        "tx": t,
    }
    r = authorized_api_request(json={
        'query': constants.SEARCH_QUERY,
        'variables': data,
    })
    if r.status_code == 200:
        print(
            str(r.json()).replace('\'', '"').replace('True', 'true').replace('False', 'false').replace('None', 'null'),
            file=open('api-ans.json', 'w'))
        return parse_tx(r.json(object_hook=lambda d: SimpleNamespace(**d)))
    else:
        print(r.status_code)
        print(r.text)
        return None


def parse_tx(root):
    vertexes_adresses = dict()
    edges = []
    vertex_uid = 0
    edge_uid = 0
    for edge in root.data.ethereum.smartContractCalls:
        if edge.caller.address not in vertexes_adresses.keys():
            v = Vertex(vertex_uid, edge.caller.address, edge.caller.annotation)
            vertex_uid += 1
            vertexes_adresses[edge.caller.address] = v
        if edge.smartContract.address.address not in vertexes_adresses.keys():
            v = Vertex(vertex_uid, edge.smartContract.address.address, edge.smartContract.address.annotation)
            vertex_uid += 1
            vertexes_adresses[edge.smartContract.address.address] = v
        edges.append(Edge(edge_uid,
                          edge.gasValue, edge.smartContractMethod.name,
                          edge.smartContract.currency.symbol,
                          vertexes_adresses[edge.caller.address],
                          vertexes_adresses[edge.smartContract.address.address]))
        edge_uid += 1
    if edges:
        return {'vertexes': [{
            'name': key,
            'class': 'unknown',
            'uid': value.uid,
        } for key, value in vertexes_adresses.items()], 'edges': edges}
    return {}


if __name__ == '__main__':
    print(api_search('0xc68d4bd2932473659213d21c6bf788d04bafe6a8f2bc4f12c2032884cddec729'))
    print(api_search('99034'))
