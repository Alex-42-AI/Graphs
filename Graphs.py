class Dict:
    def __init__(self, *args: tuple):
        self.__items = []
        for arg in args:
            if arg not in self.__items:
                self.__items.append(arg)
                if len(arg) != 2:
                    raise ValueError('Pairs of keys and values expected!')
        for i, item1 in enumerate(self.__items):
            for item2 in self.__items[i + 1:]:
                if item1[0] == item2[0]:
                    raise KeyError('No similar keys in a dictionary allowed!')
    def keys(self):
        return [p[0] for p in self.__items]
    def values(self):
        return [p[1] for p in self.__items]
    def items(self):
        return self.__items
    def pop(self, item):
        for i in self.__items:
            if item == i[0]:
                self.__items.remove(i)
                return i[1]
        raise KeyError(item)
    def popitem(self):
        if not self.items():
            raise IndexError('Can\'t pop from an empty dictionary!')
        res = self.__items[-1]
        self.__items.pop()
        return res
    def copy(self):
        return Dict(*self.__items)
    def __len__(self):
        return len(self.__items)
    def __getitem__(self, item):
        for k, v in self.__items:
            if item == k:
                return v
    def __setitem__(self, key, value):
        for i in range(len(self.__items)):
            if key == self.__items[i][0]:
                self.__items[i] = (key, value)
                return
        self.__items.append((key, value))
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
            return len(self.items()) == len(other.items())
        return False
    def __str__(self):
        return '{' + ', '.join(f'{k}: {v}' for k, v in self.__items) + '}'
    def __repr__(self):
        return str(self)
class Node:
    def __init__(self, value):
        self.value = value
    def copy(self):
        return Node(self.value)
    def __bool__(self):
        return bool(self.value)
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        return False
    def __str__(self):
        return '(' + str(self.value) + ')'
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
        raise Exception('Unrecognized node!')
    def __contains__(self, item):
        return item in [self.__node1, self.__node2]
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
        for i, n in enumerate(rest):
            if start == n:
                raise ValueError('Can\'t have a node twice in a graph.')
            for m in range(i + 1, len(rest)):
                if n == rest[m]:
                    raise ValueError('Can\'t have a node twice in a graph.')
        self.__nodes = [start, *rest]
        self.__links, self.__neighboring, self.__degrees, self.__degrees_sum = [], Dict(*[(n, []) for n in self.__nodes]), Dict(*[(n, 0) for n in self.__nodes]), 0
    def get_nodes(self):
        return self.__nodes
    def get_links(self):
        return self.__links
    def get_neighboring(self, node=None):
        if node is None:
            return self.__neighboring
        if isinstance(node, Node):
            try:
                return self.__neighboring[node]
            except KeyError:
                raise KeyError('No such node in the graph!')
        raise TypeError('Node expected!')
    def get_degrees(self, node=None):
        if node is None:
            return self.__degrees
        if isinstance(node, Node):
            try:
                return self.__degrees[node]
            except KeyError:
                raise KeyError('No such node in the graph!')
        raise TypeError('Node expected!')
    def get_degrees_sum(self):
        return self.__degrees_sum
    def add_node(self, node: Node, *current_nodes: Node):
        if node not in self.__nodes:
            res = []
            for c in current_nodes:
                if c in self.__nodes and c != node and c not in res:
                    res.append(c)
            current_nodes = res
            self.__degrees[node] = len(current_nodes)
            self.__degrees_sum += 2 * len(current_nodes)
            for old_node in current_nodes:
                self.__degrees[old_node] += 1
                self.__links.append(Link(old_node, node))
                self.__neighboring[old_node].append(node)
            self.__nodes.append(node)
            self.__neighboring[node] = list(current_nodes)
    def remove_node(self, node: Node):
        if node not in self.__nodes:
            raise Exception('Node not found.')
        for n in self.__neighboring[node]:
            self.__degrees[n] -= 1
            self.__degrees_sum -= 2
            self.__links.remove(Link(n, node)), self.__neighboring[n].remove(node)
        self.__nodes.remove(node), self.__degrees.pop(node), self.__neighboring.pop(node)
    def connect(self, node1: Node, node2: Node, *rest: Node):
        for current in [node2] + [*rest]:
            if Link(node1, current) not in self.__links and node1 != current:
                self.__degrees[node1] += 1
                self.__degrees[current] += 1
                self.__degrees_sum += 2
                self.__neighboring[node1].append(current)
                self.__neighboring[current].append(node1)
                self.__links.append(Link(node1, current))
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        for n in [node2] + [*rest]:
            if Link(node1, n) in self.__links:
                self.__degrees[node1] -= 1
                self.__degrees[n] -= 1
                self.__degrees_sum -= 2
                self.__neighboring[node1].remove(n)
                self.__neighboring[n].remove(node1)
                self.__links.remove(Link(node1, n))
    def copy(self):
        res = UndirectedGraph(*self.__nodes)
        res.__links, res.__neighboring, res.__degrees, res.__degrees_sum = self.__links.copy(), self.__neighboring.copy(), self.__degrees.copy(), self.__degrees_sum
        return res
    def connection_components(self, nodes=None, links=None):
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
    def connected(self, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if len(links) < len(nodes) - 1:
            return False
        return len(self.connection_components(nodes, links)) == 1
    def tree(self):
        if not self.connected() or len(self.__nodes) != len(self.__links) + 1:
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
    def reachable(self, node1: Node, node2: Node, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            raise Exception('Unrecognized node(s).')
        for comp in self.connection_components(nodes, links):
            if node1 in comp:
                return node2 in comp
    def path_with_length(self, node1: Node, node2: Node, length: int, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            if node1 not in self.__nodes or node2 not in self.__nodes:
                raise Exception('Unrecognized node(s).')
            return False
        if not self.reachable(node1, node2, nodes, links):
            return False
        if not length:
            return [False, []][node1 == node2]
        if Link(node1, node2) in links and length == 1:
            return [Link(node1, node2)]
        All = []
        for l in [l for l in links if node1 in l]:
            sec = l.other(node1)
            if sec in nodes:
                if self.reachable(sec, node2, nodes, [L for L in links if L != l]):
                    res = self.path_with_length(sec, node2, length - 1, [n for n in nodes if n != node1], [L for L in links if L != l])
                    if res:
                        All.append([l] + res)
        for path in All:
            if len(path) == length:
                return path
        return False
    def loop_with_length(self, length: int, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if length < 3:
            raise ValueError('No loop in an undirected graph with length less than 3 exists!')
        for n in nodes:
            for m in [_n for _n in self.get_neighboring(n) if _n in nodes]:
                res = self.path_with_length(m, n, length - 1, nodes, [l for l in links if l != Link(m, n)])
                if res:
                    return [Link(n, m)] + res
        return False
    def holes_in_surface(self):
        if self.connected():
            i, v, loop_3 = 0, 2, bool(self.loop_with_length(3))
            while True:
                if (v + loop_3) * (len(self.__nodes) - 2) >= len(self.__links):
                    return i
                i += 1
                v += 2
        Max = 0
        for comp in self.connection_components():
            curr = UndirectedGraph(*comp)
            for n in curr.get_nodes():
                for m in curr.get_nodes():
                    if Link(m, n) in self.__links:
                        curr.connect(n, m)
            Max = max(Max, curr.holes_in_surface())
        return Max
    def planar(self):
        return not self.holes_in_surface()
    def faces(self):
        if self.connected():
            return len(self.__links) - len(self.__nodes) + 2 - 2 * self.holes_in_surface()
        total = 0
        for comp in self.connection_components():
            curr = UndirectedGraph(*comp)
            for n in curr.get_nodes():
                for m in curr.get_nodes():
                    if Link(m, n) in self.__links:
                        curr.connect(n, m)
            total += curr.faces() - 1
        return total
    def full(self, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        return 2 * len(links) == len(nodes) * (len(nodes) - 1)
    def get_shortest_path(self, node1: Node, node2: Node):
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        if Link(node1, node2) in self.__links:
            return [Link(node1, node2)]
        if not self.reachable(node1, node2):
            return False
        paths = Dict(*[(n, None) for n in self.__nodes])
        paths[node2] = []
        for n in self.__neighboring[node2]:
            paths[n] = [Link(n, node2)]
        so_far, total = self.__neighboring[node2].copy(), self.__neighboring[node2].copy()
        while True:
            for m in so_far:
                for n in self.get_neighboring(m):
                    try:
                        if len(paths[n]) > len(paths[m]) + 1:
                            paths[n] = [Link(n, m)] + paths[m]
                    except TypeError:
                        paths[n] = [Link(n, m)] + paths[m]
                    if n == node1:
                        return paths[n]
                    if n not in total:
                        total.append(n)
            if so_far == total:
                break
            so_far = total.copy()
    def shortest_path_length(self, node1: Node, node2: Node):
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        distances = Dict(*[(n, len(self.__nodes) - 1) for n in self.__nodes])
        distances[node2] = 0
        if not self.reachable(node1, node2):
            return float('inf')
        if Link(node1, node2) in self.__links:
            return 1
        for n in self.__neighboring[node2]:
            distances[n] = 1
        so_far = self.__neighboring[node2].copy()
        total = so_far.copy()
        while True:
            for n in self.__nodes:
                for m in so_far:
                    if n in self.get_neighboring(m):
                        distances[n] = min(distances[n], distances[m] + 1)
                        if n == node1:
                            return distances[n]
                        if n not in total:
                            total.append(n)
            if so_far == total:
                break
            so_far = total.copy()
    def Euler_tour_exists(self):
        return not any(self.__degrees[node] % 2 for node in self.__nodes)
    def Euler_walk_exists(self, start: Node, end: Node, links=None):
        if links is None:
            links = self.__links
        temp_degrees = Dict(*[(n, sum([n in l for l in links])) for n in self.__nodes])
        for node in self.__nodes:
            if temp_degrees[node] % 2 and node not in [start, end]:
                return False
        return temp_degrees[start] % 2 + temp_degrees[end] % 2 in [0, 2]
    def Hamilton_tour_exists(self, nodes=None, links=None, can_continue_from=None, can_end_in=None, end_links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = nodes
        if self.full(nodes, links) or len(nodes) == 1:
            return True
        curr_degrees = Dict(*[(n, 0) for n in nodes])
        for n in nodes:
            for m in self.__neighboring[n]:
                curr_degrees[n] += Link(n, m) in links
        if any(curr_degrees[n] <= 1 for n in nodes) or not self.connected(nodes, links):
            return False
        if can_end_in is not None:
            can_continue = False
            for n in nodes:
                if n in can_end_in:
                    can_continue = True
                    break
                if can_continue:
                    break
            if not can_continue:
                return False
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
            if self.Hamilton_tour_exists([_n for _n in nodes if _n != n], [l for l in links if n not in l], [_n for _n in nodes if _n in self.__neighboring[n]], can_end_in, end_links):
                return True
        return False
    def Hamilton_walk_exists(self, node1: Node, node2=None, nodes=None, links=None, can_continue_from=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = [n for n in nodes if Link(node1, n) in links and n != node2]
        if not self.connected(nodes, links):
            return False
        if self.Hamilton_tour_exists(nodes, links, can_continue_from):
            return True
        if node2 is None:
            for n2 in [n for n in self.__nodes if n != node1]:
                if self.Hamilton_walk_exists(node1, n2):
                    return True
            return False
        if len(nodes) == 1 and node1 == node2 or len(nodes) == 2 and Link(node1, node2) in links:
            return True
        if self.loop_with_length(len(nodes), nodes, links + [Link(node1, node2)] * (Link(node1, node2) not in links)):
            return True
        for n in can_continue_from:
            if self.Hamilton_walk_exists(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], [_n for _n in nodes if Link(_n, n) in links and _n not in [node1, node2]]):
                return True
        return False
    def Euler_tour(self):
        if self.Euler_tour_exists():
            for n1 in self.__nodes:
                for n2 in self.__neighboring[n1]:
                    res = self.Euler_walk(n1, n2, [l for l in self.__links if l != Link(n1, n2)])
                    return res + [Link(n1, n2)]
        return []
    def Euler_walk(self, node1: Node, node2: Node, links=None):
        if links is None:
            links = self.__links
        if node1 in self.__nodes and node2 in self.__nodes:
            if self.Euler_walk_exists(node1, node2, links):
                if links == [Link(node1, node2)]:
                    return [Link(node1, node2)]
                for l in links:
                    if node1 in l:
                        res = self.Euler_walk(l.other(node1), node2, [_l for _l in links if _l != l])
                        if res:
                            return [l] + res
            return []
        raise Exception('Unrecognized nodes!')
    def Hamilton_tour(self):
        for n1 in self.__nodes:
            for n2 in self.__neighboring[n1]:
                res = self.Hamilton_walk(n1, n2)
                if res:
                    return res
        return []
    def Hamilton_walk(self, node1: Node, node2=None, nodes=None, links=None, can_continue_from=None, res_stack=None):
        if node1 in self.__nodes and (node2 is None or node2 in self.__nodes):
            if nodes is None:
                nodes = self.__nodes
            if links is None:
                links = self.__links
            if res_stack is None:
                res_stack = [node1]
            if can_continue_from is None:
                can_continue_from = [n for n in nodes if Link(node1, n) in links and n != node2]
            if node2 is None:
                if len(nodes) == 1:
                    return nodes
                for n2 in [n for n in nodes if n != node1]:
                    res = self.Hamilton_walk(node1, n2)
                    if res:
                        return res
            else:
                if len(nodes) == 2 and Link(node1, node2) in links:
                    return [node1, node2]
            for n in can_continue_from:
                if node2 is None or n != node2:
                    res = self.Hamilton_walk(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], [_n for _n in nodes if Link(_n, n) in links and _n not in [node1, node2]], [n])
                    if res:
                        return res_stack + res
            return []
        raise ValueError('Unrecognized nodes!')
    def __add__(self, other):
        res = self.copy()
        res.__nodes += [n for n in other.get_nodes() if n not in self.get_nodes()]
        res.__links += [l for l in other.get_links() if l not in self.__links]
        res.__degrees_sum = 2 * len(res.get_links())
        for n in res.get_nodes():
            if n not in res.get_neighboring().keys():
                res.__neighboring[n] = []
            for l in [l for l in res.get_links() if n in l]:
                sec = l.other(n)
                if sec not in res.get_neighboring(n):
                    res.__neighboring[n].append(sec)
        res.__degrees = Dict(*[(n, len(res.get_neighboring(n))) for n in res.get_nodes()])
        return res
    def __eq__(self, other):
        for n in self.__nodes:
            if n not in other.get_nodes():
                return False
        for l in self.get_links():
            if l not in other.get_links():
                return False
        return len(self.get_links()) == len(other.get_links()) and len(self.get_nodes()) == len(other.get_nodes())
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.__nodes) + '}, {' + ', '.join(str(l) for l in self.__links) + '})'
    def __repr__(self):
        return str(self)
class WeightedUndirectedGraph(UndirectedGraph):
    def __init__(self, start: Node, *rest: Node):
        super().__init__(start, *rest)
        self.__weights, self.__total_weight = Dict(*[(l, 0) for l in self.get_links()]), 0
    def get_weights(self, node1_or_link=None, node2=None):
        if node1_or_link is None:
            return ', '.join([str(k) + ' -> ' + str(v) for k, v in self.__weights.items()])
        elif isinstance(node1_or_link, Node):
            if node2 is None:
                return ', '.join(str(Link(node1_or_link, n)) + ' -> ' + str(self.__weights[Link(node1_or_link, n)]) for n in self._UndirectedGraph__neighboring[node1_or_link])
            if isinstance(node2, Node):
                if node2 in self.get_nodes():
                    if Link(node1_or_link, node2) in self.get_links():
                        return self.__weights[Link(node1_or_link, node2)]
                    raise KeyError(f'No link between {node1_or_link} and {node2}!')
                raise ValueError('No such node exists in this graph!')
            raise TypeError('Node expected!')
        elif isinstance(node1_or_link, Link):
            if node1_or_link in self.get_links():
                return self.__weights[node1_or_link]
            raise KeyError('Link not in graph!')
        raise TypeError('Node or link expected!')
    def get_total_weight(self):
        return self.__total_weight
    def add_node(self, node: Node, *nodes_values: tuple):
        if node in self.get_nodes():
            raise Exception('Node already in graph.')
        for n, v in nodes_values:
            if type(v) not in [int, float]:
                raise TypeError('Real numerical value expected!')
        res = []
        for n, v in nodes_values:
            if n in self.get_nodes() and n not in [p[0] for p in res]:
                res.append((n, v))
        self._UndirectedGraph__degrees[node] = len(nodes_values)
        self._UndirectedGraph__degrees_sum += 2 * len(nodes_values)
        for n, v in nodes_values:
            self._UndirectedGraph__degrees[n] += 1
            self._UndirectedGraph__links.append(Link(n, node))
            self._UndirectedGraph__neighboring[n].append(node)
            self.__weights[Link(node, n)] = v
            self.__total_weight += v
        self._UndirectedGraph__nodes.append(node)
        self._UndirectedGraph__neighboring[node] = list(p[0] for p in nodes_values)
    def remove_node(self, node: Node):
        if node not in self.get_nodes():
            raise Exception('Node not found.')
        for n in self.get_neighboring(node):
            self._UndirectedGraph__degrees[n] -= 1
            self._UndirectedGraph__degrees_sum -= 2
            self._UndirectedGraph__links.remove(Link(n, node))
            self._UndirectedGraph__neighboring[n].remove(node)
            self.__total_weight -= self.__weights[Link(node, n)]
            self.__weights.pop(Link(node, n))
        self._UndirectedGraph__nodes.remove(node)
        self._UndirectedGraph__degrees.pop(node)
        self._UndirectedGraph__neighboring.pop(node)
    def connect(self, node1: Node, node2_and_value: tuple, *nodes_values: tuple):
        if node1 in self.get_nodes():
            for n, v in [node2_and_value] + list(nodes_values):
                if type(v) not in [int, float]:
                    raise TypeError('Real numerical value expected!')
            res = []
            for n, v in [node2_and_value] + list(nodes_values):
                if n not in [p[0] for p in res] and n in self.get_nodes():
                    res.append((n, v))
            for current, v in [node2_and_value] + list(nodes_values):
                if Link(node1, current) not in self.get_links() and node1 != current:
                    self._UndirectedGraph__degrees[node1] += 1
                    self._UndirectedGraph__degrees[current] += 1
                    self._UndirectedGraph__degrees_sum += 2
                    self._UndirectedGraph__links.append(Link(node1, current)), self._UndirectedGraph__neighboring[node1].append(current), self._UndirectedGraph__neighboring[current].append(node1)
                    self.__weights[Link(node1, current)] = v
                    self.__total_weight += v
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        for n in [node2] + [*rest]:
            if Link(node1, n) in self.__links:
                self._UndirectedGraph__degrees[node1] -= 1
                self._UndirectedGraph__degrees[n] -= 1
                self._UndirectedGraph__degrees_sum -= 2
                self._UndirectedGraph__neighboring[node1].remove(n)
                self._UndirectedGraph__neighboring[n].remove(node1)
                self._UndirectedGraph__links.remove(Link(node1, n))
                self.__total_weight -= self.__weights[Link(node1, n)]
                self.__weights.pop(Link(node1, n))
    def copy(self):
        res = WeightedUndirectedGraph(*self.get_nodes())
        for n in self.get_nodes():
            for m in self.get_nodes():
                if Link(n, m) in self.get_links():
                    res.connect(n, (m, self.get_weights(n, m)))
        return res
    def minimal_spanning_tree(self):
        if self.tree():
            return self.get_links(), self.__total_weight
        if not self.connected():
            res = []
            for comp in self.connection_components():
                curr = WeightedUndirectedGraph(*comp)
                for n in curr.get_nodes():
                    for m in curr.get_nodes():
                        if m in self.get_neighboring(m):
                            curr.connect(n, (m, self.get_weights(n, m)))
                res.append(curr.minimal_spanning_tree())
            return res
        res_links, node_groups = [], []
        links = list(sorted((l for l in self.get_links()), key=lambda x: self.get_weights(x)))
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
                node_groups.append([*l])
                res_links.append(l)
            if len(node_groups) == 1 and len(node_groups[0]) == len(self.get_nodes()):
                return res_links, sum(self.get_weights(l) for l in res_links)
        return res_links, sum(v for v in (self.get_weights(l) for l in res_links))
    def minimal_path(self, node1: Node, node2: Node):
        if node1 in self.get_nodes() and node2 in self.get_nodes():
            if self.reachable(node1, node2):
                def DFS(curr_node, curr_path, total_negative, res_path=None):
                    if node1 == node2 and res_path is None:
                        res_path = [[], 0]
                    for n in [_ for _ in self.get_neighboring(curr_node) if Link(_, curr_node) not in curr_path[0]]:
                        if res_path is not None:
                            if curr_path[1] + self.get_weights(Link(n, curr_node)) + total_negative >= res_path[1]:
                                continue
                        if n == node2:
                            if res_path is None:
                                res_path = [curr_path[0].copy() + [Link(curr_node, n)], curr_path[1] + self.get_weights(Link(n, curr_node))]
                            elif curr_path[1] + self.get_weights(Link(curr_node, n)) < res_path[1]:
                                res_path[0], res_path[1] = curr_path[0].copy() + [Link(curr_node, n)], curr_path[1] + self.get_weights(Link(curr_node, n))
                        curr = DFS(n, [curr_path[0] + [Link(curr_node, n)], curr_path[1] + self.get_weights(Link(curr_node, n))], total_negative - self.get_weights(Link(curr_node, n)) * (self.get_weights(Link(curr_node, n)) < 0), res_path)
                        if curr is not None:
                            if res_path is None or curr[1] < res_path[1]:
                                res_path = curr
                    return res_path
                return DFS(node1, [[], 0], sum((sum(self.get_weights(n1, n2) for n2 in self.get_neighboring(n1) if self.get_weights(n1, n2) < 0) for n1 in self.get_nodes())) // 2)
            return f'No path between {node1} and {node2}!'
        raise ValueError('Unrecognized node(s)!')
    def __add__(self, other):
        res = self.copy()
        res._UndirectedGraph__nodes += [n for n in other.get_nodes() if n not in self.get_nodes()]
        res._UndirectedGraph__links += [l for l in other.get_links() if l not in self.get_links()]
        res._UndirectedGraph__degrees_sum = 2 * len(res.get_links())
        for n in res.get_nodes():
            if n not in res.get_neighboring().keys():
                res._UndirectedGraph__neighboring[n] = []
            for l in [l for l in res.get_links() if n in l]:
                sec = l.other(n)
                if sec not in res.get_neighboring(n):
                    res._UndirectedGraph__neighboring[n].append(sec)
        res._UndirectedGraph__degrees = Dict(*[(n, len(res.get_neighboring(n))) for n in res.get_nodes()])
        for l in other.get_links():
            if l not in res.__weights.keys():
                res.__weights[l] = other.get_weights(l)
            else:
                res.__weights[l] += other.get_weights(l)
        for l in other.get_links():
            res.__total_weight += other.get_weights(l)
        return res
    def __eq__(self, other):
        for n in self.get_nodes():
            if n not in other.get_nodes():
                return False
        return len(self.get_nodes()) == len(other.get_nodes()) and self.__weights == other.__weights
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.get_nodes()) + '}, ' + str(self.__weights) + ')'
class DirectedGraph:
    def __init__(self, start: Node, *rest: Node):
        for n in range(len(rest)):
            if start == rest[n]:
                raise ValueError('Can\'t have a node twice in a graph.')
            for m in range(n + 1, len(rest)):
                if rest[n] == rest[m]:
                    raise ValueError('Can\'t have a node twice in a graph.')
        self.__nodes, self.__links, self.__degrees_sum = [start, *rest], [], 0
        self.__degrees = Dict(*[(n, [0, 0]) for n in self.__nodes])
    def get_nodes(self):
        return self.__nodes
    def get_links(self):
        return self.__links
    def get_degrees(self, node=None):
        if node is None:
            return self.__degrees
        elif isinstance(node, Node):
            if node in self.__degrees.keys():
                return self.__degrees[node]
            raise ValueError('No such node in the graph!')
        raise TypeError('Node expected!')
    def get_degrees_sum(self):
        return self.__degrees_sum
    def add_node(self, node: Node, pointed_by: iter, points_to: iter):
        if node not in self.__nodes:
            for n in pointed_by + points_to:
                if n not in self.__nodes:
                    raise Exception('Unrecognized node(s)!')
            self.__degrees[node] = [0, 0]
            for n in pointed_by:
                self.__links.append((n, node))
                self.__degrees[n][0] += 1
                self.__degrees[node][1] += 1
                self.__degrees_sum += 2
            for n in points_to:
                self.__links.append((node, n))
                self.__degrees[n][1] += 1
                self.__degrees[node][0] += 1
                self.__degrees_sum += 2
            self.__nodes.append(node)
    def remove_node(self, node: Node):
        if node not in self.__nodes:
            raise Exception('Node not found.')
        c = 0
        while c < len(self.__links):
            link = self.__links[c]
            if node in link:
                sec = link[1 - link.index(node)]
                self.__degrees[sec][link.index(sec)] -= 1
                self.__links.remove(link)
                self.__degrees_sum -= 2
                c -= 1
            c += 1
        self.__nodes.remove(node)
        self.__degrees.pop(node)
    def connect_to_from(self, node1: Node, node2: Node, *rest: Node):
        if node1 not in self.__nodes:
            raise Exception('Node not found!')
        for current in [node2] + list(rest):
            if current in self.__nodes:
                if (current, node1) not in self.__links and node1 != current:
                    self.__links.append((current, node1))
                    self.__degrees[node1][1] += 1
                    self.__degrees[current][0] += 1
                    self.__degrees_sum += 2
    def connect_from_to(self, node1: Node, node2: Node, *rest: Node):
        if node1 not in self.__nodes:
            raise Exception('Node not found!')
        for current in [node2] + list(rest):
            if current in self.__nodes:
                if (node1, current) not in self.__links and node1 != current:
                    self.__links.append((node1, current))
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
    def copy(self):
        res = DirectedGraph(*self.__nodes)
        res.__links, res.__degrees, res.__degrees_sum = self.__links.copy(), self.__degrees.copy(), self.__degrees_sum
        return res
    def connected(self, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        return len(self.connection_components(nodes, links)) == 1
    def connection_components(self, nodes=None, links=None):
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
    def strongly_connected(self, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        for n in nodes:
            for m in [m for m in nodes if m != n]:
                if not self.reachable(n, m, nodes, links):
                    return False
        return True
    def reachable(self, node1: Node, node2: Node, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            raise Exception('Unrecognized node(s).')
        for comp in self.connection_components(nodes, links):
            if node1 in comp:
                if node2 in comp:
                    total, so_far = [node1], [node1]
                    while True:
                        for m in so_far:
                            for n in [n for n in nodes if (m, n) in links and n not in total]:
                                if n == node2:
                                    return True
                                if n not in total:
                                    total.append(n)
                        if so_far == total:
                            break
                        so_far = total.copy()
                return False
    def path_with_length(self, node1: Node, node2: Node, length: int, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if node1 not in nodes or node2 not in nodes:
            raise Exception('Unrecognized node(s).')
        if not self.reachable(node1, node2, nodes, links) or length < 0:
            return False
        if not length:
            return [False, []][node1 == node2]
        if (node1, node2) in links and length == 1:
            return [(node1, node2)]
        All = []
        for l in [l for l in links if node1 == l[0]]:
            sec = l[1]
            if sec in nodes:
                if self.reachable(sec, node2, nodes, [L for L in links if L != l]):
                    res = self.path_with_length(sec, node2, length - 1, [n for n in nodes if n != node1], [l for l in links if node1 not in l])
                    if res:
                        All.append([l] + res)
        for path in All:
            if len(path) == length + 1:
                return path
        return False
    def loop_with_length(self, length: int, nodes=None, links=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        for n in nodes:
            for l in [l for l in links if l[0] == n]:
                res = self.path_with_length(l[1], n, length - 1, nodes, [_l for _l in links if _l != (l[1], n)])
                if isinstance(res, list):
                    return [l] + res
        return False
    def get_shortest_path(self, node1: Node, node2: Node):
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        if (node1, node2) in self.__links:
            return [(node1, node2)]
        if not self.reachable(node1, node2):
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
                    try:
                        if len(paths[n]) > len(paths[m]) + 1:
                            paths[n] = [(n, m)] + paths[m]
                    except TypeError:
                        paths[n] = [(n, m)] + paths[m]
                    if n == node1:
                        return paths[n]
                    if n not in total:
                        total.append(n)
            if so_far == total:
                break
            so_far = total.copy()
        return paths[node1]
    def shortest_path_length(self, node1: Node, node2: Node):
        distances = Dict(*[(n, len(self.__links)) for n in self.__nodes])
        distances[node2] = 0
        if node1 not in self.__nodes or node2 not in self.__nodes:
            raise Exception('Unrecognized node(s).')
        if not self.reachable(node1, node2):
            return float('inf')
        if (node1, node2) in self.__links:
            return 1
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
            if so_far == total:
                break
            so_far = total.copy()
    def Euler_tour_exists(self):
        return all(d[0] == d[1] for d in self.__degrees.values())
    def Euler_walk_exists(self, start: Node, end: Node, links=None):
        if links is None:
            links = self.__links
        if self.Euler_tour_exists():
            return True
        temp_degrees = {n: [sum([n == l[0] for l in links]), sum([n == l[1] for l in links])] for n in self.__nodes}
        for node in self.__nodes:
            if temp_degrees[node][0] % 2 and node != start or temp_degrees[node][1] % 2 and node != end:
                return False
        return temp_degrees[start][0] % 2 + temp_degrees[end][1] % 2 in [0, 2]
    def Hamilton_tour_exists(self, nodes=None, links=None, can_continue_from=None, can_end_in=None, end_links=None):
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
            if not can_end_in:
                return False
            can_continue = False
            for n in nodes:
                if n in [l[1] for l in end_links]:
                    can_continue = True
                    break
            if not can_continue:
                return False
        if self.strongly_connected(nodes, links):
            return True
        for n in can_continue_from:
            if can_end_in is None:
                can_end_in = [m for m in nodes if (m, n) in links]
                end_links = [(m, n) for m in can_end_in]
            if self.Hamilton_tour_exists([_n for _n in nodes if _n != n], [l for l in links if n not in l], [_n for _n in nodes if (n, _n) in links], can_end_in, end_links):
                return True
        return False
    def Hamilton_walk_exists(self, node1: Node, node2=None, nodes=None, links=None, can_continue_from=None):
        if nodes is None:
            nodes = self.__nodes
        if links is None:
            links = self.__links
        if can_continue_from is None:
            can_continue_from = [n for n in nodes if (node1, n) in links]
        if not self.connected(nodes, links):
            return False
        if self.Hamilton_tour_exists(nodes, links, can_continue_from):
            return True
        if node2 is None:
            for n2 in [_n for _n in self.__nodes if _n != node1]:
                if self.Hamilton_walk_exists(node1, n2):
                    return True
            return False
        if node2 in nodes:
            if self.loop_with_length(len(nodes), nodes, links + [(node2, node1)] * ((node2, node1) not in links)) or len(nodes) == 1 and node1 == node2 or len(nodes) == 2 and (node1, node2) in links:
                return True
            for n in can_continue_from:
                if self.Hamilton_walk_exists(n, node2, [m for m in nodes if m != node1], [l for l in links if node1 not in l], [m for m in nodes if (n, m) in links and m not in [node1, node2]]):
                    return True
            return False
        raise ValueError('Unrecognized node(s).')
    def Euler_tour(self):
        if self.Euler_tour_exists():
            for n1 in self.__nodes:
                for n2 in [n for n in self.__nodes if (n, n1) in self.__links]:
                    res = self.Euler_walk(n1, n2, [l for l in self.__links if l != (n2, n1)])
                    if res:
                        return res + [(n2, n1)]
        return []
    def Euler_walk(self, node1: Node, node2: Node, links=None):
        if links is None:
            links = self.__links
        if node1 in self.__nodes and node2 in self.__nodes:
            if self.Euler_walk_exists(node1, node2, links):
                if links == [(node1, node2)]:
                    return [(node1, node2)]
                for l in links:
                    if node1 == l[0]:
                        res = self.Euler_walk(l[1], node2, [_l for _l in links if _l != l])
                        if res:
                            return [l] + res
            return []
        raise ValueError('Unrecognized nodes!')
    def Hamilton_tour(self):
        for n1 in self.__nodes:
            for n2 in [_n for _n in self.__nodes if (_n, n1) in self.__links]:
                res = self.Hamilton_walk(n1, n2)
                if isinstance(res, list):
                    return res
        return []
    def Hamilton_walk(self, node1: Node, node2=None, nodes=None, links=None, can_continue_from=None, res_stack=None):
        if node1 in self.__nodes and (node2 is None or node2 in self.__nodes):
            if nodes is None:
                nodes = self.__nodes
            if links is None:
                links = self.__links
            if res_stack is None:
                res_stack = [node1]
            if can_continue_from is None:
                can_continue_from = [n for n in nodes if (node1, n) in links and n != node2]
            if node2 is None:
                if len(nodes) == 1:
                    return nodes
                for n2 in [n for n in nodes if n != node1]:
                    res = self.Hamilton_walk(node1, n2)
                    if res:
                        return res
            else:
                if len(nodes) == 2 and (node1, node2) in links:
                    return [node1, node2]
            for n in can_continue_from:
                if node2 is None or n != node2:
                    res = self.Hamilton_walk(n, node2, [_n for _n in nodes if _n != node1], [l for l in links if node1 not in l], [_n for _n in nodes if (_n, n) in links and _n not in [node1, node2]], [n])
                    if res:
                        return res_stack + res
            return []
        raise ValueError('Unrecognized nodes!')
    def __add__(self, other):
        res = self.copy()
        res.__nodes += [n for n in other.get_nodes() if n not in self.__nodes]
        res.__links += [l for l in other.get_links() if l not in self.__links]
        for n in res.get_nodes():
            res.__degrees[n] = [0, 0]
            for l in [l for l in res.get_links() if n in l]:
                res.__degrees[n][l.index(n)] += 1
        res.__degrees_sum = 2 * len(res.get_links())
        return res
    def __eq__(self, other):
        for n in self.__nodes:
            if n not in other.get_nodes():
                return False
        for l in self.get_links():
            if l not in other.get_links():
                return False
        return len(self.get_links()) == len(other.get_links()) and len(self.get_nodes()) == len(other.get_nodes())
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.__nodes) + '}, {' + ', '.join(str(l) for l in self.__links) + '})'
    def __repr__(self):
        return str(self)
class WeightedDirectedGraph(DirectedGraph):
    def __init__(self, start: Node, *rest: Node):
        super().__init__(start, *rest)
        self.__weights, self.__total_weight = Dict(*[(l, 0) for l in self.get_links()]), 0
    def get_weights(self, node1_or_link=None, node2=None):
        if node1_or_link is None:
            return ', '.join([str(k) + ' -> ' + str(v) for k, v in self.__weights.items()])
        elif isinstance(node1_or_link, Node):
            if node2 is None:
                return ', '.join(str((node1_or_link, n)) + ' -> ' + str(self.__weights[(node1_or_link, n)]) for n in [m for m in self.get_nodes() if (node1_or_link, m) in self.get_links()])
            if isinstance(node2, Node):
                if node2 in self.get_nodes():
                    if (node1_or_link, node2) in self.get_links():
                        return self.__weights[(node1_or_link, node2)]
                    raise KeyError(f'No link from {node1_or_link} to {node2}!')
                raise ValueError('No such node exists in this graph!')
            raise TypeError('Node expected!')
        elif isinstance(node1_or_link, tuple):
            if node1_or_link in self.get_links():
                return self.__weights[node1_or_link]
            raise KeyError('Link not in graph!')
        raise TypeError('Node or link expected!')
    def get_total_weight(self):
        return self.__total_weight
    def add_node(self, node: Node, pointed_by_values: iter, points_to_values: iter):
        if node in self.get_nodes():
            raise ValueError('Can\'t add this node to this graph.')
        for p in points_to_values + pointed_by_values:
            if len(p) < 2:
                raise ValueError('Node-value pairs expected!')
        for v in [p[1] for p in pointed_by_values] + [p[1] for p in points_to_values]:
            if type(v) not in [int, float]:
                raise TypeError('Real numerical value expected!')
        pointed_by_res, points_to_res = [], []
        for n, v in pointed_by_values:
            if n in self.get_nodes() and n not in [p[0] for p in pointed_by_res]:
                pointed_by_res.append((n, v))
        for n, v in points_to_values:
            if n in self.get_nodes() and n not in [p[0] for p in points_to_res]:
                points_to_res.append((n, v))
        pointed_by_values, points_to_values = pointed_by_res, points_to_res
        self._DirectedGraph__degrees[node] = [0, 0]
        for n, v in pointed_by_values:
            self._DirectedGraph__links.append((n, node))
            self._DirectedGraph__degrees[n][0] += 1
            self._DirectedGraph__degrees[node][1] += 1
            self._DirectedGraph__degrees_sum += 2
            self.__weights[(n, node)] = v
            self.__total_weight += v
        for n, v in points_to_values:
            self._DirectedGraph__links.append((node, n))
            self._DirectedGraph__degrees[n][1] += 1
            self._DirectedGraph__degrees[node][0] += 1
            self._DirectedGraph__degrees_sum += 2
            self.__weights[(node, n)] = v
            self.__total_weight += v
        self._DirectedGraph__nodes.append(node)
    def remove_node(self, node: Node):
        if node not in self.get_nodes():
            raise Exception('Node not found.')
        c = 0
        while c < len(self.get_links()):
            link = self.get_links()[c]
            if node in link:
                sec = link[1 - link.index(node)]
                self._DirectedGraph__degrees[sec][link.index(sec)] -= 1
                self._DirectedGraph__links.remove(link)
                self._DirectedGraph__degrees_sum -= 2
                self.__total_weight -= self.get_weights(link)
                if node == link[0]:
                    self.__weights.pop((node, sec))
                else:
                    self.__weights.pop((sec, node))
                c -= 1
            c += 1
        self._DirectedGraph__nodes.remove(node)
        self._DirectedGraph__degrees.pop(node)
    def connect_to_from(self, node1: Node, node2_and_value: tuple, *nodes_values: tuple):
        if node1 not in self.get_nodes():
            raise Exception('Node not found!')
        for p in [node2_and_value] + list(nodes_values):
            if len(p) < 2:
                raise ValueError('Node-value pairs expected!')
        for v in [p[1] for p in [node2_and_value] + list(nodes_values)]:
            if type(v) not in [int, float]:
                raise TypeError('Real numerical value expected!')
        res = []
        for n, v in [node2_and_value] + list(nodes_values):
            if n not in [p[0] for p in res] and n in self.get_nodes():
                res.append((n, v))
        for current, v in res:
            if (current, node1) not in self.get_links() and node1 != current:
                self._DirectedGraph__links.append((current, node1))
                self._DirectedGraph__degrees[node1][1] += 1
                self._DirectedGraph__degrees[current][0] += 1
                self._DirectedGraph__degrees_sum += 2
                self.__weights[(current, node1)] = v
                self.__total_weight += v
    def connect_from_to(self, node1: Node, node2_and_value: tuple, *nodes_values: tuple):
        if node1 not in self.get_nodes():
            raise Exception('Node not found!')
        for p in [node2_and_value] + list(nodes_values):
            if len(p) < 2:
                raise ValueError('Node-value pairs expected!')
        for v in [p[1] for p in [node2_and_value] + list(nodes_values)]:
            if type(v) not in [int, float]:
                raise TypeError('Real numerical value expected!')
        res = []
        for n, v in [node2_and_value] + list(nodes_values):
            if n not in [p[0] for p in res] and n in self.get_nodes():
                res.append((n, v))
        for current, v in res:
            if (node1, current) not in self.get_links() and node1 != current:
                self._DirectedGraph__links.append((node1, current))
                self._DirectedGraph__degrees[node1][0] += 1
                self._DirectedGraph__degrees[current][1] += 1
                self._DirectedGraph__degrees_sum += 2
                self.__weights[(node1, current)] = v
                self.__total_weight += v
    def disconnect(self, node1: Node, node2: Node, *rest: Node):
        for n in [node2] + [*rest]:
            if (node1, n) in self.get_links():
                self._DirectedGraph__degrees[node1][0] -= 1
                self._DirectedGraph__degrees[n][1] -= 1
                self._DirectedGraph__degrees -= 2
                self._DirectedGraph__links.remove((node1, n))
                self.__total_weight -= self.__weights[(node1, n)]
                self.__weights.pop((node1, n))
    def copy(self):
        res = WeightedDirectedGraph(*self.get_nodes())
        for n in self.get_nodes():
            for m in self.get_nodes():
                if (n, m) in self.get_links():
                    res.connect_from_to(n, (m, self.get_weights(n, m)))
        return res
    def minimal_path(self, node1: Node, node2: Node):
        if node1 in self.get_nodes() and node2 in self.get_nodes():
            if self.reachable(node1, node2):
                def DFS(curr_node, curr_path, total_negative, res_path=None):
                    if node1 == node2 and res_path is None:
                        res_path = [[], 0]
                    for n in [_ for _ in self.get_nodes() if (curr_node, _) in self.get_links() and (curr_node, _) not in curr_path[0]]:
                        if res_path is not None:
                            if curr_path[1] + self.get_weights((curr_node, n)) + total_negative >= res_path[1]:
                                continue
                        if n == node2:
                            if res_path is None:
                                res_path = [curr_path[0].copy() + [(curr_node, n)], curr_path[1] + self.get_weights((curr_node, n))]
                            elif curr_path[1] + self.get_weights((curr_node, n)) < res_path[1]:
                                res_path[0], res_path[1] = curr_path[0].copy() + [(curr_node, n)], curr_path[1] + self.get_weights((curr_node, n))
                        curr = DFS(n, [curr_path[0] + [(curr_node, n)], curr_path[1] + self.get_weights((curr_node, n))], total_negative - self.get_weights((curr_node, n)) * (self.get_weights((curr_node, n)) < 0), res_path)
                        if curr is not None:
                            if res_path is None or curr[1] < res_path[1]:
                                res_path = curr
                    return res_path
                return DFS(node1, [[], 0], sum((sum(self.get_weights(n1, n2) for n2 in [n for n in self.get_nodes() if (n, n1) in self.get_links()] if self.get_weights(n1, n2) < 0)) for n1 in self.get_nodes()))
            return f'No path between {node1} and {node2}!'
        raise ValueError('Unrecognized node(s)!')
    def __add__(self, other):
        res = self.copy()
        res._DirectedGraph__nodes += [n for n in other.get_nodes() if n not in self.get_nodes()]
        res._DirectedGraph__links += [l for l in other.get_links() if l not in self.get_links()]
        for n in res.get_nodes():
            res._DirectedGraph__degrees[n] = [0, 0]
            for l in [l for l in res.get_links() if n in l]:
                res._DirectedGraph__degrees[n][l.index(n)] += 1
        res._DirectedGraph__degrees_sum = 2 * len(res.get_links())
        for l in other.get_links():
            if l not in res.__weights.keys():
                res.__weights[l] = other.get_weights(l)
            else:
                res.__weights[l] += other.get_weights(l)
        for l in other.get_links():
            res.__total_weight += other.get_weights(l)
        return res
    def __eq__(self, other):
        for n in self.get_nodes():
            if n not in other.get_nodes():
                return False
        return len(self.get_nodes()) == len(other.get_nodes()) and self.__weights == other.__weights
    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.get_nodes()) + '}, ' + f'{self.__weights}' + ')'
class Tree:
    def __init__(self, root: Node, *descendants: Node):
        self.__root = root
        if root in descendants:
            raise ValueError('Can\'t have a node twice in a tree!')
        for i in range(len(descendants)):
            for j in range(i + 1, len(descendants)):
                if descendants[i] == descendants[j]:
                    raise ValueError('Can\'t have a node twice in a tree!')
        self.__hierarchy, self.__nodes, self.__links, self.__leaves = Dict((self.__root, list(descendants))), [root, *descendants], [Link(root, n) for n in descendants], [*descendants] if descendants else [root]
    def get_root(self):
        return self.__root
    def get_nodes(self):
        return self.__nodes
    def get_links(self):
        return self.__links
    def get_leaves(self):
        return self.__leaves
    def get_hierarchy(self):
        return self.__hierarchy
    def get_descendants(self, node: Node):
        return self.__hierarchy[node]
    def add_nodes_to(self, old: Node, node: Node, *rest: Node):
        if old not in self.__nodes:
            raise Exception('Node not found!')
        if old in self.__leaves:
            self.__leaves.remove(old)
        for n in [node] + [*rest]:
            if n not in self.get_nodes():
                self.__nodes.append(n)
                self.__hierarchy[old].append(n)
                self.__links.append(Link(old, n))
                self.__leaves.append(n)
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
    def get_parent(self, node: Node):
        if node in self.__nodes:
            if node == self.__root:
                return None
            for k, v in self.__hierarchy.items():
                if node in v:
                    return k
        raise ValueError('Node not in graph!')
    def node_depth(self, node: Node):
        if node in self.__nodes:
            d = 0
            while node != self.__root:
                node = self.get_parent(node)
                d += 1
            return d
        raise ValueError('Node not in graph!')
    def depth(self):
        return max(self.node_depth(l) for l in self.__leaves)
    def __eq__(self, other):
        for n in self.get_nodes():
            if n not in other.get_nodes():
                return False
        if len(self.__nodes) - len(other.__nodes):
            return False
        for n in self.__nodes:
            if len(self.__hierarchy[n]) - len(other.__hierarchy[n]):
                return False
            for m in self.__hierarchy[n]:
                if m not in other.__hierarchy[n]:
                    return False
            return True
    def __str__(self):
        return '\n'.join(str(k) + ' -- ' + str(v) for k, v in self.__hierarchy.items())
    def __repr__(self):
        return str(self)
