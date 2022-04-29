from types import SimpleNamespace

import requests as requests

import constants
from models import Vertex, Edge, Type


def authorized_api_request(_type='POST', **kwargs) -> requests.Response:
    TYPE_TO_METHOD = {
        'POST': requests.post,
    }
    return TYPE_TO_METHOD[_type](constants.API_URL, headers={'X-API-KEY': constants.API_KEY}, **kwargs)


def api_search(t: str):
    data = {
        "tx": t,
    }
    r_t = authorized_api_request(json={
        'query': constants.SEARCH_QUERY,
        'variables': data,
    })
    if r_t.status_code == 200:
        # print(
        #     str(r_t.json()).replace('\'', '"').replace('True', 'true').replace('False', 'false').replace('None',
        #                                                                                                  'null'),
        #     file=open('api-ans.json', 'w'))
        return parse_tx(r_t.json(object_hook=lambda d: SimpleNamespace(**d)))
    else:
        print(r_t.status_code)
        print(r_t.text)
        return None


def api_events(t: str):
    data = {
        "tx": t,
    }
    r_e = authorized_api_request(json={
        'query': constants.EVENTS_QUERY,
        'variables': data,
    })
    if r_e.status_code == 200:
        return {'events': sorted(r_e.json()['data']['ethereum']['smartContractEvents'],
                                 key=lambda x: (-1,) if not x['eventIndex'] else tuple(
                                     map(int, x['eventIndex'].split('-'))))}
    else:
        print(r_e.status_code)
        print(r_e.text)
        return None


def get_vertex_class(edge):
    if edge.smartContract.address.annotation:
        return Type(*edge.smartContract.address.annotation.split(', ', 1))
    # if edge.smartContract.contractType == 'Generic':
    #     return Type('Smart contract', edge.smartContract.address.annotation or 'unclassified')
    if edge.smartContract.contractType == 'Token':
        return Type('Token', edge.smartContract.currency.symbol)
    if edge.smartContract.contractType == 'DEX':
        return Type('Exchanger', edge.smartContract.protocolType)
    return Type('User', 'address')


def parse_tx(root):
    vertexes_adresses = dict()
    edges = []
    vertex_uid = 0
    edge_uid = 0
    for edge in root.data.ethereum.smartContractCalls:
        if edge.caller.address not in vertexes_adresses.keys():
            v = Vertex(vertex_uid, edge.caller.address, edge.caller.annotation, get_vertex_class(edge))
            vertex_uid += 1
            vertexes_adresses[edge.caller.address] = v
        if edge.smartContract.address.address not in vertexes_adresses.keys():
            v = Vertex(vertex_uid, edge.smartContract.address.address, edge.smartContract.address.annotation,
                       get_vertex_class(edge))
            vertex_uid += 1
            vertexes_adresses[edge.smartContract.address.address] = v
        edges.append(Edge(edge_uid,
                          edge.gasValue, edge.smartContractMethod.name,
                          edge.smartContract.currency.symbol,
                          vertexes_adresses[edge.caller.address],
                          vertexes_adresses[edge.smartContract.address.address],
                          edge.callDepth))
        edge_uid += 1
    if edges:
        return {'vertexes': [{
            'name': key,
            'class': value.cl,
            'uid': value.uid,
        } for key, value in vertexes_adresses.items()], 'edges': edges}
    return {}
