def cartesian_product(list0: list, *rest: list):
    if not rest:
        return [[l] for l in list0]
    res = []
    for el in list0:
        for n_pair in cartesian_product(*rest):
            res.append([el] + n_pair)
    return res
class Dict:
    def __init__(self, *args: (object, object)):
        self.__items = []
        for arg in args:
            if arg not in self.__items:
                if len(arg) != 2:
                    raise ValueError('Pairs of keys and values expected!')
                if arg[1] is not None:
                    self.__items.append(arg)
        for i, item1 in enumerate(self.__items):
            for item2 in self.__items[i + 1:]:
                if item1[0] == item2[0]:
                    raise KeyError('No similar keys in a dictionary allowed!')
        self.__keys, self.__values = [p[0] for p in self.__items], [p[1] for p in self.__items]
    def keys(self):
        return self.__keys
    def values(self):
        return self.__values
    def items(self):
        return self.__items
    def pop(self, item):
        for i, p in enumerate(self.__items):
            if item == p[0]:
                self.__items.remove(p), self.__keys.remove(item), self.__values.pop(i)
                return p[1]
    def popitem(self):
        if self.items():
            res = self.__items[-1]
            self.__items.pop(), self.__keys.pop(), self.__values.pop()
            return res
    def copy(self):
        return Dict(*self.__items)
    def __len__(self):
        return len(self.__items)
    def __contains__(self, item):
        return item in self.__keys
    def __delitem__(self, key):
        self.pop(key)
    def __getitem__(self, item):
        try:
            return self.__values[self.__keys.index(item)]
        except ValueError:
            pass
    def __setitem__(self, key, value):
        try:
            self.__items[self.__keys.index(key)] = (key, value)
            self.__values[self.__keys.index(key)] = value
        except ValueError:
            self.__items.append((key, value)), self.__keys.append(key), self.__values.append(value)
    def __add__(self, other):
        if isinstance(other, (dict, Dict)):
            return Dict(*(self.items() + list(other.items())))
        raise TypeError(f'Addition not defined between type Dict and type {type(other)}!')
    def __eq__(self, other):
        if isinstance(other, Dict):
            for i in self.items():
                if i not in other.items():
                    return False
            return len(self.__items) == len(other.items())
        if isinstance(other, dict):
            for k, v in self.items():
                if k not in other.keys() or other.get(k) != v:
                    return False
            return len(self.__items) == len(other.items())
        return False
    def __str__(self):
        return '{' + ', '.join(f'{k}: {v}' for k, v in self.__items) + '}'
    def __repr__(self):
        return str(self)
class Node:
    def __init__(self, value):
        self.__value = value
    def value(self):
        return self.__value
    def copy(self):
        return Node(self.__value)
    def __bool__(self):
        return bool(self.__value)
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__value == other.__value
        return False
    def __str__(self):
        return '(' + str(self.__value) + ')'
    def __repr__(self):
        return str(self)
class Link:
    def __init__(self, node1: Node, node2: Node):
        self.__node1, self.__node2 = node1, node2
    def index(self, node: Node):
        if node in (self.__node1, self.__node2):
            return int(node == self.__node2)
        raise Exception('Node not present!')
    def other(self, node: Node):
        if node in [self.__node1, self.__node2]:
            return [self.__node1, self.__node2][node == self.__node1]
        raise ValueError('Unrecognized node!')
    def __contains__(self, item):
        return item in (self.__node1, self.__node2)
    def __len__(self):
        return 1 + (self.__node1 != self.__node2)
    def __getitem__(self, i: int):
        return [self.__node1, self.__node2][i % 2]
    def __eq__(self, other):
        if isinstance(other, Link):
            return (self.__node1, self.__node2) in [(other.__node1, other.__node2), (other.__node2, other.__node1)]
        return False
    def __str__(self):
        return f'{self.__node1}-{self.__node2}'
    def __repr__(self):
        return str(self)
class UndirectedGraph:
    def __init__(self, start: Node, *rest: Node):
        self.__nodes = []
        for n in (start,) + rest:
            if n not in self.__nodes:
                self.__nodes.append(n)
        self.__links, self.__neighboring, self.__degrees, self.__degrees_sum = [], Dict(*[(n, []) for n in self.__nodes]), Dict(*[(n, 0) for n in self.__nodes]), 0
    def nodes(self):
        return self.__nodes
    def links(self):
        return self.__links
    def neighboring(self, node: Node = None):
        if node is None:
            return self.__neighboring
        if isinstance(node, Node):
            if node in self.__nodes:
                return self.__neighboring[node]
            raise KeyError('No such node in the graph!')
        raise TypeError('Node expected!')
    def degrees(self, node: Node = None):
        if node is None:
            return self.__degrees
        if isinstance(node, Node):
            if node in self.__nodes:
                return self.__degrees[node]
            raise KeyError('No such node in the graph!')
        raise TypeError('Node expected!')
    def degrees_sum(self):
        return self.__degrees_sum
    def add_node(self, node: Node, *current_nodes: Node):
        if node not in self.__nodes:
            res = []
            for c in current_nodes:
                if c in self.__nodes and c not in res:
                    res.append(c)
            self.__degrees[node] = len(res)
            self.__degrees_sum += 2 * len(res)
            for old_node in res:
                self.__degrees[old_node] += 1
                self.__links.append(Link(old_node, node)), self.__neighboring[old_node].append(node)
            self.__nodes.append(node)
            self.__neighboring[node] = res
    def remove(self, node1: Node, *nodes: Node):
        for node in (node1,) + nodes:
            if node in self.__nodes:
                for n in self.__neighboring[node]:
                    self.__degrees[n] -= 1
                    self.__degrees_sum -= 2
                    self.__links.remove(Link(n, node)), self.__neighboring[n].remove(node)
                self.__nodes.remove(node), self.__degrees.pop(node), self.__neighboring.pop(node)
    def connect(self, node1: Node, node2: Node, *rest: Node):
        for current in [node2] + [*rest]:
            if Link(node1, current) not in self.__links and node1 != current and current in self.__nodes:
                self.__degrees[node1] += 1
                self.__degrees[current] += 1
                self.__degrees_sum += 2
                self.__neighboring[node1].append(current), self.__neighboring[current].append(node1), self.__links.append(Link(node1, current))
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        for n in [node2] + [*rest]:
            if Link(node1, n) in self.__links:
                self.__degrees[node1] -= 1
                self.__degrees[n] -= 1
                self.__degrees_sum -= 2
                self.__neighboring[node1].remove(n), self.__neighboring[n].remove(node1), self.__links.remove(Link(node1, n))
    def complementary(self):
        res = UndirectedGraph(*self.__nodes)
        for i, n in enumerate(self.__nodes):
            for j in range(i + 1, len(self.__nodes)):
                if Link(n, self.__nodes[j]) not in self.__links:
                    res.connect(n, self.__nodes[j])
        return res
    def copy(self):
        res = UndirectedGraph(*self.__nodes)
        for n in self.__nodes:
            if self.degrees(n):
                res.connect(n, *self.neighboring(n))
        return res
    def __connection_components(self, nodes: [Node] = None, links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if len(nodes) == 1:
            return [nodes]
        components, current, total, old = [[nodes[0]]], [nodes[0]], [nodes[0]], []
        while True:
            new = []
            for node in current:
                if node not in total:
                    total.append(node)
                    if len(total) == len(nodes):
                        components[-1] += new
                        return components
                for n in [m for m in self.__neighboring[node] if Link(node, m) in links]:
                    if n not in current and n not in old:
                        new.append(n), total.append(n)
                        if len(total) == len(nodes):
                            components[-1] += new
                            return components
                    old.append(n)
                old.append(node)
            components[-1] += new
            if not new:
                new = [[n for n in nodes if n not in total][0]]
                components.append(new)
            current = new.copy()
    def connection_components(self):
        return self.__connection_components()
    def __connected(self, nodes: [Node] = None, links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if len(links) < len(nodes) - 1:
            return False
        if len(links) > (len(nodes) - 1) * (len(nodes) - 2) / 2 or len(nodes) == 1:
            return True
        so_far, total = [nodes[0]], [nodes[0]]
        while True:
            for n in so_far:
                for m in [m for m in nodes if Link(m, n) in links]:
                    if m not in total:
                        total.append(m)
                        if len(total) == len(nodes):
                            return True
            if so_far == total:
                return False
            so_far = total.copy()
    def connected(self):
        return self.__connected()
    def tree(self):
        if len(self.__nodes) != len(self.__links) + 1:
            return False
        nodes, duplicates = [], []
        for l in self.__links:
            if l[0] not in nodes:
                nodes.append(l[0])
            else:
                duplicates.append(l[0])
                if l[1] in duplicates:
                    return False
            if l[1] not in nodes:
                nodes.append(l[1])
            else:
                duplicates.append(l[1])
                if l[0] in duplicates:
                    return False
        return True
    def __reachable(self, node1: Node, node2: Node, nodes: [Node] = None, links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            raise Exception('Unrecognized node(s).')
        if node1 == node2:
            return True
        total, so_far = [node1], [node1]
        while True:
            for m in so_far:
                for n in [n for n in nodes if Link(m, n) in links and n not in total]:
                    if n == node2:
                        return True
                    if n not in total:
                        total.append(n)
            if so_far == total:
                return False
            so_far = total.copy()
    def reachable(self, node1: Node, node2: Node):
        return self.__reachable(node1, node2)
    def __path_with_length(self, node1: Node, node2: Node, length: int, nodes: [Node] = None, links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if not self.__reachable(node1, node2, nodes, links):
            return False
        if not length:
            return (False, [])[node1 == node2]
        if length == 1:
            return (False, [Link(node1, node2)])[Link(node1, node2) in links]
        for n in [_n for _n in nodes if Link(node1, _n) in links]:
            res = self.__path_with_length(n, node2, length - 1, [_n for _n in nodes if _n != node1], [_l for _l in links if _l != Link(node1, n)])
            if isinstance(res, list):
                return [Link(node1, n)] + res
        return False
    def path_with_length(self, node1: Node, node2: Node, length: int):
        return self.__path_with_length(node1, node2, length)
    def __loop_with_length(self, length: int, nodes: [Node] = None, links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if length < 3:
            raise ValueError('No loop in an undirected graph with length less than 3 exists!')
        for n in nodes:
            for m in [_n for _n in self.neighboring(n) if _n in nodes]:
                res = self.__path_with_length(m, n, length - 1, nodes, [l for l in links if l != Link(m, n)])
                if res:
                    return [Link(n, m)] + res
        return []
    def loop_with_length(self, length: int):
        return self.__loop_with_length(length)
    def cliques(self, n: int):
        from itertools import permutations
        n = abs(n)
        if not n or n > len(self.__nodes):
            return []
        if n == 1:
            return [[_n] for _n in self.__nodes]
        if n == len(self.__nodes):
            return [[], [self.__nodes.copy()]][self.__full()]
        result = []
        for p in permutations(self.__nodes, n):
            can = True
            for i, _n in enumerate(p):
                for j in range(i + 1, len(p)):
                    if Link(_n, p[j]) not in self.__links:
                        can = False
                        break
                if not can:
                    break
            if can:
                exists = False
                for clique in result:
                    if all(_n in clique for _n in p):
                        exists = True
                        break
                if not exists:
                    result.append(list(p))
        return result
    def cut_nodes(self):
        c, cuts = len(self.__connection_components()), []
        for n in self.__nodes:
            if len(self.__connection_components([_n for _n in self.__nodes if _n != n], [l for l in self.__links if n not in l])) > c:
                cuts.append(n)
        return cuts
    def bridge_links(self):
        c, bridges = len(self.__connection_components()), []
        for l in self.__links:
            if len(self.__connection_components(links=[_l for _l in self.__links if _l != l])) > c:
                bridges.append(l)
        return bridges
    def __chromatic_number_nodes(self, nodes: [Node] = None, curr=0, so_far: [Node] = None, Except: [Node] = None):
        if len(self.__links) > 30:
            nodes = sorted(self.__nodes, key=lambda _n: self.__degrees[_n])
            colors, so_far, curr = Dict((nodes[0], 0)), [nodes[0]], [nodes[0]]
            while len(so_far) < len(nodes):
                new_curr = []
                for n in curr:
                    neighboring = [n for n in self.__neighboring[n] if n not in curr + so_far]
                    new_curr += neighboring.copy()
                    for m in neighboring:
                        so_far.append(m)
                        cols = [colors[_n] for _n in filter(lambda node: node in so_far, self.__neighboring[m])]
                        for i in range(len(cols) + 1):
                            if i not in cols:
                                colors[m] = i
                                break
                curr = new_curr.copy()
            return max(colors.values())
        if so_far is None:
            so_far = []
        if Except is None:
            Except = []
        if nodes is None:
            nodes = sorted(self.__nodes, key=lambda _n: self.__degrees[_n])
        if not nodes:
            return curr
        if self.__full(nodes, [l for l in self.__links if l[0] in nodes and l[1] in nodes]):
            return len(nodes) + curr
        curr_degrees = Dict(*[(n, 0) for n in nodes])
        for n in nodes:
            for m in nodes:
                if Link(n, m) in self.__links:
                    curr_degrees[n] += 1
        nodes = [nodes[0]] + sorted([_n for _n in nodes if _n != nodes[0]], key=lambda _n: curr_degrees[_n])
        so_far.append(nodes[0])
        rest = [_n for _n in nodes if _n not in self.__neighboring[nodes[0]] and _n != nodes[0] and _n not in Except]
        if not rest:
            _res = self.__chromatic_number_nodes([n for n in nodes if n not in so_far], curr + 1, so_far)
            so_far.pop()
            return _res
        res = len(self.__nodes)
        for n in rest:
            _res = self.__chromatic_number_nodes([n] + [_n for _n in nodes if _n not in (nodes[0], n)], curr, so_far, Except + [_n for _n in nodes if Link(nodes[0], _n) in self.__links or Link(n, _n) in self.__links])
            if n in so_far:
                so_far.remove(n)
            res = min(res, _res)
        return res
    def chromatic_number_nodes(self):
        return self.__chromatic_number_nodes()
    def chromatic_number_links(self):
        if not self.__links:
            return 0
        res_graph = UndirectedGraph(*[Node(l) for l in self.__links])
        for n in res_graph.nodes():
            for m in res_graph.nodes():
                if m != n and (n.value()[0] in m.value() or n.value()[1] in m.value()):
                    res_graph.connect(n, m)
        return res_graph.__chromatic_number_nodes()
    def planar(self):
        if len(self.__nodes) < 2 + bool(self.__links):
            return True
        if self.__connected():
            return (2 + bool(self.__loop_with_length(3))) * (len(self.__nodes) - 2) >= len(self.__links)
        for comp in self.__connection_components():
            curr = UndirectedGraph(*comp)
            for n in comp:
                for m in comp:
                    if Link(n, m) in self.__links:
                        curr.connect(n, m)
            if not curr.planar():
                return False
        return True
    def faces(self):
        if self.planar():
            if self.__connected():
                return len(self.__links) - len(self.__nodes) + 2
            total = 1
            for comp in self.__connection_components():
                curr = UndirectedGraph(*comp)
                for n in curr.nodes():
                    for m in curr.nodes():
                        if Link(m, n) in self.__links:
                            curr.connect(n, m)
                total += curr.faces() - 1
            return total
    def __full(self, nodes: [Node] = None, links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        return 2 * len(links) == len(nodes) * (len(nodes) - 1)
    def full(self):
        return self.__full()
    def get_shortest_path(self, node1: Node, node2: Node):
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        if Link(node1, node2) in self.__links:
            return [Link(node1, node2)]
        if not self.__reachable(node1, node2):
            return []
        paths = Dict(*[(n, None) for n in self.__nodes])
        paths[node2] = []
        for n in self.__neighboring[node2]:
            paths[n] = [Link(n, node2)]
        so_far, total = self.__neighboring[node2].copy(), self.__neighboring[node2].copy()
        while True:
            for m in so_far:
                for n in self.neighboring(m):
                    if paths[n] is None:
                        paths[n] = [Link(n, m)] + paths[m]
                    if n == node1:
                        return paths[n]
                    if n not in total:
                        total.append(n)
            so_far = total.copy()
    def shortest_path_length(self, node1: Node, node2: Node):
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        distances = Dict(*[(n, len(self.__nodes) - 1) for n in self.__nodes])
        distances[node2] = 0
        if not self.__reachable(node1, node2):
            return float('inf')
        if Link(node1, node2) in self.__links:
            return 1
        for n in self.__neighboring[node2]:
            distances[n] = 1
        so_far, total = self.__neighboring[node2].copy(), self.__neighboring[node2].copy()
        while True:
            for n in self.__nodes:
                for m in so_far:
                    if n in self.neighboring(m):
                        distances[n] = min(distances[n], distances[m] + 1)
                        if n == node1:
                            return distances[n]
                        if n not in total:
                            total.append(n)
            so_far = total.copy()
    def Euler_tour_exists(self):
        for node in self.__nodes:
            if self.__degrees[node] % 2:
                return False
        return True
    def __Euler_walk_exists(self, start: Node, end: Node, links=None):
        if links is None:
            links = self.__links
        temp_degrees = Dict(*[(n, sum([n in l for l in links])) for n in self.__nodes])
        for node in self.__nodes:
            if temp_degrees[node] % 2 and node not in [start, end]:
                return False
        return temp_degrees[start] % 2 + temp_degrees[end] % 2 == [2, 0][start == end]
    def Euler_walk_exists(self, start: Node, end: Node):
        return self.__Euler_walk_exists(start, end)
    def __Hamilton_tour_exists(self, nodes: [Node] = None, links: [Link] = None, can_continue_from: [Node] = None, can_end_in: [Node] = None, end_links: [Link] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = nodes
        if self.__full(nodes, links) or len(nodes) == 1:
            return True
        curr_degrees = Dict(*[(n, 0) for n in nodes])
        for n in nodes:
            for m in self.__neighboring[n]:
                curr_degrees[n] += Link(n, m) in links
        if any(curr_degrees[n] <= 1 for n in nodes) or not self.__connected(nodes, links):
            return False
        if can_end_in is not None:
            can_continue = False
            for n in [n for n in nodes if n not in can_continue_from + can_end_in]:
                for l in end_links:
                    if Link(n, l[0]) in links or Link(n, l[1]) in links:
                        can_continue = True
                        break
                if can_continue:
                    break
            if not can_continue:
                return False
        if len(nodes) > 2:
            if all(curr_degrees[n] >= len(nodes) / 2 for n in nodes) or len(links) > (len(nodes) - 1) * (len(nodes) - 2) / 2 + 1:
                return True
            res = True
            for n1 in nodes:
                for n2 in [n for n in nodes if n != n1 and Link(n1, n) not in links]:
                    if curr_degrees[n1] + curr_degrees[n2] < len(nodes):
                        res = False
                        break
                if not res:
                    break
            if res:
                return True
        for n in can_continue_from:
            if can_end_in is None:
                can_end_in = [m for m in nodes if Link(m, n) in links]
                end_links = [Link(n, m) for m in can_end_in]
                if not can_end_in:
                    continue
            if self.__Hamilton_tour_exists([_n for _n in nodes if _n != n], [l for l in links if n not in l], [_n for _n in nodes if _n in self.__neighboring[n]], can_end_in, end_links):
                return True
        return False
    def Hamilton_tour_exists(self):
        return self.__Hamilton_tour_exists()
    def __Hamilton_walk_exists(self, node1: Node, node2: Node = None, nodes: [Node] = None, links: [Link] = None, can_continue_from: [Node] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = [n for n in nodes if Link(node1, n) in links and n != node2]
        if not self.__connected(nodes, links):
            return False
        if self.__Hamilton_tour_exists(nodes, links, can_continue_from):
            return True
        if node2 is None:
            for n2 in [n for n in self.__nodes if n != node1]:
                if self.__Hamilton_walk_exists(node1, n2):
                    return True
            return False
        if len(nodes) == 1 and node1 == node2 or len(nodes) == 2 and Link(node1, node2) in links:
            return True
        if self.__loop_with_length(len(nodes), nodes, links + [Link(node1, node2)] * (Link(node1, node2) not in links)):
            return True
        for n in can_continue_from:
            if self.__Hamilton_walk_exists(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], [_n for _n in nodes if Link(_n, n) in links and _n not in [node1, node2]]):
                return True
        return False
    def Hamilton_walk_exists(self, node1: Node, node2: Node):
        return self.__Hamilton_walk_exists(node1, node2)
    def Euler_tour(self):
        if self.Euler_tour_exists():
            for n1 in self.__nodes:
                for n2 in self.__neighboring[n1]:
                    if self.__Euler_walk_exists(n1, n2):
                        return self.__Euler_walk(n1, n2, [l for l in self.__links if l != Link(n1, n2)]) + [Link(n1, n2)]
        return False
    def __Euler_walk(self, node1: Node, node2: Node, links: [Link] = None):
        if links is None:
            links = self.__links
        if node1 in self.__nodes and node2 in self.__nodes:
            if self.__Euler_walk_exists(node1, node2, links):
                if links == [Link(node1, node2)]:
                    return [Link(node1, node2)]
                for l in links:
                    if node1 in l:
                        res = self.__Euler_walk(l.other(node1), node2, [_l for _l in links if _l != l])
                        if res:
                            return [l] + res
            return False
        raise Exception('Unrecognized nodes!')
    def Euler_walk(self, node1: Node, node2: Node):
        return self.__Euler_walk(node1, node2)
    def Hamilton_tour(self):
        if any(self.__degrees[n] <= 1 for n in self.__nodes) or not self.__connected():
            return False
        for n1 in self.__nodes:
            for n2 in self.__neighboring[n1]:
                res = self.__Hamilton_walk(n1, n2)
                if res:
                    return res + [n1]
        return False
    def __Hamilton_walk(self, node1: Node, node2: Node | None, nodes: [Node] = None, links: [Link] = None, can_continue_from: [Node] = None, res_stack: [Node] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 in nodes and (node2 is None or node2 in nodes):
            if not self.__connected(nodes, links):
                return False
            if res_stack is None:
                res_stack = [node1]
            curr_degrees = Dict(*[(n, 0) for n in nodes])
            for n in nodes:
                for m in self.__neighboring[n]:
                    curr_degrees[n] += Link(n, m) in links
            if can_continue_from is None:
                can_continue_from = sorted((n for n in nodes if Link(node1, n) in links and n != node2), key=lambda x: curr_degrees[x])
            nodes_with_degree_1 = list(filter(lambda x: curr_degrees[x] == 1, curr_degrees.keys()))
            if len(nodes_with_degree_1) > (node1 in nodes_with_degree_1) + (node2 in nodes_with_degree_1) or len(nodes_with_degree_1) == 1 and nodes_with_degree_1[0] not in (node1, node2):
                return False
            if len(nodes_with_degree_1) == 1 and node1 not in nodes_with_degree_1:
                node2 = nodes_with_degree_1[0]
            if node2 is None:
                if len(nodes) == 1:
                    return nodes
            elif len(nodes) == 2 and Link(node1, node2) in links:
                return [node1, node2]
            for n in can_continue_from:
                res = self.__Hamilton_walk(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], sorted([_n for _n in nodes if Link(_n, n) in links and _n not in [node1, node2]], key=lambda x: self.__degrees[x]), [n])
                if res:
                    return res_stack + res
            return False
        raise ValueError('Unrecognized nodes!')
    def Hamilton_walk(self, node1: Node, node2: Node = None):
        return self.__Hamilton_walk(node1, node2)
    def isomorphic(self, other):
        if type(other) == UndirectedGraph:
            if self.__degrees_sum != other.__degrees_sum:
                return False
            if len(self.__nodes) != len(other.__nodes):
                return False
            this_degrees, other_degrees = dict(), dict()
            for d in self.__degrees.values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.__degrees.values():
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            if this_degrees != other_degrees:
                return False
            this_nodes_degrees, other_nodes_degrees = {d: [] for d in this_degrees.keys()}, {d: [] for d in other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.__nodes:
                    if self.__degrees[n] == d:
                        this_nodes_degrees[d].append(n)
                    if other.__degrees[n] == d:
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = cartesian_product(*_permutations)
            for possibility in possibilities:
                map_dict = Dict()
                for i, group in enumerate(possibility):
                    map_dict += Dict(*zip(group, other_nodes_degrees[i]))
                possible = True
                for n, v0 in map_dict.items():
                    for m, v1 in map_dict.items():
                        if (m in self.neighboring(n)) != (v1 in other.neighboring(v0)):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return True
            return False
        return False
    def __reversed__(self):
        return self.complementary()
    def __contains__(self, item):
        return item in self.__nodes + self.__links
    def __add__(self, other):
        if isinstance(other, UndirectedGraph):
            res = self.copy()
            res.__nodes += [n for n in other.nodes() if n not in self.__nodes]
            res.__links += [l for l in other.links() if l not in self.__links]
            res.__degrees_sum = 2 * len(res.links())
            for n in res.nodes():
                if n not in res.neighboring().keys():
                    res.__neighboring[n] = []
                for l in [l for l in res.links() if n in l]:
                    sec = l.other(n)
                    if sec not in res.neighboring(n):
                        res.__neighboring[n].append(sec)
            res.__degrees = Dict(*[(n, len(res.neighboring(n))) for n in res.nodes()])
            return res
        raise TypeError(f'Can\'t add class UndirectedGraph to class {type(other)}!')
    def __eq__(self, other):
        if isinstance(other, UndirectedGraph):
            for n in self.__nodes:
                if n not in other.nodes():
                    return False
            for l in self.__links:
                if l not in other.links():
                    return False
            return len(self.__links) == len(other.links()) and len(self.__nodes) == len(other.nodes())
        return False
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.__nodes) + '}, {' + ', '.join(str(l) for l in self.__links) + '})'
    def __repr__(self):
        return str(self)
class WeightedUndirectedGraph(UndirectedGraph):
    def __init__(self, start: Node, *rest: Node):
        super().__init__(start, *rest)
        self.__weights, self.__total_weight = Dict(*[(l, 0) for l in self.links()]), 0
    def weights(self, node1_or_link: (Node, Link) = None, node2: Node = None):
        if node1_or_link is None:
            return ', '.join([str(k) + ' -> ' + str(v) for k, v in self.__weights.items()])
        elif isinstance(node1_or_link, Node):
            if node2 is None:
                return ', '.join(str(Link(node1_or_link, n)) + ' -> ' + str(self.__weights[Link(node1_or_link, n)]) for n in self.neighboring(node1_or_link))
            if isinstance(node2, Node):
                if node2 in self.nodes():
                    if Link(node1_or_link, node2) in self.links():
                        return self.__weights[Link(node1_or_link, node2)]
                    raise KeyError(f'No link between {node1_or_link} and {node2}!')
                raise ValueError('No such node exists in this graph!')
            raise TypeError('Node expected!')
        elif isinstance(node1_or_link, Link):
            if node1_or_link in self.links():
                return self.__weights[node1_or_link]
            raise KeyError('Link not in graph!')
        raise TypeError('Node or link expected!')
    def total_weight(self):
        return self.__total_weight
    def add_node(self, node: Node, *nodes_values: tuple):
        if node not in self.nodes():
            res = []
            for n, v in nodes_values:
                if n in self.nodes() and n not in [p[0] for p in res]:
                    res.append((n, v))
            for n, v in res:
                if not isinstance(v, (int, float)):
                    raise TypeError('Real numerical values expected!')
            super().add_node(node, *[p[0] for p in res])
            for n, v in res:
                self.__weights[Link(node, n)] = v
                self.__total_weight += v
    def remove(self, node1: Node, *nodes: Node):
        super().remove(node1, *nodes)
        for node in (node1,) + nodes:
            for l in self.__weights.keys():
                if node in l:
                    self.__total_weight -= self.__weights[l]
                    self.__weights.pop(l)
    def connect(self, node1: Node, node2_and_value: (Node, float), *nodes_values: (Node, float)):
        if node1 in self.nodes():
            super().connect(node1, *[p[0] for p in [node2_and_value] + list(nodes_values)])
            for current, v in [node2_and_value] + list(nodes_values):
                if Link(node1, current) not in self.__weights:
                    self.__weights[Link(node1, current)] = v
                    self.__total_weight += v
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        super().disconnect(node1, node2, *rest)
        for n in [node2] + [*rest]:
            if Link(node1, n) in [l for l in self.__weights.keys()]:
                self.__total_weight -= self.__weights[Link(node1, n)]
                self.__weights.pop(Link(node1, n))
    def copy(self):
        res = WeightedUndirectedGraph(*self.nodes())
        for n in self.nodes():
            for m in self.nodes():
                if Link(n, m) in self.links():
                    res.connect(n, (m, self.weights(n, m)))
        return res
    def path_with_length(self, node1: Node, node2: Node, length: int):
        res = super().path_with_length(node1, node2, length)
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def loop_with_length(self, length: int):
        res = super().loop_with_length(length)
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def get_shortest_path(self, node1: Node, node2: Node):
        res = super().get_shortest_path(node1, node2)
        return res, sum(self.__weights[l] for l in res)
    def minimal_spanning_tree(self):
        if self.tree():
            return self.links(), self.__total_weight
        if not self.__connected():
            res = []
            for comp in self.connection_components():
                curr = WeightedUndirectedGraph(*comp)
                for n in comp:
                    for m in comp:
                        if m in self.neighboring(n):
                            curr.connect(n, (m, self.weights(n, m)))
                res.append(curr.minimal_spanning_tree())
            return res
        res_links, node_groups = [], []
        links = sorted((l for l in self.links()), key=lambda x: self.weights(x))
        for l in links:
            somewhere1, somewhere2 = False, False
            for first_nodes in node_groups:
                if l[0] in first_nodes and l[1] not in first_nodes:
                    first_nodes.append(l[1])
                    somewhere1 = True
                    res_links.append(l)
                elif l[1] in first_nodes and l[0] not in first_nodes:
                    first_nodes.append(l[0])
                    somewhere2 = True
                    res_links.append(l)
                elif all(n in first_nodes for n in l):
                    somewhere1, somewhere2 = True, True
                for second_nodes in node_groups:
                    if first_nodes != second_nodes:
                        if l[0] in first_nodes and l[1] in second_nodes or l[1] in first_nodes and l[0] in second_nodes:
                            for n in second_nodes:
                                if n not in first_nodes:
                                    first_nodes.append(n)
                            node_groups.remove(second_nodes)
                            break
            if not (somewhere1 or somewhere2):
                node_groups.append([*l]), res_links.append(l)
            if len(node_groups) == 1 and len(node_groups[0]) == len(self.nodes()):
                return res_links, sum(self.weights(l) for l in res_links)
        return res_links, sum(v for v in (self.weights(l) for l in res_links))
    def minimal_path(self, node1: Node, node2: Node):
        if node1 in self.nodes() and node2 in self.nodes():
            if self.__reachable(node1, node2):
                def DFS(curr_node, curr_path, total_negative, res_path=None):
                    if node1 == node2 and res_path is None:
                        res_path = [[], 0]
                    for n in [_ for _ in self.neighboring(curr_node) if Link(_, curr_node) not in curr_path[0]]:
                        if res_path is not None:
                            if curr_path[1] + self.weights(Link(n, curr_node)) + total_negative >= res_path[1]:
                                continue
                        if n == node2:
                            if res_path is None:
                                res_path = [curr_path[0].copy() + [Link(curr_node, n)], curr_path[1] + self.weights(Link(n, curr_node))]
                            elif curr_path[1] + self.weights(Link(curr_node, n)) < res_path[1]:
                                res_path[0], res_path[1] = curr_path[0].copy() + [Link(curr_node, n)], curr_path[1] + self.weights(Link(curr_node, n))
                        curr = DFS(n, [curr_path[0] + [Link(curr_node, n)], curr_path[1] + self.weights(Link(curr_node, n))], total_negative - self.weights(Link(curr_node, n)) * (self.weights(Link(curr_node, n)) < 0), res_path)
                        if curr is not None:
                            if res_path is None or curr[1] < res_path[1]:
                                res_path = curr
                    return res_path
                return DFS(node1, [[], 0], sum(sum(self.weights(n1, n2) for n2 in self.neighboring(n1) if self.weights(n1, n2) < 0) for n1 in self.nodes()) // 2)
            return [[], 0]
        raise ValueError('Unrecognized node(s)!')
    def Euler_tour(self):
        res = super().Euler_tour()
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def Euler_walk(self, node1: Node, node2: Node):
        res = super().Euler_walk(node1, node2)
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def Hamilton_tour(self):
        if any(self.__degrees[n] <= 1 for n in self.__nodes) or not self.__connected():
            return False
        for n1 in self.__nodes:
            for n2 in self.__neighboring[n1]:
                res = self.__Hamilton_walk(n1, n2)
                if res:
                    return res[0] + [n1], res[1] + sum(self.weights(res[0][i], res[0][i + 1]) for i in range(len(res[0]) - 1)) + self.weights(res[0][-1], res[0][0])
        return False
    def __Hamilton_walk(self, node1: Node, node2: Node | None, nodes: [Node] = None, links: [Link] = None, can_continue_from: [Node] = None, res_stack: [Node] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 in self.__nodes and (node2 is None or node2 in nodes):
            if not self.__connected(nodes, links):
                return False
            if res_stack is None:
                res_stack = [node1]
            curr_degrees = Dict(*[(n, 0) for n in nodes])
            for n in nodes:
                for m in self.__neighboring[n]:
                    curr_degrees[n] += Link(n, m) in links
            if can_continue_from is None:
                can_continue_from = sorted((n for n in nodes if Link(node1, n) in links and n != node2), key=lambda x: curr_degrees[x])
            nodes_with_degree_1 = list(filter(lambda x: curr_degrees[x] == 1, curr_degrees.keys()))
            if len(nodes_with_degree_1) > (node1 in nodes_with_degree_1) + (node2 in nodes_with_degree_1) or len(nodes_with_degree_1) == 1 and nodes_with_degree_1[0] not in (node1, node2):
                return False
            if len(nodes_with_degree_1) == 1 and node1 not in nodes_with_degree_1:
                node2 = nodes_with_degree_1[0]
            if node2 is None:
                if len(nodes) == 1:
                    return nodes, 0
            elif len(nodes) == 2 and Link(node1, node2) in links:
                return [node1, node2], self.__weights[Link(node1, node2)]
            for n in sorted([n for n in can_continue_from], key=lambda x: self.__weights[Link(node1, x)]):
                res = self.__Hamilton_walk(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], [_n for _n in nodes if Link(_n, n) in links and _n not in [node1, node2]], [n])
                if res:
                    return res_stack + res[0], res[1] + sum(self.weights(res[0][i], res[0][i + 1]) for i in range(len(res[0]) - 1))
            return False
        raise ValueError('Unrecognized nodes!')
    def Hamilton_walk(self, node1: Node, node2: Node = None):
        return self.__Hamilton_walk(node1, node2)
    def isomorphic(self, other):
        if type(other) == WeightedUndirectedGraph:
            if self.__degrees_sum != other.degrees_sum():
                return False
            if len(self.__nodes) != len(other.nodes()):
                return False
            this_degrees, other_degrees, this_weights, other_weights = dict(), dict(), dict(), dict()
            for d in self.__degrees.values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.__degrees.values():
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            for w in self.__weights.values():
                if w in this_weights:
                    this_weights[w] += 1
                else:
                    this_weights[w] = 1
            for w in other.__weights.values():
                if w in other_weights:
                    other_weights[w] += 1
                else:
                    other_weights[w] = 1
            if this_degrees != other_degrees or this_weights != other_weights:
                return False
            this_nodes_degrees, other_nodes_degrees = {d: [] for d in this_degrees.keys()}, {d: [] for d in other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.__nodes:
                    if self.__degrees[n] == d:
                        this_nodes_degrees[d].append(n)
                    if other.degrees(n) == d:
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = cartesian_product(*_permutations)
            for possibility in possibilities:
                map_dict = Dict()
                for i, group in enumerate(possibility):
                    map_dict += Dict(*zip(group, other_nodes_degrees[i]))
                possible = True
                for n, v0 in map_dict.items():
                    for m, v1 in map_dict.items():
                        if self.__weights[Link(n, m)] != other.__weights[Link(v0, v1)]:
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return True
            return False
        return False
    def __add__(self, other):
        if isinstance(other, WeightedUndirectedGraph):
            res = WeightedUndirectedGraph(*self.nodes() + other.nodes())
            for n in res.nodes():
                for m in res.nodes():
                    if Link(m, n) in self.links() + other.links():
                        if Link(m, n) in self.links():
                            weight = self.weights(m, n)
                            if Link(m, n) in other.links():
                                weight += other.weights(m, n)
                            res.connect(n, (m, weight))
                        else:
                            res.connect(n, (m, other.weights(m, n)))
            return res
        if isinstance(other, UndirectedGraph):
            res = WeightedUndirectedGraph(*self.nodes() + other.nodes())
            for n in res.nodes():
                for m in res.nodes():
                    if Link(m, n) in self.links() + other.links():
                        if Link(m, n) in self.links():
                            res.connect(n, (m, self.weights(m, n)))
                        else:
                            res.connect(n, (m, 0))
            return res
        raise TypeError(f'Can\'t add class WeightedUndirectedGraph to class {type(other)}!')
    def __eq__(self, other):
        if isinstance(other, WeightedUndirectedGraph):
            if len(self.nodes()) != len(other.nodes()) or self.__weights != other.__weights:
                return False
            for n in self.nodes():
                if n not in other.nodes():
                    return False
            return True
        if isinstance(other, UndirectedGraph):
            if len(self.links()) != len(other.links()) or len(self.nodes()) != len(other.nodes()):
                return False
            for n in self.nodes():
                if n not in other.nodes():
                    return False
            for l in self.links():
                if l not in other.links():
                    return False
            return True
        return False
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.nodes()) + '}, ' + str(self.__weights) + ')'
class DirectedGraph:
    def __init__(self, start: Node, *rest: Node):
        self.__nodes = []
        for n in (start,) + rest:
            if n not in self.__nodes:
                self.__nodes.append(n)
        self.__links, self.__degrees_sum, self.__degrees, self.__neighboring = [], 0, Dict(*[(n, [0, 0]) for n in self.__nodes]), Dict(*[(n, []) for n in self.__nodes])
    def nodes(self):
        return self.__nodes
    def links(self):
        return self.__links
    def degrees(self, node: Node = None):
        if node is None:
            return self.__degrees
        elif isinstance(node, Node):
            if node in self.__degrees:
                return self.__degrees[node]
            raise ValueError('No such node in the graph!')
        raise TypeError('Node expected!')
    def degrees_sum(self):
        return self.__degrees_sum
    def neighboring(self, node: Node = None):
        if node is None:
            return self.__neighboring
        if isinstance(node, Node):
            if node in self.__nodes:
                return self.__neighboring[node]
            raise ValueError('Node not in graph!')
        raise TypeError('Node expected!')
    def add_node(self, node: Node, pointed_by: iter, points_to: iter):
        if node not in self.__nodes:
            res_pointed_by, res_points_to = [], []
            for n in pointed_by:
                if n in self.__nodes and n not in res_pointed_by:
                    res_pointed_by.append(n)
            for n in points_to:
                if n in self.__nodes and n not in res_points_to:
                    res_points_to.append(n)
            self.__degrees[node], self.__neighboring[node] = [len(res_points_to), len(res_pointed_by)], []
            for n in res_pointed_by:
                self.__links.append((n, node)), self.__neighboring[n].append(node)
                self.__degrees[n][0] += 1
                self.__degrees_sum += 2
            for n in res_points_to:
                self.__links.append((node, n)), self.__neighboring[node].append(n)
                self.__degrees[n][1] += 1
                self.__degrees_sum += 2
            self.__nodes.append(node)
    def remove(self, node1: Node, *nodes: Node):
        for node in (node1,) + nodes:
            if node in self.__nodes:
                c = 0
                while c < len(self.__links):
                    link = self.__links[c]
                    if node in link:
                        sec = link.other(node)
                        if node == link[1]:
                            self.__neighboring[sec].remove(node)
                        self.__degrees[sec][link.index(sec)] -= 1
                        self.__links.remove(link)
                        self.__degrees_sum -= 2
                        c -= 1
                    c += 1
                self.__nodes.remove(node), self.__neighboring.pop(node), self.__degrees.pop(node)
    def connect_to_from(self, node1: Node, node2: Node, *rest: Node):
        if node1 in self.__nodes:
            for current in [node2] + list(rest):
                if (current, node1) not in self.__links and node1 != current and current in self.__nodes:
                    self.__links.append((current, node1)), self.__neighboring[current].append(node1)
                    self.__degrees[node1][1] += 1
                    self.__degrees[current][0] += 1
                    self.__degrees_sum += 2
    def connect_from_to(self, node1: Node, node2: Node, *rest: Node):
        if node1 in self.__nodes:
            for current in [node2] + list(rest):
                if (node1, current) not in self.__links and node1 != current and current in self.__nodes:
                    self.__links.append((node1, current)), self.__neighboring[node1].append(current)
                    self.__degrees[node1][0] += 1
                    self.__degrees[current][1] += 1
                    self.__degrees_sum += 2
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        for n in [node2] + [*rest]:
            if (node1, n) in self.__links:
                self.__degrees[node1][0] -= 1
                self.__degrees[n][1] -= 1
                self.__degrees_sum -= 2
                self.__links.remove((node1, n))
    def complementary(self):
        res = DirectedGraph(*self.__nodes)
        for i, n in enumerate(self.__nodes):
            for j in range(i + 1, len(self.__nodes)):
                if (n, self.__nodes[j]) not in self.__links:
                    res.connect_from_to(n, self.__nodes[j])
        return res
    def transposed(self):
        res = DirectedGraph(*self.__nodes)
        for l in self.__links:
            res.connect_to_from(*l)
        return res
    def copy(self):
        res = DirectedGraph(*self.__nodes)
        for n in self.__nodes:
            if self.degrees(n)[0]:
                res.connect_from_to(n, *self.neighboring(n))
        return res
    def __connected(self, nodes: [Node] = None, links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if len(links) < len(nodes) - 1:
            return False
        if len(links) > (len(nodes) - 1) * (len(nodes) - 2) or len(nodes) == 1:
            return True
        so_far, total = [nodes[0]], [nodes[0]]
        while True:
            for n in so_far:
                for m in [m for m in nodes if (m, n) in links or (n, m) in links]:
                    if m not in total:
                        total.append(m)
                        if len(total) == len(nodes):
                            return True
            if so_far == total:
                return False
            so_far = total.copy()
    def connected(self):
        return self.__connected()
    def __connection_components(self, nodes: [Node] = None, links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        components, current, total, old = [[nodes[0]]], [nodes[0]], [nodes[0]], []
        while True:
            new = []
            for node in current:
                if node not in total:
                    total.append(node)
                    if len(total) == len(nodes):
                        components[-1] += new
                        return components
                for n in [n for n in nodes if (node, n) in links or (n, node) in links]:
                    if n not in current and n not in old:
                        new.append(n), total.append(n)
                        if len(total) == len(nodes):
                            components[-1] += new
                            return components
                    old.append(n)
                old.append(node)
            components[-1] += new
            if not new:
                new = [[n for n in nodes if n not in total][0]]
                components.append(new)
            current = new.copy()
    def connection_components(self):
        return self.__connection_components()
    def __strongly_connected(self, nodes: [Node] = None, links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        for n in nodes:
            for m in [m for m in nodes if m != n]:
                if not self.__reachable(n, m, nodes, links):
                    return False
        return True
    def strongly_connected(self):
        return self.__strongly_connected()
    def __reachable(self, node1: Node, node2: Node, nodes: [Node] = None, links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            raise Exception('Unrecognized node(s).')
        total, so_far = [node1], [node1]
        while True:
            for m in so_far:
                for n in [n for n in nodes if (m, n) in links and n not in total]:
                    if n == node2:
                        return True
                    if n not in total:
                        total.append(n)
            if so_far == total:
                return False
            so_far = total.copy()
    def reachable(self, node1: Node, node2: Node):
        return self.__reachable(node1, node2)
    def __path_with_length(self, node1: Node, node2: Node, length: int, nodes: [Node] = None, links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            raise Exception('Unrecognized node(s).')
        if not self.__reachable(node1, node2, nodes, links) or length < 0:
            return False
        if not length:
            return (False, [])[node1 == node2]
        if length == 1:
            return (False, [(node1, node2)])[(node1, node2) in links]
        for n in [_n for _n in nodes if (node1, _n) in links]:
            res = self.__path_with_length(n, node2, length - 1, [_n for _n in nodes if _n != node1], [_l for _l in links if _l != (node1, n)])
            if isinstance(res, list):
                return [(node1, n)] + res
        return False
    def path_with_length(self, node1: Node, node2: Node, length: int):
        return self.__path_with_length(node1, node2, length)
    def __loop_with_length(self, length: int, nodes: [Node] = None, links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        for n in nodes:
            for l in [l for l in links if l[0] == n]:
                res = self.__path_with_length(l[1], n, length - 1, nodes, [_l for _l in links if _l != (l[1], n)])
                if isinstance(res, list):
                    return [l] + res
        return False
    def loop_with_length(self, length: int):
        return self.__loop_with_length(length)
    def cut_nodes(self):
        c, cuts = len(self.__connection_components()), []
        for n in self.__nodes:
            if len(self.__connection_components([_n for _n in self.__nodes if _n != n], [l for l in self.__links if n not in l])) > c:
                cuts.append(n)
        return cuts
    def bridge_links(self):
        c, bridges = len(self.__connection_components()), []
        for l in self.__links:
            if len(self.__connection_components(links=[_l for _l in self.__links if _l != l])) > c:
                bridges.append(l)
        return bridges
    def get_shortest_path(self, node1: Node, node2: Node):
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        if (node1, node2) in self.__links:
            return [(node1, node2)]
        if not self.__reachable(node1, node2):
            return False
        paths = Dict(*[(n, None) for n in self.__nodes])
        paths[node2] = []
        for l in [l for l in self.__links if node2 == l[1]]:
            paths[l[0]] = [(l[0], node2)]
        so_far = [n for n in self.__nodes if (n, node2) in self.__links]
        total = so_far.copy()
        while True:
            for m in so_far:
                for n in [n for n in self.__nodes if (n, m) in self.__links]:
                    if paths[n] is None:
                        paths[n] = [(n, m)] + paths[m]
                    if n == node1:
                        return paths[n]
                    if n not in total:
                        total.append(n)
            so_far = total.copy()
    def shortest_path_length(self, node1: Node, node2: Node):
        distances = Dict(*[(n, len(self.__links)) for n in self.__nodes])
        distances[node2] = 0
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        if (node1, node2) in self.__links:
            return 1
        if not self.__reachable(node1, node2):
            return float('inf')
        for l in [l for l in self.__links if node2 == l[1]]:
            distances[l[0]] = 1
        so_far = [n for n in self.__nodes if (n, node2) in self.__links]
        total = so_far.copy()
        while True:
            for n in self.__nodes:
                for m in so_far:
                    if (n, m) in self.__links:
                        distances[n] = min(distances[n], distances[m] + 1)
                        if n == node1:
                            return distances[n]
                        if n not in total:
                            total.append(n)
            so_far = total.copy()
    def Euler_tour_exists(self):
        for d in self.__degrees.values():
            if d[0] != d[1]:
                return False
        return self.__connected()
    def __Euler_walk_exists(self, start: Node, end: Node, links: [(Node, Node)] = None):
        if links is None:
            links = self.__links
        if self.Euler_tour_exists():
            return start == end
        temp_degrees = Dict(*[(n, [sum([n == l[0] for l in links]), sum([n == l[1] for l in links])]) for n in self.__nodes])
        for node in self.__nodes:
            if temp_degrees[node][0] % 2 and node != start or temp_degrees[node][1] % 2 and node != end:
                return False
        return temp_degrees[start][0] % 2 + temp_degrees[end][1] % 2 in [0, 2] and self.__connected()
    def Euler_walk_exists(self, start: Node, end: Node):
        return self.__Euler_walk_exists(start, end)
    def __Hamilton_tour_exists(self, nodes: [Node] = None, links: [(Node, Node)] = None, can_continue_from: [Node] = None, can_end_in: [Node] = None, end_links: [(Node, Node)] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = nodes
        curr_degrees = Dict(*[(n, [0, 0]) for n in nodes])
        for n in nodes:
            for l in links:
                curr_degrees[n][0] += n == l[0]
                curr_degrees[n][1] += n == l[1]
        if len(links) == len(nodes) ** 2 - len(nodes) or all(sum(curr_degrees[n]) >= len(can_continue_from) for n in can_continue_from):
            return True
        if can_end_in is not None:
            can_continue = False
            for n in nodes:
                if n in [l[1] for l in end_links]:
                    can_continue = True
                    break
            if not can_continue:
                return False
        if self.__strongly_connected(nodes, links):
            return True
        for n in can_continue_from:
            if can_end_in is None:
                can_end_in = [m for m in nodes if (m, n) in links]
                end_links = [(m, n) for m in can_end_in]
                if not can_end_in:
                    continue
            if self.__Hamilton_tour_exists([_n for _n in nodes if _n != n], [l for l in links if n not in l], [_n for _n in nodes if (n, _n) in links], can_end_in, end_links):
                return True
        return False
    def Hamilton_tour_exists(self):
        return self.__Hamilton_tour_exists()
    def __Hamilton_walk_exists(self, node1: Node, node2: Node | None, nodes: [Node] = None, links: [(Node, Node)] = None, can_continue_from: [Node] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = [n for n in nodes if (node1, n) in links]
        if not self.__connected(nodes, links):
            return False
        if self.__Hamilton_tour_exists(nodes, links, can_continue_from):
            return True
        if node2 is None:
            for n2 in [_n for _n in self.__nodes if _n != node1]:
                if self.__Hamilton_walk_exists(node1, n2):
                    return True
            return False
        if node2 in nodes:
            if self.__loop_with_length(len(nodes), nodes, links + [(node2, node1)] * ((node2, node1) not in links)) or len(nodes) == 1 and node1 == node2 or len(nodes) == 2 and (node1, node2) in links:
                return True
            for n in can_continue_from:
                if self.__Hamilton_walk_exists(n, node2, [m for m in nodes if m != node1], [l for l in links if node1 not in l], [m for m in nodes if (n, m) in links and m not in [node1, node2]]):
                    return True
            return False
        raise ValueError('Unrecognized node(s).')
    def Hamilton_walk_exists(self, node1: Node, node2: Node = None):
        return self.__Hamilton_walk_exists(node1, node2)
    def Euler_tour(self):
        if self.Euler_tour_exists():
            n1 = self.__nodes[0]
            for l in self.__links:
                if n1 == l[1]:
                    return self.__Euler_walk(n1, l[0], [_l for _l in self.__links if _l != l]) + [l]
        return False
    def __Euler_walk(self, node1: Node, node2: Node, links: [(Node, Node)] = None):
        if links is None:
            links = self.__links
        if node1 in self.__nodes and node2 in self.__nodes:
            if links == [(node1, node2)]:
                return links
            for l in links:
                if node1 == l[0] and self.__connected(self.__nodes, [_l for _l in links if _l != l]):
                    return [l] + self.__Euler_walk(l[1], node2, [_l for _l in links if _l != l])
        raise ValueError('Unrecognized nodes!')
    def Euler_walk(self, node1: Node, node2: Node):
        return self.__Euler_walk(node1, node2) if self.__Euler_walk_exists(node1, node2) else False
    def Hamilton_tour(self):
        if any(not self.__degrees[n][0] or not self.__degrees[n][1] for n in self.__nodes) or not self.__connected():
            return False
        for n1 in self.__nodes:
            for n2 in [_n for _n in self.__nodes if (_n, n1) in self.__links]:
                res = self.__Hamilton_walk(n1, n2)
                if res:
                    return res + [n1]
        return False
    def __Hamilton_walk(self, node1: Node, node2: Node | None, nodes: [Node] = None, links: [(Node, Node)] = None, can_continue_from: [Node] = None, res_stack: [Node] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 in nodes and (node2 is None or node2 in nodes):
            if not self.__connected(nodes, links):
                return False
            if res_stack is None:
                res_stack = [node1]
            curr_degrees = Dict()
            for n in nodes:
                curr_degrees[n] = [0, 0]
                for m in nodes:
                    if (n, m) in links:
                        curr_degrees[n][0] += 1
                        curr_degrees[m][1] += 1
                    elif (m, n) in links:
                        curr_degrees[n][1] += 1
                        curr_degrees[m][0] += 1
            if can_continue_from is None:
                can_continue_from = sorted((n for n in nodes if (node1, n) in links and n != node2), key=lambda x: (curr_degrees[x][1], curr_degrees[x][0]))
            for n in nodes:
                if not curr_degrees[n][0] and n != node2 or not curr_degrees[n][1] and n != node1:
                    return False
            if node2 is None:
                if len(nodes) == 1:
                    return nodes
            elif len(nodes) == 2 and (node1, node2) in links:
                return [node1, node2]
            for n in can_continue_from:
                res = self.__Hamilton_walk(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], sorted([_n for _n in nodes if (_n, n) in links and _n not in [node1, node2]], key=lambda x: self.__degrees[x][0]), [n])
                if res:
                    return res_stack + res
            return False
        raise ValueError('Unrecognized nodes!')
    def Hamilton_walk(self, node1: Node, node2: Node = None):
        return self.__Hamilton_walk(node1, node2)
    def isomorphic(self, other):
        if type(other) == DirectedGraph:
            if self.__degrees_sum != other.__degrees_sum:
                return False
            if len(self.__nodes) != len(other.__nodes):
                return False
            this_degrees, other_degrees = Dict(), Dict()
            for d in self.__degrees.values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.__degrees.values():
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            if this_degrees != other_degrees:
                return False
            this_nodes_degrees, other_nodes_degrees = Dict(*[(d, []) for d in this_degrees.keys()]), Dict(*[(d, []) for d in other_degrees.keys()])
            for d in this_degrees.keys():
                for n in self.__nodes:
                    if self.__degrees[n] == d:
                        this_nodes_degrees[d].append(n)
                    if other.__degrees[n] == d:
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = cartesian_product(*_permutations)
            for possibility in possibilities:
                map_dict = Dict()
                for i, group in enumerate(possibility):
                    map_dict += Dict(*zip(group, other_nodes_degrees[i]))
                possible = True
                for n, v0 in map_dict.items():
                    for m, v1 in map_dict.items():
                        if (m in self.neighboring(n)) != (v1 in other.neighboring(v0)):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return True
            return False
        return False
    def __reversed__(self):
        return self.complementary()
    def __contains__(self, item):
        return item in self.__nodes + self.__links
    def __add__(self, other):
        if isinstance(other, DirectedGraph):
            res = self.copy()
            res.__nodes += [n for n in other.nodes() if n not in self.__nodes]
            res.__links += [l for l in other.links() if l not in self.__links]
            for n in res.nodes():
                res.__degrees[n] = [0, 0]
                for l in [l for l in res.links() if n in l]:
                    res.__degrees[n][l.index(n)] += 1
            res.__degrees_sum = 2 * len(res.links())
            return res
        raise TypeError(f'Can\'t add class DirectedGraph to class {type(other)}!')
    def __eq__(self, other):
        if isinstance(other, DirectedGraph):
            if len(self.__links) != len(other.links()) or len(self.__nodes) != len(other.nodes()):
                return False
            for n in self.__nodes:
                if n not in other.nodes():
                    return False
            for l in self.__links:
                if l not in other.links():
                    return False
            return True
        return False
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.__nodes) + '}, {' + ', '.join(str(l[0]) + '->' + str(l[1]) for l in self.__links) + '})'
    def __repr__(self):
        return str(self)
class WeightedDirectedGraph(DirectedGraph):
    def __init__(self, start: Node, *rest: Node):
        super().__init__(start, *rest)
        self.__weights, self.__total_weight = Dict(*[(l, 0) for l in self.links()]), 0
    def weights(self, node1_or_link: Node | tuple = None, node2: Node = None):
        if node1_or_link is None:
            return ', '.join([str(k) + ' -> ' + str(v) for k, v in self.__weights.items()])
        elif isinstance(node1_or_link, Node):
            if node2 is None:
                return ', '.join(str((node1_or_link, n)) + ' -> ' + str(self.__weights[(node1_or_link, n)]) for n in [m for m in self.nodes() if (node1_or_link, m) in self.links()])
            if isinstance(node2, Node):
                if node2 in self.nodes():
                    if (node1_or_link, node2) in self.links():
                        return self.__weights[(node1_or_link, node2)]
                    raise KeyError(f'No link from {node1_or_link} to {node2}!')
                raise ValueError('No such node exists in this graph!')
            raise TypeError('Node expected!')
        elif isinstance(node1_or_link, tuple):
            if node1_or_link in self.links():
                return self.__weights[node1_or_link]
            raise KeyError('Link not in graph!')
        raise TypeError('Node or link expected!')
    def total_weight(self):
        return self.__total_weight
    def add_node(self, node: Node, pointed_by_values: iter, points_to_values: iter):
        if node not in self.nodes():
            for p in points_to_values + pointed_by_values:
                if len(p) < 2:
                    raise ValueError('Node-value pairs expected!')
            for v in [p[1] for p in pointed_by_values] + [p[1] for p in points_to_values]:
                if not isinstance(v, (int, float)):
                    raise TypeError('Real numerical values expected!')
            pointed_by_res, points_to_res = [], []
            for n, v in pointed_by_values:
                if n in self.nodes() and n not in [p[0] for p in pointed_by_res]:
                    pointed_by_res.append((n, v))
            for n, v in points_to_values:
                if n in self.nodes() and n not in [p[0] for p in points_to_res]:
                    points_to_res.append((n, v))
            super().add_node(node, [p[0] for p in pointed_by_res], [p[0] for p in points_to_res])
            for n, v in pointed_by_res:
                self.__weights[(n, node)] = v
                self.__total_weight += v
            for n, v in points_to_res:
                self.__weights[(node, n)] = v
                self.__total_weight += v
    def remove(self, node1: Node, *nodes: Node):
        super().remove(node1, *nodes)
        for node in (node1,) + nodes:
            for l in self.__weights.keys():
                if node in l:
                    self.__total_weight -= self.__weights[l]
                    self.__weights.pop(l)
    def connect_to_from(self, node1: Node, node2_and_value: (Node, float), *nodes_values: (Node, float)):
        if node1 in self.nodes():
            super().connect_to_from(node1, *[p[0] for p in [node2_and_value] + list(nodes_values)])
            for current, v in [node2_and_value] + list(nodes_values):
                if (current, node1) not in self.__weights:
                    self.__weights[(current, node1)] = v
                    self.__total_weight += v
    def connect_from_to(self, node1: Node, node2_and_value: (Node, float), *nodes_values: (Node, float)):
        if node1 in self.nodes():
            super().connect_from_to(node1, *[p[0] for p in [node2_and_value] + list(nodes_values)])
            for current, v in [node2_and_value] + list(nodes_values):
                if (node1, current) not in self.__weights:
                    self.__weights[(node1, current)] = v
                    self.__total_weight += v
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        super().disconnect(node1, node2, *rest)
        for n in [node2] + [*rest]:
            if (node1, n) in [l for l in self.__weights.keys()]:
                self.__total_weight -= self.__weights[(node1, n)]
                self.__weights.pop((node1, n))
    def copy(self):
        res = WeightedDirectedGraph(*self.nodes())
        for n in self.nodes():
            for m in self.nodes():
                if (n, m) in self.links():
                    res.connect_from_to(n, (m, self.weights(n, m)))
        return res
    def path_with_length(self, node1: Node, node2: Node, length: int):
        res = super().path_with_length(node1, node2, length)
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def loop_with_length(self, length: int):
        res = super().loop_with_length(length)
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def get_shortest_path(self, node1: Node, node2: Node):
        res = super().get_shortest_path(node1, node2)
        return res, sum(self.__weights[l] for l in res)
    def minimal_path(self, node1: Node, node2: Node):
        if node1 in self.nodes() and node2 in self.nodes():
            if self.__reachable(node1, node2):
                def DFS(curr_node, curr_path, total_negative, res_path=None):
                    if node1 == node2 and res_path is None:
                        res_path = [[], 0]
                    for n in [_ for _ in self.nodes() if (curr_node, _) in self.links() and (curr_node, _) not in curr_path[0]]:
                        if res_path is not None:
                            if curr_path[1] + self.weights((curr_node, n)) + total_negative >= res_path[1]:
                                continue
                        if n == node2:
                            if res_path is None:
                                res_path = [curr_path[0].copy() + [(curr_node, n)], curr_path[1] + self.weights((curr_node, n))]
                            elif curr_path[1] + self.weights((curr_node, n)) < res_path[1]:
                                res_path[0], res_path[1] = curr_path[0].copy() + [(curr_node, n)], curr_path[1] + self.weights((curr_node, n))
                        curr = DFS(n, [curr_path[0] + [(curr_node, n)], curr_path[1] + self.weights((curr_node, n))], total_negative - self.weights((curr_node, n)) * (self.weights((curr_node, n)) < 0), res_path)
                        if curr is not None:
                            if res_path is None or curr[1] < res_path[1]:
                                res_path = curr
                    return res_path
                return DFS(node1, [[], 0], sum((sum(self.weights(n1, n2) for n2 in [n for n in self.nodes() if (n, n1) in self.links()] if self.weights(n1, n2) < 0)) for n1 in self.nodes()))
            return [[], 0]
        raise ValueError('Unrecognized node(s)!')
    def Euler_tour(self):
        res = super().Euler_tour()
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def Euler_walk(self, node1: Node, node2: Node):
        res = super().Euler_walk(node1, node2)
        return (res, sum(self.__weights[l] for l in res)) if res else False
    def Hamilton_tour(self):
        if any(not self.__degrees[n][0] or not self.__degrees[n][1] for n in self.__nodes) or not self.__connected():
            return False
        for n1 in self.__nodes:
            for n2 in self.__neighboring[n1]:
                res = self.__Hamilton_walk(n1, n2)
                if res:
                    return res[0] + [n1], res[1] + sum(self.weights(res[0][i], res[0][i + 1]) for i in range(len(res[0]) - 1)) + self.weights(res[0][-1], res[0][0])
        return False
    def __Hamilton_walk(self, node1: Node, node2: Node | None, nodes: [Node] = None, links: [(Node, Node)] = None, can_continue_from: [Node] = None, res_stack: [Node] = None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 in self.__nodes and (node2 is None or node2 in nodes):
            if not self.__connected(nodes, links):
                return False
            if res_stack is None:
                res_stack = [node1]
            curr_degrees = Dict()
            for n in nodes:
                curr_degrees[n] = [0, 0]
                for m in nodes:
                    if (n, m) in links:
                        curr_degrees[n][0] += 1
                        curr_degrees[m][1] += 1
                    elif (m, n) in links:
                        curr_degrees[n][1] += 1
                        curr_degrees[m][0] += 1
            if can_continue_from is None:
                can_continue_from = sorted((n for n in nodes if (node1, n) in links and n != node2), key=lambda x: (curr_degrees[x][1], curr_degrees[x][0]))
            for n in nodes:
                if not curr_degrees[n][0] and n != node2 or not curr_degrees[n][1] and n != node1:
                    return False
            if node2 is None:
                if len(nodes) == 1:
                    return nodes, 0
            elif len(nodes) == 2 and (node1, node2) in links:
                return [node1, node2], self.__weights[(node1, node2)]
            for n in sorted([n for n in can_continue_from], key=lambda x: self.__weights[(node1, x)]):
                res = self.__Hamilton_walk(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], [_n for _n in nodes if (n, _n) in links and _n not in [node1, node2]], [n])
                if res:
                    return res_stack + res[0], res[1] + sum(self.weights(res[0][i], res[0][i + 1]) for i in range(len(res[0]) - 1))
            return False
    def Hamilton_walk(self, node1: Node, node2: Node = None):
        return self.__Hamilton_walk(node1, node2)
    def isomorphic(self, other):
        if type(other) == DirectedGraph:
            if self.__degrees_sum != other.__degrees_sum:
                return False
            if len(self.__nodes) != len(other.__nodes):
                return False
            this_degrees, other_degrees, this_weights, other_weights = Dict(), Dict(), dict(), dict()
            for d in self.__degrees.values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.__degrees.values():
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            for w in self.__weights.values():
                if w in this_weights:
                    this_weights[w] += 1
                else:
                    this_weights[w] = 1
            for w in other.__weights.values():
                if w in other_weights:
                    other_weights[w] += 1
                else:
                    other_weights[w] = 1
            if this_degrees != other_degrees or this_weights != other_weights:
                return False
            this_nodes_degrees, other_nodes_degrees = Dict(*[(d, []) for d in this_degrees.keys()]), Dict(*[(d, []) for d in other_degrees.keys()])
            for d in this_degrees.keys():
                for n in self.__nodes:
                    if self.__degrees[n] == d:
                        this_nodes_degrees[d].append(n)
                    if other.__degrees[n] == d:
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = cartesian_product(*_permutations)
            for possibility in possibilities:
                map_dict = Dict()
                for i, group in enumerate(possibility):
                    map_dict += Dict(*zip(group, other_nodes_degrees[i]))
                possible = True
                for n, v0 in map_dict.items():
                    for m, v1 in map_dict.items():
                        if self.__weights[(n, m)] != other.__weights[(v0, v1)]:
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return True
            return False
        return False
    def __add__(self, other):
        if isinstance(other, WeightedDirectedGraph):
            res = WeightedDirectedGraph(*self.nodes() + other.nodes())
            for n in res.nodes():
                for m in res.nodes():
                    if (n, m) in self.links() + other.links():
                        if (n, m) in self.links():
                            weight = self.weights(n, m)
                            if (n, m) in other.links():
                                weight += other.weights(n, m)
                            res.connect_from_to(n, (m, weight))
                        else:
                            res.connect_from_to(n, (m, other.weights(n, m)))
            return res
        if isinstance(other, DirectedGraph):
            res = WeightedDirectedGraph(*self.nodes() + other.nodes())
            for n in res.nodes():
                for m in res.nodes():
                    if (n, m) in self.links() + other.links():
                        if (n, m) in self.links():
                            res.connect_from_to(n, (m, self.weights(n, m)))
                        else:
                            res.connect_from_to(n, (m, 0))
            return res
        raise TypeError(f'Can\'t add class WeightedDirectedGraph to class {type(other)}!')
    def __eq__(self, other):
        if isinstance(other, WeightedDirectedGraph):
            if len(self.nodes()) != len(other.nodes()) or self.__weights != other.__weights:
                return False
            for n in self.nodes():
                if n not in other.nodes():
                    return False
            return True
        if isinstance(other, DirectedGraph):
            if len(self.links()) != len(other.links()) or len(self.nodes()) != len(other.nodes()):
                return False
            for n in self.nodes():
                if n not in other.nodes():
                    return False
            for l in self.links():
                if l not in other.links():
                    return False
            return True
        return False
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.nodes()) + '}, ' + f'{self.__weights}' + ')'
class Tree:
    def __init__(self, root: Node, *descendants: Node):
        self.__root = root
        if root in descendants:
            raise ValueError('Can\'t have a node twice in a tree!')
        for i in range(len(descendants)):
            for j in range(i + 1, len(descendants)):
                if descendants[i] == descendants[j]:
                    raise ValueError('Can\'t have a node twice in a tree!')
        self.__hierarchy, self.__nodes, self.__links, self.__leaves = Dict((self.__root, list(descendants))) + Dict(*[(n, []) for n in descendants]), [root, *descendants], [(root, n) for n in descendants], [*descendants] if descendants else [root]
    def root(self):
        return self.__root
    def nodes(self):
        return self.__nodes
    def links(self):
        return self.__links
    def leaves(self):
        return self.__leaves
    def hierarchy(self):
        return Dict(*filter(lambda p: p[1], self.__hierarchy.items()))
    def descendants(self, node: Node):
        return self.__hierarchy[node]
    def copy(self):
        res = Tree(self.root(), *self.descendants(self.__root))
        curr = self.descendants(res.__root)
        while True:
            new = []
            for n in curr:
                res_descendants = self.descendants(n)
                if res_descendants:
                    res.add_nodes_to(n, *res_descendants)
                new += self.descendants(n)
            if new:
                curr = new
            else:
                break
        return res
    def add_nodes_to(self, old: Node, new: Node, *rest: Node):
        if old not in self.__nodes:
            raise Exception('Node not found!')
        if old in self.__leaves:
            self.__leaves.remove(old)
        for n in [new] + [*rest]:
            if n not in self.nodes():
                self.__nodes.append(n), self.__hierarchy[old].append(n), self.__links.append((old, n)), self.__leaves.append(n)
                self.__hierarchy[n] = []
    def extend_tree_at(self, node: Node, tree):
        if node not in self.__nodes:
            raise Exception('Node not found!')
        if not isinstance(tree, Tree):
            raise TypeError('Tree expected!')
        self.add_nodes_to(node, tree.__root)
        current = [tree.__root]
        while True:
            new = []
            for c in current:
                res = list(filter(lambda n: n not in self.__nodes, tree.descendants(c)))
                if res:
                    self.add_nodes_to(c, *res)
                new += tree.descendants(c)
            if not new:
                break
            current = new.copy()
    def remove_node(self, node: Node):
        if node not in self.__nodes:
            raise ValueError('Node not in tree!')
        self.__nodes.remove(node)
        c, l = [n for n in self.__nodes if node in self.__hierarchy[n]][0], 0
        while l < len(self.__links):
            if node in self.__links[l]:
                self.__links.remove(self.__links[l])
                l -= 1
            l += 1
        self.__hierarchy[c] += self.__hierarchy[node]
        if node in self.__leaves:
            self.__leaves.remove(node)
            if not self.__hierarchy[c]:
                self.__leaves.append(c)
        self.__hierarchy.pop(node)
    def parent(self, node: Node):
        if node in self.__nodes:
            for l in self.__links:
                if node == l[1]:
                    return l[0]
        raise ValueError('Node not in tree!')
    def node_depth(self, node: Node):
        if node in self.__nodes:
            d = 0
            while node != self.__root:
                node = self.parent(node)
                d += 1
            return d
        raise ValueError('Node not in graph!')
    def height(self, curr_node: Node = None):
        if curr_node is None:
            curr_node = self.__root
        return 1 + max([0, *map(self.height, self.descendants(curr_node))])
    def path_to(self, node: Node, curr_root: Node = None):
        if curr_root is None:
            curr_root = self.__root
        if curr_root == node:
            return [node]
        if curr_root in self.__leaves:
            return
        for n in self.descendants(curr_root):
            res = self.path_to(node, n)
            if res:
                return [curr_root] + res
    def isomorphic(self, other):
        if isinstance(other, Tree):
            if len(self.__nodes) != len(other.__nodes) or len(self.__links) != len(other.__links) or len(self.leaves()) != len(other.leaves()) or len(self.descendants(self.__root)) != len(other.descendants(other.root())):
                return False
            this_hierarchies, other_hierarchies = dict(), dict()
            for n in self.__nodes:
                descendants = len(self.descendants(n))
                if descendants not in this_hierarchies:
                    this_hierarchies[descendants] = 1
                else:
                    this_hierarchies[descendants] += 1
            for n in other.__nodes:
                descendants = len(other.descendants(n))
                if descendants not in other_hierarchies:
                    other_hierarchies[descendants] = 1
                else:
                    other_hierarchies[descendants] += 1
            if this_hierarchies != other_hierarchies:
                return False
            this_nodes_descendants, other_nodes_descendants = {d: [] for d in this_hierarchies.keys()}, {d: [] for d in other_hierarchies.keys()}
            for n in self.__nodes:
                this_nodes_descendants[len(self.descendants(n))].append(n)
            for n in other.__nodes:
                other_nodes_descendants[len(self.descendants(n))].append(n)
            this_nodes_descendants, other_nodes_descendants = list(sorted(this_nodes_descendants.values(), key=lambda x: len(x))), list(sorted(other_nodes_descendants.values(), key=lambda x: len(x)))
            from itertools import permutations
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_descendants]
            possibilities = cartesian_product(*_permutations)
            for possibility in possibilities:
                map_dict = Dict()
                for i, group in enumerate(possibility):
                    map_dict += Dict(*zip(group, other_nodes_descendants[i]))
                possible = True
                for n, v0 in map_dict.items():
                    for m, v1 in map_dict.items():
                        if ((n, m) in self.links()) != ((v0, v1) in other.links()) or ((m, n) in self.links()) != ((v1, v0) in other.links()):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return True
            return False
        return False
    def __contains__(self, item):
        return item in self.__nodes + self.__links
    def __eq__(self, other):
        for n in self.nodes():
            if n not in other.nodes():
                return False
        if len(self.__nodes) != len(other.__nodes):
            return False
        for n in self.__nodes:
            if len(self.__hierarchy[n]) != len(other.__hierarchy[n]):
                return False
            for m in self.__hierarchy[n]:
                if m not in other.__hierarchy[n]:
                    return False
            return True
    def __str__(self):
        return '\n'.join(str(k) + ' -- ' + str(v) for k, v in filter(lambda p: p[1], self.__hierarchy.items()))
    def __repr__(self):
        return str(self)
