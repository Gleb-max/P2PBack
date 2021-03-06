class JsonSerializable:
    def to_json(self):
        return self.__dict__

    def __repr__(self):
        return str(self.to_json())


class Type(JsonSerializable):
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class Vertex(JsonSerializable):
    """
    # можно ещё добавить/удалить какие-нибудь поля
    # uid - id
    # name - адрес смарт контракта
    # annotation - тип смартконтракта (почти везде null кроме свапа)
    """

    def __init__(self, uid: int, name: str, annotation: str, cl: Type):
        self.uid = uid
        self.name = name
        self.annotation = annotation
        self.cl = cl


class Edge(JsonSerializable):
    """
    # можно ещё добавить/удалить какие-нибудь поля
    # uid - id
    # name - комиссия
    # method_name - имя операции (transfer, swap и тд)
    # currency - имя валюты, который принимает входная вершина
    # vertex_from - исходящая вершина ребра
    # vertex_to - входящая вершина ребра
    """

    def __init__(self, uid: int, gas_value: float, method_name, currency: str, vertex_from: Vertex, vertex_to: Vertex,
                 call_depth: str):
        self.uid = uid
        self.gas_value = gas_value
        self.method_name = method_name
        self.currency = currency
        self.vertex_from = vertex_from
        self.vertex_to = vertex_to
        self.call_depth = call_depth
