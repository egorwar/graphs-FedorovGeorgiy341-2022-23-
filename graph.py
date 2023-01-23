import copy
from graphExceptions import *
from math import cos, sin

class Graph:
    '''Realization of a graph structure'''
    __slots__ = ('__nodes', '__isDirected', '__isWeighted')

    @staticmethod
    def __check_nodelist_format(nodes: dict):
        '''checks whether a collection is either an empty dict, or a dict with dict values,
        generates GraphNodeListSetError elsewise'''
        if not isinstance(nodes, dict):
            raise GraphNodeListSetError(nodes)

        if len(nodes) == 0:
            return

        for i, x in nodes.items():
            if not isinstance(x, dict):
                raise GraphNodeListSetError(nodes)

    @staticmethod
    def __check_unique(lst: dict):
        '''checks whether a list has only unique elements,
        generates a GraphNodeListSetError exception elsewise'''
        if len(set(lst.keys())) != len(lst.keys()):
            raise GraphNodeListSetError("nodes repeated in node list")
        for el in lst.values():
            if el is None:
                return
        for node, joints in lst.items():
            nodeset = set()
            for joint, weight in joints.items():
                prev = len(nodeset)
                nodeset.add(joint)
                if prev == len(nodeset):
                    raise GraphNodeListSetError(f"node {joint} repeated in joint list for {node}")

    @staticmethod
    def __check_refer_conditions(nodes: dict, isDir: bool):
        '''for a dict with dict values checks whether keys of each value refer to the keys of the original dict,
        ALSO checks for symmetrical edges in non-directed graphs,
        generates a GraphNodeListSetError exception elsewise'''
        for node, nodeDict in nodes.items():
            for jointNode, weight in nodeDict.items():
                try:
                    nodes[jointNode]
                    if not isDir and weight != nodes[jointNode][node]:
                        raise GraphNodeListSetError(f"Edge [{node}-{jointNode} is asymmetrical]")
                except KeyError:
                    for k, v in nodes.items():
                        print(k)
                        for vk, vv in v.items():
                            print(f'({vk}:{vv})', sep='', end=' ')
                        print()
                    raise GraphNodeListSetError(f"Refering problem for {node} and {jointNode}")

    @staticmethod
    def __check_bool(name, val):
        '''checks whether a 'val' element is a bool,
        generates a GraphAttributeSetError exception elsewise'''
        if not isinstance(val, bool):
            raise GraphAttributeSetError(name, val)

    @staticmethod
    def __match_pattern(word: str, pattern: str):
        '''returns True, if [word] == [pattern];
        false, if [word] == not [pattern],
        raises GraphFileInputError exception elsewise'''
        if word == pattern:
            return True
        elif word == 'not ' + pattern:
            return False
        else:
            raise GraphFileInputError(f"'{word}' must be '{pattern}' or 'not {pattern}'")

    @classmethod
    def __validate_node_list(cls, nodes, isDir):
        '''checks whether a node dictionary meets the requirements,
        generates a GraphNodeListSetError exception elsewise'''
        # 1. Node list must be either an empty dict, or a dict with dict values
        cls.__check_nodelist_format(nodes)
        # 2. Nodes cannot repeat
        cls.__check_unique(nodes)
        # 3. All joint node names must refer to existing nodes;
        #    For non-directed graphs, check edge symmetry
        cls.__check_refer_conditions(nodes, isDir)

    def __read(self, filename):
        with open(filename, 'r') as file:
            # 1st line : directed or not
            self.__isDirected = self.__match_pattern(file.readline()[:-1], 'directed')

            # 2nd line : weighted or not
            self.__isWeighted = self.__match_pattern(file.readline()[:-1], 'weighted')

            # 3rd line : list of N nodes or an empty (and last) line
            line = file.readline()[:-1]
            if line == '':
                if file.read() == '':
                    self.__nodes = {}
                    return
                else:
                    raise GraphFileInputError("If the 3rd line is empty, nothing has to come after")
            nodedict = dict.fromkeys(line.split(' '))
            self.__check_unique(nodedict)  # nodes cannot repeat

            # reading N blocks of data
            for node in nodedict.keys():
                # 1. nodes should come in order
                c = file.readline().strip('\n')
                if c != node:
                    if c != '':
                        raise GraphFileInputError(f"node {c} doesn't exist or doesn't come in the set order")
                    else:
                        raise GraphFileInputError(
                            "Each node from the node list must be written, even if it is isolated")
                # 2. read pairs into dict
                jointdict = {}
                while True:
                    # read up to an empty line
                    s = file.readline().strip()
                    if s == '':
                        break
                    pair = s.split(' ')
                    # must be a pair
                    if len(pair) != 2:
                        if self.isWeighted:
                            raise GraphFileInputError(f"line {pair} must be a node-weight pair")
                        else:
                            pair.append(None)
                    # key must be an existing node
                    try:
                        nodedict[pair[0]]
                    except KeyError:
                        raise GraphFileInputError(f"node {pair[0]} doesen't exist")
                    # each node-weight pair should only be described once in a dict of joints
                    try:
                        jointdict[pair[0]]
                    except KeyError:
                        jointdict[pair[0]] = pair[1]
                    else:
                        raise GraphFileInputError(f"node {pair[0]} in pair {pair} is described twice or more")
                # 3. include this dict into nodedict
                if nodedict[node] != None:
                    raise GraphFileInputError(f"node {node} is described twice or more")
                nodedict[node] = jointdict

            # final check on some additional conditions
            self.__check_refer_conditions(nodedict, self.isDirected)
            self.__nodes = nodedict

    def __init__(self,
                 param='',  # 'filename.txt' or Graph object to copy
                 isDirected=False,  # whether a graph is Directed
                 isWeighted=False,  # whether a graph is Weighted
                 ):

        if not isinstance(param, (str, Graph, tuple)):
            raise GraphInitError(
                "Parameter 'param' should be a Graph object or a string representing a filename as follows: 'filename.txt'")

        elif not isinstance(isDirected, bool):
            raise GraphInitError("Property 'isDirected' should be a boolean")

        elif not isinstance(isWeighted, bool):
            raise GraphInitError("Property 'isWeighted' should be a boolean")

        # init #1
        # initialize an empty graph
        elif param == '':
            self.__nodes = {}
            self.__isDirected = isDirected
            self.__isWeighted = isWeighted

        # init #2
        # deepcopy a graph given
        elif isinstance(param, Graph):
            try:
                self.isDirected = param.isDirected
                self.isWeighted = param.isWeighted
                self.nodes = copy.deepcopy(param.nodes)
            except:
                print("Deepcopy error")

        elif isinstance(param, tuple):
            self.isDirected = False
            self.isWeighted = param[0]
            self.nodes = param[1]

        # init #3
        # read graph from file
        elif len(param.split('.')) == 2 \
                and param.split('.')[1] == 'txt':
            self.__read(param)

        else:
            raise GraphInitError(f"Parameter '{param}' doesn't represent an appropriate filename")

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, nodes):
        self.__validate_node_list(nodes, self.isDirected)
        self.__nodes = nodes

    @nodes.deleter
    def nodes(self):
        self.__nodes = {}

    @property
    def isDirected(self):
        return self.__isDirected

    @isDirected.setter
    def isDirected(self, isDirected):
        self.__check_bool('isDirected', isDirected)
        self.__isDirected = isDirected

    @property
    def isWeighted(self):
        return self.__isWeighted

    @isWeighted.setter
    def isWeighted(self, isWeighted):
        self.__check_bool('isWeighted', isWeighted)
        self.__isWeighted = isWeighted

    def add_node(self, node):
        '''Add an isolated node. Name should be unique and non-empty, or GraphNodeError exception will be triggered'''
        if node == '':
            raise GraphNodeError("Node name cannot be empty")
        try:
            self.nodes[node]
        except KeyError:
            self.nodes[node] = {}
        else:
            raise GraphNodeError(f"Node '{node}' already exists")

    def del_node(self, node, d=-1):
        '''Removes the node with all its edges. Node with given name should exist,
        or GraphNodeError exception will be triggered'''
        if d == -1:
            d = self.nodes
        try:
            d[node]
        except KeyError:
            raise GraphNodeError(f"Node '{node}' doesn't exist")
        else:
            d.pop(node, None)
            for vert, joints in d.items():
                joints.pop(node, None)

    def add_edge(self, origin, destination, weight=None):
        '''Add an edge from origin to destination. Both given nodes should exist and should not be linked
        from origin to destination, or GraphNodeError exception will be triggered'''
        if origin == '' or destination == '':
            raise GraphNodeError("Node names cannot be empty")
        try:
            self.nodes[origin]
            self.nodes[destination]
        except KeyError:
            raise GraphNodeError(f"Node '{origin}' or '{destination}' doesn't exist")
        else:
            try:
                self.nodes[origin][destination]
            except KeyError:
                self.nodes[origin][destination] = weight
                if not self.isDirected:
                    self.nodes[destination][origin] = weight
            else:
                raise GraphNodeError(f"An edge from '{origin}' to '{destination}' already exists with weight "
                                     f"{self.nodes[origin][destination]}")

    def del_edge(self, origin, destination):
        '''Remove an edge from origin to destination. Both given nodes should exist and should be linked
        from origin to destination, or GraphNodeError exception will be triggered'''
        if origin == '' or destination == '':
            raise GraphNodeError("Node names cannot be empty")
        try:
            self.nodes[origin]
            self.nodes[destination]
        except KeyError:
            raise GraphNodeError(f"Node '{origin}' or '{destination}' doesn't exist")
        else:
            try:
                self.nodes[origin][destination]
            except KeyError:
                raise GraphNodeError(f"An edge from '{origin}' to '{destination}' doesn't exist")
            else:
                self.nodes[origin].pop(destination)
                if not self.isDirected:
                    self.nodes[destination].pop(origin)

    def save(self, filename):
        '''Writes graph data into the file with specified filename
        WARNING: if such file already exists, its previous contents will be lost'''
        try:
            with open(filename, "w") as file:
                file.write(('' if self.isDirected else 'not ') + 'directed\n')
                file.write(('' if self.isWeighted else 'not ') + 'weighted\n')
                file.write(' '.join(str(x) for x in self.nodes.keys()) + '\n')
                for node, joints in self.nodes.items():
                    file.write(str(node) + '\n')
                    if joints != {}:
                        for joint, weight in joints.items():
                            file.write(f"{str(joint)} {str(weight)}\n")
                    file.write('\n')
        except FileNotFoundError:
            raise GraphError(f"Incorrect filename: {filename}")

    def __call__(self):
        print(('' if self.isDirected else 'not ') + 'directed')
        print(('' if self.isWeighted else 'not ') + 'weighted')
        print(' '.join(str(x) for x in self.nodes.keys()))
        for node, joints in self.nodes.items():
            print(str(node))
            if joints != {}:
                for joint, weight in joints.items():
                    if self.isWeighted:
                        print(f"{str(joint)} {str(weight)}")
                    else:
                        print(str(joint))
            print()

    def __mirror(self, d=-1):
        '''Gets an inverted node dict, where for each destination node a dict of source nodes is given'''
        if d == -1:
            d = self.nodes
        mirror = dict((key, {}) for key in d.keys())
        for node, joints in d.items():
            for joint, weight in joints.items():
                mirror[joint][node] = weight
        return mirror

    def lesser_income_then(self, x: str):
        try:
            self.nodes[x]
        except KeyError:
            raise GraphNodeError(f"node [{str(x)}] does not exist.")
        else:
            mirror = self.__mirror()
            ans = dict(filter(lambda c: len(c[1]) < len(mirror[x]), mirror.items())).keys()
            print(*ans)

    def find_between(self, a: str, b: str):
        try:
            self.nodes[a]
        except KeyError:
            raise GraphNodeError(f"node [{str(a)}] does not exist.")

        try:
            self.nodes[b]
        except KeyError:
            raise GraphNodeError(f"node [{str(b)}] does not exist.")

        if a == b:
            raise GraphError("Nodes should not be equal")

        mirror = self.__mirror()
        for i in self.nodes[a].keys():
            if i == a or i == b:
                continue
            for j in self.nodes[i].keys():
                if j == a:
                    continue
                if j == b:
                    return i
            for j in mirror[i].keys():
                if j == a:
                    continue
                if j == b:
                    return i
        for i in mirror[a].keys():
            if i == a or i == b:
                continue
            for j in self.nodes[i].keys():
                if j == a:
                    continue
                if j == b:
                    return i
            for j in mirror[i].keys():
                if j == a:
                    continue
                if j == b:
                    return i
        raise Default(f"nodes [{str(a)}] and [{str(b)}] does not have a common neighbour.")

    def undirect(self):
        if not self.isDirected:
            raise GraphError("Graph is already undirected")
        result = copy.deepcopy(self.nodes)
        for node, joints in result.items():
            for joint, weight in joints.items():
                result[joint][node] = weight
        return result

    def check_tree(self):
        '''checks if you can make an oriented tree from the graph by removing one node'''
        # 0. Cut off degenerated graphs
        if len(self.nodes.keys()) < 3:
            print("Graph is too simple")
            return ''

        verts = copy.deepcopy(self.nodes)
        deleted = False
        mirror = self.__mirror(verts)

        # 1. Find all isolated nodes, remove first. If there is more, tree is impossible
        for node, joints in mirror.items():
            if len(joints) == 0 and len(verts[node]) == 0:
                if deleted:
                    print("Cannot create tree: too much isolated nodes")
                    return ''
                else:
                    deleted = node
        if deleted:
            self.del_node(deleted, verts)

        # 2. Find all nodes with 0 in-edges;
        #    - if there is none, try removing each edge and try start from each new 0 in-edge node
        #    - if there is one, start from it
        #    - if there are 2, try removing each and start from the other
        #    - if there are more than 2, tree is impossible
        mirror = self.__mirror(verts)
        in_zero = []
        for node, ins in mirror.items():
            if len(ins) == 0:
                in_zero.append(node)
            if len(in_zero) == 2 and deleted:
                print("Cannot create tree: 2 nodes with no incoming edges, and one node is already deleted")
                return ''
            if len(in_zero) > 2:
                print("Cannot create tree: too much nodes with no incoming edges")
                return ''
        if len(in_zero) == 0 and deleted:
            print("Cannot create tree: no nodes with no incoming edges, and one node is already deleted")
            return ''

        # print(f"deleted: {deleted}")
        # for k, v in verts.items():
        #     print(k)
        #     for vk, vv in v.items():
        #         print(f"({vk},{vv})", sep='', end=' ')
        #     print()
        # for k, v in mirror.items():
        #     print(k)
        #     for vk, vv in v.items():
        #         print(f"({vk},{vv})", sep='', end=' ')
        #     print()

        # 3. All peculiar conditions are managed, now a simple search
        prev = deleted
        list(mirror.keys())
        for node_to_delete in list(mirror.keys()):
            deleted = prev
            cverts = copy.deepcopy(verts)
            # try to delete another node, if nothing was previously deleted
            if not deleted:
                self.del_node(node_to_delete, cverts)
                deleted = node_to_delete
            cmirror = self.__mirror(cverts)
            # then find a node with no in-edges, tree is impossible if there is none
            root = ''
            for node, ins in cmirror.items():
                if len(ins) == 0:
                    root = node
                    break
            if root == '':
                continue
            res = self.dfs(root, cverts)
            try:
                res[-1]
            except KeyError:
                if len(res.keys()) == len(cverts.keys()):
                    return deleted, root
        print("All possibilities checked: impossible to create tree")
        return ''

    def dfs(self, x, d=-1):
        if d == -1:
            d = self.nodes
        try:
            d[x]
        except KeyError:
            raise GraphNodeError(f"Node '{x}' doesn't exist")

        res = dict()
        visited = dict.fromkeys(d.keys(), False)

        def __dfs(node, path):
            visited[node] = True
            res[node] = path
            for nxt in d[node]:
                if not visited[nxt]:
                    __dfs(nxt, path + 1)
                else:
                    res[-1] = None
            return

        __dfs(x, 0)
        return res

    def dfs1(self, x):
        d = self.nodes
        try:
            d[x]
        except KeyError:
            raise GraphNodeError(f"Node '{x}' doesn't exist")

        res = []
        visited = dict.fromkeys(d.keys(), False)

        def __dfs(parent, node):
            visited[node] = True
            res.append((parent, node))
            for nxt in d[node]:
                if not visited[nxt]:
                    __dfs(node, nxt)
            return

        __dfs(x, x)
        return res

    def bfs(self, x):
        try:
            self.nodes[x]
        except KeyError:
            raise GraphNodeError(f"Node '{x}' doesn't exist")
        res = dict()
        visited = dict.fromkeys(self.nodes.keys(), False)
        queue = dict({x: 0}, **dict.fromkeys(self.nodes[x].keys(), 1))
        for el in queue.keys():
            visited[el] = True

        while queue:
            node = list(queue.keys())[0]
            res[node] = queue[node]
            visited[node] = True
            for el in self.nodes[node].keys():
                if not visited[el]:
                    visited[el] = True
                    queue[el] = res[node] + 1
                    if node == 'g':
                        print(queue[el])
            del queue[node]

        return res

    def radius(self):
        excs = sorted(zip([max(self.bfs(x).values()) for x in self.nodes.keys()], self.nodes.keys()),
                      key=lambda x: x[0])
        print(excs)
        return list(filter(lambda x: x[0] == excs[0][0], excs))

    def kruskal(self):
        # 1. Save graph structure as a set of triples like (nodeA, edge_weight, nodeB),
        #    where nodeA < nodeB (to prevent duplicating)
        verts = set()
        for node, joints in self.nodes.items():
            for joint, weight in joints.items():
                if node == joint:
                    continue  # skip loops, they are useless in this algorithm
                try:
                    verts.add((min(node, joint), float(weight), max(node, joint)))
                except Exception:
                    print("Weights should be numbers!")
                    raise Exception

        # 2. Now sort it by weights in ascending order (it'll return a list)
        verts = sorted(verts, key=lambda triple: triple[1])

        # 3. create a list of lists, representing connected components
        #    each node alone will form it's component at start, components will merge in process
        components = [[x] for x in self.nodes.keys()]

        # 4. Kruskal algorithm itself
        res = []
        for triple in verts:
            iA = -1
            iB = -1
            # find connected component of nodeA
            for i in range(len(components)):
                for node in components[i]:
                    if triple[0] == node:
                        iA = i
                        break
                if iA != -1:
                    break
            # find connected component of nodeB
            for i in range(len(components)):
                for node in components[i]:
                    if triple[2] == node:
                        iB = i
                        break
                if iB != -1:
                    break
            if iA == iB:
                continue
            res.append(triple)
            components[iA].extend(components[iB])
            components.pop(iB)

        # 5. Separate nodes into components
        blocks = dict()
        visited = set(self.nodes.keys())
        while visited:
            k = visited.pop()
            block = set(self.bfs(k).keys())
            visited.add(k)
            for item in block:
                visited.remove(item)
            blocks[''.join(str(x) for x in block)] = []

        for link in res:
            for group in blocks.keys():
                if link[0] in group:
                    blocks[group].append(link)
                    continue
        return blocks

    def negloop(self):
        '''Start Bellman-Ford from each node until it returns False,
        then find the negative loop using predecessors list and return it'''

        verts = list() if self.isDirected else set()
        for node, joints in self.nodes.items():
            for joint, weight in joints.items():
                if node == joint:
                    continue
                try:
                    if self.isDirected:
                        verts.append((node, float(weight), joint))
                    else:
                        verts.add((min(node, joint), float(weight), max(node, joint)))
                except Exception:
                    print("Weights should be numbers!")
                    raise Exception

        for node in self.nodes.keys():
            pred, changed, res = self.bellman_ford(node, verts)

            # no negative loop
            if res:
                break #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # find negative loop by going through [pred] starting from [changed]

    def bellman_ford(self, node, verts):
        print('1: ', node, verts)
        d = dict(zip(self.nodes.keys(), [float("Inf")] * len(self.nodes)))
        p = dict(zip(self.nodes.keys(), [None] * len(self.nodes)))
        d[node] = 0

        for _ in range(len(self.nodes) - 1):
            for v, w, u in verts:
                print('comp: ', v, w, u)
                if d[v] > d[u] + w and d[u] != float("Inf"):
                    d[v] = d[u] + w
                    p[v] = u
        for v, w, u in verts:
            if d[v] > d[u] + w and d[u] != float("Inf"):
                return p, v, False
        print(d)
        print(p)
        return p, None, True

    def kpaths(self, start, dest, k):
        k = int(k)
        answer = []    # k shortest paths: (length, [path])
        to_each = dict(zip(self.nodes.keys(), [0] * len(self.nodes)))  # number of shortest paths to each node
        pathheap = [(0, [start])]
        while len(pathheap) and to_each[dest] < k:
            shortest = min(pathheap, key=lambda x: x[0])
            pathheap.remove(shortest)
            to_each[shortest[1][-1]] += 1
            if shortest[1][-1] == dest:
                answer.append(shortest)
            if to_each[shortest[1][-1]] <= k:
                for joint, weight in self.nodes[shortest[1][-1]].items():
                    pathheap.append((shortest[0] + float(weight), shortest[1] + [joint]))
        return answer

    @staticmethod
    def draw_node(canvas, pos, name, color, size):

        # draw corners
        canvas[pos[1] - size][pos[0] - size * 3] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '╭' + '\033[0;0m'
        canvas[pos[1] - size][pos[0] + size * 3] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '╮' + '\033[0;0m'
        canvas[pos[1] + size][pos[0] - size * 3] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '╰' + '\033[0;0m'
        canvas[pos[1] + size][pos[0] + size * 3] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '╯' + '\033[0;0m'

        # draw top and bottom sides
        canvas[pos[1] - size][pos[0] - size * 3 + 1: pos[0] + size * 3] = \
            [f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '─' + '\033[0;0m'] * ((size * 3 - 1) * 2 + 1)
        canvas[pos[1] + size][pos[0] - size * 3 + 1: pos[0] + size * 3] = \
            [f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '─' + '\033[0;0m'] * ((size * 3 - 1) * 2 + 1)

        # draw left and right sides
        for line in range(pos[1] - size + 1, pos[1] + size):
            canvas[line][pos[0] - size * 3] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '│' + '\033[0;0m'
            canvas[line][pos[0] + size * 3] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '│' + '\033[0;0m'

        # insert node name
        name = str(name)
        if len(name) > size * 6 - 1:
            name = name[:size * 6 - 1]
        canvas[pos[1]][pos[0] - int(len(name) / 2): pos[0] + len(name) - int(len(name) / 2)] = name

    @staticmethod
    def angle(n):
        next = 0
        step = 2 * 3.1415 / n
        while next < 2 * 3.1415:
            yield next
            next += step

    @staticmethod
    def draw_line(canvas, start, end, color, size, weight, weighted):

        borders = ['╭', '╮', '╰', '╯', '─', '│']
        inside = True   # whether current position is within node or not
        block = False
        overprint = color == (255, 255, 255)
        w = str(weight)[:10]

        # if nodeX and jointX are the same, we draw vertical line
        if start[0] == end[0]:
            for y in range(start[1], end[1], 1 if start[1] < end[1] else -1):
                # switch inside trigger when crossing border
                if len(canvas[y][start[0]]) > 1 and canvas[y][start[0]][-7] in borders:
                    inside = not inside
                    continue
                # draw if outside and nothing is drawn yet on this point
                if not inside:
                    if canvas[y][start[0]] == ' ':
                        canvas[y][start[0]] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '█' + '\033[0;0m'
                    if weighted:
                        # check if weight fits on current row
                        for el in range(start[0], start[0] + len(w)):
                            if canvas[y][el] in borders or len(canvas[y][el]) > 1 and canvas[y][el][-7] != '█':
                                if not overprint:
                                    break
                        else:
                            canvas[y][start[0]: start[0] + len(w)] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + w + '\033[0;0m'
                            weighted = False

        # if nodeY and jointY are the same, we draw horizontal line
        elif start[1] == end[1]:
            for x in range(start[0], end[0], 1 if start[0] < end[0] else -1):
                # switch inside trigger when crossing border
                if len(canvas[start[1]][x]) > 1 and canvas[start[1]][x][-7] in borders:
                    inside = not inside
                    continue
                # draw if outside and nothing is drawn yet on this point
                if not inside:
                    if canvas[start[1]][x] == ' ':
                        canvas[start[1]][x] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '█' + '\033[0;0m'
                    if weighted:
                        # check if weight fits on current row
                        for el in range(x, x + len(w)):
                            if canvas[start[1]][el] in borders or len(canvas[start[1]][el]) > 1 and canvas[start[1]][el][-7] != '█':
                                if not overprint:
                                    break
                        else:
                            canvas[start[1]][x: x + len(w)] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + w + '\033[0;0m'
                            weighted = False

        # if we have to draw diagonal line
        else:
            prev = ' '
            # coefficients for line equation
            p = (start[1] - end[1]) / (start[0] - end[0])
            q = start[1] - p * start[0]

            # if the angle between Ox and line is less than or equal to 45 degrees,
            # it is better to calculate single y for each x
            if abs(p) <= 1:
                for x in range(start[0], end[0], 1 if start[0] < end[0] else -1):
                    y = int(p * x + q)
                    if inside and (len(canvas[y][x]) == 1 or canvas[y][x][-7] not in borders) and prev in borders and not block:
                        inside = False
                    if not inside and len(canvas[y][x]) > 1 and canvas[y][x][-7] in borders:
                        inside = True
                        if abs(x - end[0]) < size + 3 or abs(y - end[1]) < size + 3:
                            block = True
                    if not inside:
                        if canvas[y][x] == ' ':
                            canvas[y][x] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '█' + '\033[0;0m'
                        if weighted:
                            # print("check weighted for", w, " with overprint", overprint, "on coords: from ", x, "to", x + len(w), "with start coords: ", start[0], start[1])
                            for el in range(x, x + len(w)):
                                if canvas[y][el] in borders or len(canvas[y][el]) > 1 and canvas[y][el][-7] != '█':
                                    if not overprint:
                                        break
                            else:
                                canvas[y][x: x + len(w)] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + w + '\033[0;0m'
                                weighted = False
                    prev = canvas[y][x][-7] if len(canvas[y][x]) > 1 else canvas[y][x]
            else:
                # if the angle between Ox and line is more than 45 degrees,
                # it is better to calculate single x for each y
                for y in range(start[1], end[1], 1 if start[1] < end[1] else -1):
                    x = int((y - q) / p)
                    if inside and (len(canvas[y][x]) == 1 or canvas[y][x][-7] not in borders) and prev in borders and not block:
                        inside = False
                    if not inside and len(canvas[y][x]) > 1 and canvas[y][x][-7] in borders:
                        inside = True
                        block = True
                    if not inside:
                        if canvas[y][x] == ' ':
                            canvas[y][x] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + '█' + '\033[0;0m'
                        if weighted:
                            for el in range(x, x + len(w)):
                                if canvas[y][el] in borders or len(canvas[y][el]) > 1 and canvas[y][el][-7] != '█':
                                    if not overprint:
                                        break
                            else:
                                canvas[y][x: x + len(w)] = f'\033[38;2;{color[0]};{color[1]};{color[2]}m' + w + '\033[0;0m'
                                weighted = False
                    prev = canvas[y][x][-7] if len(canvas[y][x]) > 1 else canvas[y][x]

    def draw(self, isAnim=False, isDfs=None):
        n = len(self.nodes)
        if n == 0:
            return ['\nGRAPH IS EMPTY\n']

        # consts
        width = 340
        height = 65
        startX = 170
        startY = 32
        r = 29
        size = 2
        colors = [(243, 195, 0), (135, 86, 146), (243, 132, 0), (161, 202, 241), (190, 0, 50),
                  (194, 178, 128), (132, 132, 130), (0, 136, 86), (230, 143, 172), (0, 103, 165),
                  (249, 147, 121), (96, 78, 151), (246, 166, 0), (179, 68, 108), (220, 211, 0),
                  (136, 45, 23), (141, 182, 0), (101, 69, 34), (226, 88, 34)]

        # variables
        canvas = [[' '] * width for _ in range(height)]
        node_info = dict.fromkeys(self.nodes.keys())    # for each node it stores (x, y) and color
        node_iter = list(self.nodes.keys())             # list of node names


        # 1. split 360 degrees into n equal angles
        angs = list(self.angle(n))

        # 2. with given radius and starting point, transfer angles from polar to cartesian coords and draw nodes
        for i in range(n):
            node_info[node_iter[i]] = (int(startX + r * cos(angs[i]) * 4), int(startY + r * sin(angs[i])), colors[i])
            self.draw_node(canvas, node_info[node_iter[i]][:-1], node_iter[i], colors[i], size)  # canvas, (x, y), name, color, size

        if isAnim:
            frames = [copy.deepcopy(canvas)]

        # 3. draw edges
        if isDfs == None:
            skip = set()  # node pairs (min_name, max_name) that should be skipped

            for node, info in node_info.items():
                for joint in self.nodes[node].keys():
                    if (min(node, joint), max(node, joint)) in skip:
                        continue
                    try:
                        self.nodes[joint][node]
                    except KeyError:
                        # if node->joint but not joint->node, draw line with the color of the node:
                        # (canvas, (nodeX, nodeY), (jointX, jointY), node_color, size, weight, is_weighted)
                        self.draw_line(canvas, info[:-1], node_info[joint][:-1], info[-1], size, self.nodes[node][joint], self.isWeighted)
                        if isAnim:
                            frames.append(copy.deepcopy(canvas))
                    else:
                        # if node is joint, it is a loop - write 'LOOP' or it's weight in the corner of the node
                        if node == joint:
                            if self.isWeighted:
                                w = str(self.nodes[joint][node])
                                if len(w) > size * 6 - 1:
                                    w = w[:size * 6 - 1]
                                canvas[info[1] - size + 1][info[0] - size * 3 + 1: info[0] - size * 3 + 1 + len(w)] = w
                            else:
                                canvas[info[1] - size + 1][info[0] - size * 3 + 1: info[0] - size * 3 + 1 + 4] = 'LOOP'
                        else:
                            # if both node->joint and joint->node exist
                            self.draw_line(canvas, info[:-1], node_info[joint][:-1], (255, 255, 255), size, self.nodes[node][joint], self.isWeighted)
                            if isAnim:
                                frames.append(copy.deepcopy(canvas))
                            if not self.isDirected:
                                skip.add((min(node, joint), max(node, joint)))

            return frames if isAnim else canvas
        else:
            search = self.dfs1(isDfs)[1:]

            for parent, child in search:
                # node = self.nodes[parent]
                # joint = self.nodes[child]
                try:
                    self.nodes[child][parent]
                except KeyError:
                    # if node->joint but not joint->node, draw line with the color of the node:
                    # (canvas, (nodeX, nodeY), (jointX, jointY), node_color, size, weight, is_weighted)
                    self.draw_line(canvas, node_info[parent][:-1], node_info[child][:-1], node_info[parent][-1], size, self.nodes[parent][child], self.isWeighted)
                    if isAnim:
                        frames.append(copy.deepcopy(canvas))
                else:
                    # if both node->joint and joint->node exist
                    self.draw_line(canvas, node_info[parent][:-1], node_info[child][:-1], (255, 255, 255), size, self.nodes[parent][child], self.isWeighted)
                    if isAnim:
                        frames.append(copy.deepcopy(canvas))
            return frames if isAnim else canvas




# width = 340
# height = 90
# startX = 170
# startY = 45
# r = 40
# size = 3