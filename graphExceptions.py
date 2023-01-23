class GraphError (Exception):
    def __init__(self, msg):
        self.__msg = msg if isinstance(msg, str) else 'Undefined graph error'

    def __str__(self):
        return self.__msg


class GraphInitError (GraphError):
    def __init__(self, msg):
        self.__msg = msg if isinstance(msg, str) else 'Graph initializing error'

    def __str__(self):
        return self.__msg


class GraphAttributeSetError (GraphError):
    def __init__(self, name, val):
        self.__msg = f"Attribute {name} cannot be set to value {val}"

    def __str__(self):
        return self.__msg


class GraphNodeListSetError (GraphAttributeSetError):
    def __init__(self, val):
        self.__msg = '\n For a graph with N nodes: node1, node2, ... , nodeN \n' \
                     'a node list must be a dictionary, where keys form a full set (each node is given once) of nodes \n' \
                     'and each value is also a dictionary, set by the following rules: \n' \
                     '\t1. For each node X, a dictionary represents a set (each node can only be giveo once) of all the edges, joining node X and some other\n' \
                     '\t2. Each key of this dictionary is a node, which X is joint to\n' \
                     '\t3. Each value is a weight of its node, it can be of any type \n' \
                     'Dont forget: directed graphs cannot have loops' \
                     '\n ================================================================\n' \
                     'Exact problem: ' + str(val)

    def __str__(self):
        return self.__msg


class GraphFileInputError (GraphAttributeSetError):
    def __init__(self, val):
        self.__msg = '\n For a graph with N nodes: node1, node2, ... , nodeN \n' \
                     'a file must look like:\n' \
                     '[directed] or [not directed]\n' \
                     '[weighted] or [not weighted]\n' \
                     'node1 node2 ... nodeN\n' \
                     'node1\n' \
                     'joint_node1 weight\n' \
                     'joint_node2 weight\n' \
                     'etc.\n' \
                     '\n' \
                     'node2\n' \
                     'joint_node1 weight\n' \
                     'joint_node2 weight\n' \
                     'etc.\n' \
                     '\n ================================================================\n' \
                     'Exact problem: ' + str(val)

    def __str__(self):
        return self.__msg


class GraphNodeError (GraphAttributeSetError):
    def __init__(self, val):
        self.__msg = '\n Each node should have a unique, non-empty name' \
                     '\n ================================================================\n' \
                     'Exact problem: ' + str(val)

    def __str__(self):
        return self.__msg

class Default (Exception):
    def __init__(self, msg):
        self.__msg = msg if isinstance(msg, str) else 'Method found nothing'

    def __str__(self):
        return self.__msg