from Graphs.General import Node, SortedList


class DirectedGraph:
    def __init__(self, neighborhood: dict, f=lambda x: x):
        self.__nodes, self.__f, self.__links = SortedList(f=f), f, []
        self.__prev, self.__next, self.__degrees = dict(), dict(), dict()
        for u, (prev_nodes, next_nodes) in neighborhood.items():
            self.add(u)
            for v in prev_nodes:
                if v in self.nodes:
                    self.connect(u, [v])
                else:
                    self.add(v, [], [u])
            for v in next_nodes:
                if v in self.nodes:
                    self.connect(v, [u])
                else:
                    self.add(v, [u])

    @property
    def nodes(self):
        return self.__nodes

    @property
    def links(self):
        return self.__links

    def degrees(self, u: Node = None):
        return self.__degrees if u is None else self.__degrees[u]

    def next(self, u: Node = None):
        return self.__next if u is None else self.__next[u]

    def prev(self, u: Node = None):
        return self.__prev if u is None else self.__prev[u]

    def f(self, x=None):
        return self.__f if x is None else self.__f(x)

    def add(self, u: Node, pointed_by: [Node] = (), points_to: [Node] = ()):
        if u not in self.nodes:
            self.__nodes.insert(u)
            self.__degrees[u], self.__next[u], self.__prev[u] = [0, 0], SortedList(f=self.f()), SortedList(f=self.f())
            DirectedGraph.connect(self, u, pointed_by, points_to)
        return self

    def remove(self, u: Node, *rest: Node):
        for n in (u,) + rest:
            if n in self.nodes:
                DirectedGraph.disconnect(self, n, self.prev(n).copy(), self.next(n).copy())
                self.__nodes.remove(n), self.__next.pop(n), self.__degrees.pop(n), self.__prev.pop(n)
        return self

    def connect(self, u: Node, pointed_by: [Node] = (), points_to: [Node] = ()):
        if u in self.nodes:
            for v in pointed_by:
                if u != v and v not in self.prev(u) and v in self.nodes:
                    self.__links.append((v, u)), self.__prev[u].insert(v), self.__next[v].insert(u)
                    self.__degrees[u][0] += 1
                    self.__degrees[v][1] += 1
            for v in points_to:
                if u != v and v not in self.next(u) and v in self.nodes:
                    self.__links.append((u, v)), self.__prev[v].insert(u), self.__next[u].insert(v)
                    self.__degrees[u][1] += 1
                    self.__degrees[v][0] += 1
        return self

    def disconnect(self, u: Node, pointed_by: [Node] = (), points_to: [Node] = ()):
        if u in self.nodes:
            for v in pointed_by:
                if v in self.prev(u):
                    self.__degrees[u][0] -= 1
                    self.__degrees[v][1] -= 1
                    self.__links.remove((v, u)), self.__next[v].remove(u), self.__prev[u].remove(v)
            for v in points_to:
                if v in self.next(u):
                    self.__degrees[u][1] -= 1
                    self.__degrees[v][0] -= 1
                    self.__links.remove((u, v)), self.__next[u].remove(v), self.__prev[v].remove(u)
        return self

    def complementary(self):
        res = DirectedGraph(dict([(n, ([], [])) for n in self.nodes]), self.f())
        for i, n in enumerate(self.nodes):
            for j in range(i + 1, len(self.nodes)):
                if self.nodes[j] not in self.next(n):
                    res.connect(self.nodes[j], [n])
        return res

    def transposed(self):
        return DirectedGraph(dict([(u, (self.next(u), self.prev(u))) for u in self.nodes]))

    def copy(self):
        return DirectedGraph(dict([(n, (self.prev(n), self.next(n))) for n in self.nodes]), self.f())

    def connected(self):
        m, n = len(self.links), len(self.nodes)
        if m + 1 < n:
            return False
        if m > (n - 1) * (n - 2) or n < 2:
            return True
        return self.component(self.nodes[0]) == self

    @property
    def sources(self):
        return [u for u in self.nodes if not self.degrees(u)[0]]

    @property
    def sinks(self):
        return [v for v in self.nodes if not self.degrees(v)[1]]

    def has_loop(self):
        sources, total, stack = self.sources, SortedList(f=self.f()), SortedList(f=self.f())
        if not sources or not self.sinks:
            return True

        def dfs(u):
            for v in self.next(u):
                if v in total:
                    continue
                if v in stack:
                    return True
                stack.insert(v)
                if dfs(v):
                    return True
                stack.remove(v)
            total.insert(u)
            return False

        for n in sources:
            stack.insert(n)
            if dfs(n):
                return True
            stack.remove(n)
        return False

    def dag(self):
        return not self.has_loop()

    def toposort(self):
        if not self.dag():
            return []
        layer, total = self.sources, SortedList(f=self.f())
        res = layer.copy()
        while layer:
            new = SortedList(f=self.f())
            for u in layer:
                total.insert(u)
                for v in self.next(u):
                    if v not in new:
                        new.insert(v)
            for u in new.copy():
                if any(v not in total for v in self.prev(u)):
                    new.remove(u)
            res, layer = res + new.value, new.copy()
        return res

    def connection_components(self):
        if not self:
            return [[]]
        components, queue = [[self.nodes[0]]], [self.nodes[0]]
        total, k, n = SortedList(self.nodes[0], f=self.f()), 1, len(self.nodes)
        while k < n:
            while queue:
                u = queue.pop(0)
                for v in filter(lambda x: x not in total, self.next(u) + self.prev(u)):
                    components[-1].append(v), queue.append(v), total.insert(v)
                    k += 1
                    if k == n:
                        return components
            if k < n:
                new = [[n for n in self.nodes if n not in total][0]]
                components.append(new), total.insert(new[0])
                k, queue = k + 1, [new[0]]
                if k == n:
                    return components
        return components

    def reachable(self, u: Node, v: Node):
        if u not in self.nodes or v not in self.nodes:
            raise Exception("Unrecognized node(s).")
        return v in self.subgraph(u)

    def component(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], DirectedGraph(dict([(u, ([], []))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, [v])
                else:
                    res.add(n, [v]), queue.append(n)
            for n in self.prev(v):
                if n in res.nodes:
                    res.connect(v, [n])
                else:
                    res.add(n, [], [v]), queue.append(n)
        return res

    def subgraph(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], DirectedGraph(dict([(u, ([], []))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, [v])
                else:
                    res.add(n, [v]), queue.append(n)
        return res

    def cut_nodes(self):
        def dfs(x: Node, l: int):
            colors[x], levels[x], min_back, is_root, count, is_cut = 1, l, l, not l, 0, False
            for y in self.next(x) + self.prev(x):
                if not colors[y]:
                    count += 1
                    b = dfs(y, l + 1)
                    if b >= l and not is_root: is_cut = True
                    min_back = min(min_back, b)
                if colors[y] == 1 and levels[y] < min_back and levels[y] + 1 != l:
                    min_back = levels[y]
            if is_cut or is_root and count > 1:
                res.append(x)
            colors[x] = 2
            return min_back

        levels = dict([(n, 0) for n in self.nodes])
        colors, res = levels.copy(), []
        for n in self.nodes:
            if not colors[n]:
                dfs(n, 0)
        return res

    def get_shortest_path(self, u: Node, v: Node):
        if u not in self.nodes or v not in self.nodes:
            raise Exception("Unrecognized node(s)!")
        previous = dict([(n, None) for n in self.nodes])
        queue, total = [u], SortedList(u, f=self.f())
        previous.pop(u)
        while queue:
            n = queue.pop(0)
            if n == v:
                res, curr_node = [n], n
                while curr_node != u:
                    res.insert(0, previous[curr_node])
                    curr_node = previous[curr_node]
                return res
            for y in filter(lambda _x: _x not in total, self.next(n)):
                queue.append(y), total.insert(y)
                previous[y] = n

    def euler_tour_exists(self):
        for d in self.degrees().values():
            if d[0] != d[1]:
                return False
        return self.connected()

    def euler_walk_exists(self, u: Node, v: Node):
        if u not in self.nodes or v not in self.nodes:
            raise ValueError("Unrecognized node(s)!")
        if self.euler_tour_exists():
            return u == v
        if self.degrees(u)[0] + 1 != self.degrees(u)[1] or self.degrees(v)[0] != self.degrees(v)[1] + 1:
            return False
        for n in self.nodes:
            if n not in (u, v) and self.degrees(n)[1] != self.degrees(n)[0]:
                return False
        return self.connected()

    def euler_tour(self):
        if self.euler_tour_exists():
            tmp = DirectedGraph.copy(self)
            v, u = self.links[0]
            return tmp.disconnect(u, [v]).euler_walk(u, v)
        return []

    def euler_walk(self, u: Node, v: Node):
        def dfs(x, stack):
            for y in self.next(x):
                if (x, y) not in result + stack:
                    if y == n:
                        result.insert(i + 1, (x, y))
                        while stack:
                            result.insert(i + 1, stack.pop())
                        return True
                    if dfs(y, stack + [(x, y)]):
                        return True

        if u not in self.nodes or v not in self.nodes:
            raise ValueError("Unrecognized node(s)!")
        if self.euler_walk_exists(u, v):
            tmp = self.get_shortest_path(u, v)
            result = [(tmp[i], tmp[i + 1]) for i in range(len(tmp) - 1)]
            while len(result) < len(self.links):
                i, n = -1, result[0][0]
                dfs(n, [])
                for i, l in enumerate(result):
                    n = l[1]
                    dfs(n, [])
                return list(map(lambda _l: _l[0], result)) + [v]
        return []

    def stronglyConnectedComponents(self):
        def helper(x, stack):
            for y in self.next(x):
                if y not in curr:
                    helper(y, stack + [y])
                elif x not in curr and y in curr:
                    curr_node, new = stack.pop(), []
                    while curr_node not in curr:
                        total.insert(curr_node), curr.insert(curr_node), new.append(curr_node)
                        if not stack:
                            break
                        curr_node = stack.pop()
                    return

        def dfs(x, stack):
            for y in self.next(x):
                if y not in curr and y not in stack:
                    dfs(y, stack + [y])
                if y == n:
                    curr_node = stack.pop()
                    while stack and curr_node != n:
                        total.insert(curr_node), curr.insert(curr_node)
                        curr_node = stack.pop()
                    for curr_node in curr:
                        helper(curr_node, [curr_node])
                    return

        if self.dag():
            return list(map(lambda x: [x], self.nodes))
        if not self.connected():
            res = []
            for c in self.connection_components():
                res += self.component(c[0]).stronglyConnectedComponents()
            return res
        total, res = SortedList(f=self.f()), []
        for n in self.nodes:
            if n not in total:
                curr = SortedList(n, f=self.f())
                dfs(n, [n]), res.append(curr), total.insert(n)
        return res

    def pathWithLength(self, u: Node, v: Node, length: int):
        def dfs(x: Node, l: int, stack):
            if not l:
                return ([], list(map(lambda link: link[0], stack)) + [v])[x == v]
            for y in filter(lambda _x: (x, _x) not in stack, self.next(x)):
                res = dfs(y, l - 1, stack + [(x, y)])
                if res:
                    return res
            return []

        tmp = self.get_shortest_path(u, v)
        if not tmp or len(tmp) > length + 1:
            return []
        if length + 1 == len(tmp):
            return tmp
        return dfs(u, length, [])

    def loopWithLength(self, length: int):
        if abs(length) < 2:
            return []
        tmp = DirectedGraph.copy(self)
        for l in tmp.links:
            u, v = l
            tmp.disconnect(v, [u])
            res = tmp.pathWithLength(v, u, length - 1)
            tmp.connect(v, [u])
            if res:
                return res
        return []

    def hamiltonTourExists(self):
        def dfs(x):
            if tmp.nodes == [x]:
                return x in can_end_in
            if all(y not in tmp.nodes for y in can_end_in):
                return False
            tmp0, tmp1 = tmp.prev(x).copy(), tmp.next(x).copy()
            tmp.remove(x)
            for y in tmp1:
                res = dfs(y)
                if res:
                    tmp.add(x, tmp0, tmp1)
                    return True
            tmp.add(x, tmp0, tmp1)
            return False

        if len(self.links) > (len(self.nodes) - 1) ** 2 + 1:
            return True
        u, tmp = self.nodes[0], DirectedGraph.copy(self)
        can_end_in = tmp.prev(u).copy()
        return dfs(u)

    def hamiltonWalkExists(self, u: Node, v: Node):
        if u not in self.nodes or v not in self.nodes:
            raise Exception("Unrecognized node(s).")
        if u in self.next(v):
            return True if all(n in (u, v) for n in self.nodes) else self.hamiltonTourExists()
        tmp = DirectedGraph.copy(self)
        return tmp.connect(u, [v]).hamiltonTourExists()

    def hamiltonTour(self):
        if self.sources or self.sinks:
            return []
        u = self.nodes[0]
        for v in self.prev(u):
            result = self.hamiltonWalk(u, v)
            if result:
                return result
        return []

    def hamiltonWalk(self, u: Node = None, v: Node = None):
        def dfs(x, stack):
            too_many = v is not None
            for n in tmp.nodes:
                if not tmp.degrees(n)[0] and n != x:
                    return []
                if not tmp.degrees(n)[1] and n != v:
                    if too_many:
                        return []
                    too_many = True
            tmp0, tmp1 = tmp.prev(x).copy(), tmp.next(x).copy()
            tmp.remove(x)
            if not tmp.nodes:
                tmp.add(x, tmp0, tmp1)
                return stack
            for y in tmp1:
                if y == v:
                    if tmp.nodes == [v]:
                        tmp.add(x, tmp0, tmp1)
                        return stack + [v]
                    continue
                res = dfs(y, stack + [y])
                if res:
                    tmp.add(x, tmp0, tmp1)
                    return res
            tmp.add(x, tmp0, tmp1)
            return []

        tmp = DirectedGraph.copy(self)
        if u is None:
            if v is not None and v not in self.nodes:
                raise Exception("Unrecognized node.")
            for _u in sorted(self.nodes, key=lambda _x: self.degrees(_x)[1]):
                result = dfs(_u, [_u])
                if result:
                    return result
            return []
        if u not in self.nodes or v is not None and v not in self.nodes:
            raise Exception("Unrecognized node(s).")
        return dfs(u, [u])

    def isomorphicFunction(self, other):
        if isinstance(other, DirectedGraph):
            if len(self.links) != len(other.links) or len(self.nodes) != len(other.nodes):
                return dict()
            this_degrees, other_degrees = dict(), dict()
            for d in map(tuple, self.degrees().values()):
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in map(tuple, other.degrees().values()):
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            if this_degrees != other_degrees:
                return dict()
            this_nodes_degrees = {d: [] for d in this_degrees.keys()}
            other_nodes_degrees = {d: [] for d in other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes:
                    if self.degrees(n) == list(d):
                        this_nodes_degrees[d].append(n)
                for n in other.nodes:
                    if other.degrees(n) == list(d):
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p)))
            other_nodes_degrees = list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility):
                    map_dict += [*zip(group, other_nodes_degrees[i])]
                map_dict = dict(map_dict)
                possible = True
                for n, u in map_dict.items():
                    for m, v in map_dict.items():
                        if (m in self.next(n)) ^ (v in other.next(u)):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return map_dict
            return dict()
        return dict()

    def __bool__(self):
        return bool(self.nodes)

    def __call__(self, x):
        return self.f(x)

    def __reversed__(self):
        return self.complementary()

    def __contains__(self, item):
        return item in self.nodes or item in self.links

    def __add__(self, other):
        if not isinstance(other, DirectedGraph):
            raise TypeError(f"Addition not defined between class DirectedGraph and type {type(other).__name__}!")
        if any(self(n) != other(n) for n in self.nodes + other.nodes):
            raise ValueError("Node sorting functions don't match!")
        if isinstance(other, (WeightedNodesDirectedGraph, WeightedLinksDirectedGraph)):
            return other + self
        res = self.copy()
        for n in other.nodes:
            if n not in res.nodes:
                res.add(n)
        for (u, v) in other.links:
            if v not in res.next(u):
                res.connect(v, [u])
        return res

    def __eq__(self, other):
        if isinstance(other, DirectedGraph):
            if len(self.links) != len(other.links) or self.nodes != other.nodes:
                return False
            for l in self.links:
                if l not in other.links:
                    return False
            return True
        return False

    def __str__(self):
        return "({" + ", ".join(str(n) for n in self.nodes) + "}, {" + ", ".join(str(l) for l in self.links) + "})"

    __repr__ = __str__


class WeightedNodesDirectedGraph(DirectedGraph):
    def __init__(self, neighborhood: dict, f=lambda x: x):
        super().__init__(dict(), f=f)
        self.__node_weights = dict()
        for n, p in neighborhood.items():
            self.add((n, p[0]))
        for u, p in neighborhood.items():
            for v in p[1][0]:
                if v in self.nodes:
                    self.connect(u, [v])
                else:
                    self.add((v, 0), [], [u])
            for v in p[1][1]:
                if v in self.nodes:
                    self.connect(v, [u])
                else:
                    self.add((v, 0), [u])

    def node_weights(self, n: Node = None):
        return self.__node_weights if n is None else self.__node_weights.get(n)

    @property
    def total_nodes_weight(self):
        return sum(self.node_weights().values())

    def copy(self):
        return WeightedNodesDirectedGraph(dict([(n, (self.node_weights(n), (self.prev(n), self.next(n)))) for n in self.nodes]), self.f())

    def add(self, n_w: (Node, float), pointed_by: [Node] = (), points_to: [Node] = ()):
        super().add(n_w[0], pointed_by, points_to)
        if n_w[0] not in self.node_weights():
            self.set_weight(*n_w)
        return self

    def remove(self, u: Node, *rest: Node):
        for n in (u,) + rest:
            self.__node_weights.pop(n)
        return DirectedGraph.remove(self, u, *rest)

    def set_weight(self, u: Node, w: float):
        if u in self.nodes:
            self.__node_weights[u] = w
        return self

    def transposed(self):
        return WeightedNodesDirectedGraph(dict([(u, (self.node_weights(u), (self.next(u), self.prev(u)))) for u in self.nodes]))

    def component(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], WeightedNodesDirectedGraph(dict([(u, (self.node_weights(u), ([], [])))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, [v])
                else:
                    res.add((n, self.node_weights(n)), [v]), queue.append(n)
            for n in self.prev(v):
                if n in res.nodes:
                    res.connect(v, [n])
                else:
                    res.add((n, self.node_weights(n)), [], [v]), queue.append(n)
        return res

    def subgraph(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], WeightedNodesDirectedGraph(dict([(u, (self.node_weights(u), ([], [])))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, [v])
                else:
                    res.add((n, self.node_weights(n)), [v]), queue.append(n)
        return res

    def minimalPathNodes(self, u: Node, v: Node):
        return WeightedDirectedGraph(dict([(n, (self.node_weights(n), (dict(), dict([(m, 0) for m in self.next(n)])))) for n in self.nodes]), self.f()).minimalPath(u, v)

    def isomorphicFunction(self, other):
        if isinstance(other, WeightedNodesDirectedGraph):
            if len(self.links) != len(other.links) or len(self.nodes) != len(other.nodes):
                return dict()
            this_degrees, other_degrees, this_weights, other_weights = dict(), dict(), dict(), dict()
            for d in map(tuple, self.degrees().values()):
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in map(tuple, other.degrees().values()):
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            for w in self.node_weights().values():
                if w in this_weights:
                    this_weights[w] += 1
                else:
                    this_weights[w] = 1
            for w in other.node_weights().values():
                if w in other_weights:
                    other_weights[w] += 1
                else:
                    other_weights[w] = 1
            if this_degrees != other_degrees or this_weights != other_weights:
                return dict()
            this_nodes_degrees = {d: [] for d in this_degrees.keys()}
            other_nodes_degrees = {d: [] for d in other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes:
                    if self.degrees(n) == list(d):
                        this_nodes_degrees[d].append(n)
                for n in other.nodes:
                    if other.degrees(n) == list(d):
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p)))
            other_nodes_degrees = list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility):
                    map_dict += [*zip(group, other_nodes_degrees[i])]
                map_dict = dict(map_dict)
                possible = True
                for n, u in map_dict.items():
                    for m, v in map_dict.items():
                        if (m in self.next(n)) ^ (v in other.next(u)) or self.node_weights(n) != other.node_weights(u):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return map_dict
            return dict()
        return super().isomorphicFunction(other)

    def __add__(self, other):
        if not isinstance(other, DirectedGraph):
            raise TypeError(f"Addition not defined between class DirectedGraph and type {type(other).__name__}!")
        if any(self(n) != other(n) for n in self.nodes + other.nodes):
            raise ValueError("Node sorting functions don't match!")
        if isinstance(other, WeightedDirectedGraph):
            return other + self
        if isinstance(other, WeightedLinksDirectedGraph):
            return WeightedDirectedGraph(dict(), self.f()) + self + other
        res = self.copy()
        if isinstance(other, WeightedNodesDirectedGraph):
            for n in other.nodes:
                if n in res.nodes:
                    res.set_weight(n, res.node_weights(n) + other.node_weights(n))
                else:
                    res.add((n, other.node_weights(n)))
            for u, v in other.links:
                if v not in res.next(u):
                    res.connect(v, [u])
            return res
        for n in other.nodes:
            if n not in res.nodes:
                res.add((n, 0))
        for u, v in other.links:
            if v not in res.next(u):
                res.connect(v, [u])
        return res

    def __eq__(self, other):
        if isinstance(other, WeightedNodesDirectedGraph):
            if len(self.links) != len(other.links) or self.node_weights() != other.node_weights():
                return False
            for l in self.links:
                if l not in other.links:
                    return False
            return True
        return False

    def __str__(self):
        return "({" + ", ".join(f"{str(n)} -> {self.node_weights(n)}" for n in self.nodes) + "}, {" + ", ".join(str(l) for l in self.links) + "})"


class WeightedLinksDirectedGraph(DirectedGraph):
    def __init__(self, neighborhood: dict, f=lambda x: x):
        super().__init__(dict(), f=f)
        self.__link_weights = dict()
        for u, (prev_pairs, next_pairs) in neighborhood.items():
            if u not in self.nodes:
                self.add(u)
            for v, w in prev_pairs.items():
                if v not in self.nodes:
                    self.add(v, points_to_weights=dict([(u, w)]))
                elif v not in self.prev(u):
                    self.connect(u, dict([(v, w)]))
            for v, w in next_pairs.items():
                if v not in self.nodes:
                    self.add(v, dict([(u, w)]))
                elif v not in self.next(u):
                    self.connect(v, dict([(u, w)]))

    def link_weights(self, u_or_l: Node | tuple = None, v: Node = None):
        if u_or_l is None:
            return self.__link_weights
        elif isinstance(u_or_l, Node):
            if v is None:
                return dict([(n, self.__link_weights[(u_or_l, n)]) for n in self.next(u_or_l)], f=self.f())
            return self.__link_weights.get((u_or_l, v))
        elif isinstance(u_or_l, tuple):
            return self.__link_weights.get(u_or_l)

    @property
    def total_links_weight(self):
        return sum(self.link_weights().values())

    def add(self, u: Node, pointed_by_weights: dict = dict(), points_to_weights: dict = dict()):
        if u not in self.nodes:
            super().add(u), self.connect(u, pointed_by_weights, points_to_weights)
        return self

    def remove(self, n: Node, *rest: Node):
        for u in (n,) + rest:
            for v in self.next(u):
                self.__link_weights.pop((u, v))
            for v in self.prev(u):
                self.__link_weights.pop((v, u))
        return super().remove(n, *rest)

    def connect(self, u: Node, pointed_by_weights: dict = dict(), points_to_weights: dict = dict()):
        if u in self.nodes:
            super().connect(u, pointed_by_weights.keys(), points_to_weights.keys())
            for v, w in pointed_by_weights.items():
                if (v, u) not in self.link_weights():
                    self.set_weight((v, u), w)
            for v, w in points_to_weights.items():
                if (u, v) not in self.link_weights():
                    self.set_weight((u, v), w)
        return self

    def disconnect(self, u: Node, pointed_by: [Node] = (), points_to: [Node] = ()):
        if u in self.nodes:
            for v in pointed_by:
                self.__link_weights.pop((v, u))
            for v in points_to:
                self.__link_weights.pop((u, v))
            super().disconnect(u, pointed_by, points_to)
        return self

    def set_weight(self, l: tuple, w: float):
        if l in self.links:
            self.__link_weights[l] = w
        return self

    def transposed(self):
        return WeightedLinksDirectedGraph(dict([(u, (self.link_weights(u), dict([(v, self.link_weights(v, u)) for v in self.prev(u)]))) for u in self.nodes]), self.f())

    def copy(self):
        return WeightedLinksDirectedGraph(dict([(u, (dict([(v, self.link_weights(v, u)) for v in self.prev(u)]), self.link_weights(u))) for u in self.nodes]), self.f())

    def component(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], WeightedLinksDirectedGraph(dict([(u, (dict(), dict()))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, dict([(v, self.link_weights((v, n)))]))
                else:
                    res.add(n, dict([(v, self.link_weights((v, n)))])), queue.append(n)
            for n in self.prev(v):
                if n in res.nodes:
                    res.connect(v, dict([(n, self.link_weights((n, v)))]))
                else:
                    res.add(n, points_to_weights=dict([(v, self.link_weights((n, v)))])), queue.append(n)
        return res

    def subgraph(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], WeightedLinksDirectedGraph(dict([(u, (dict(), dict()))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, dict([(v, self.link_weights(v, n))]))
                else:
                    res.add(n, dict([(v, self.link_weights(v, n))])), queue.append(n)
        return res

    def minimalPathLinks(self, u: Node, v: Node):
        return WeightedDirectedGraph(dict([(n, (0, (dict(), self.link_weights(n)))) for n in self.nodes]), self.f()).minimalPath(u, v)

    def isomorphicFunction(self, other):
        if isinstance(other, WeightedLinksDirectedGraph):
            if len(self.links) != len(other.links) or len(self.nodes) != len(other.nodes):
                return dict()
            this_degrees, other_degrees, this_weights, other_weights = dict(), dict(), dict(), dict()
            for d in map(tuple, self.degrees().values()):
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in map(tuple, other.degrees().values()):
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            for w in self.link_weights().values():
                if w in this_weights:
                    this_weights[w] += 1
                else:
                    this_weights[w] = 1
            for w in other.link_weights().values():
                if w in other_weights:
                    other_weights[w] += 1
                else:
                    other_weights[w] = 1
            if this_degrees != other_degrees or this_weights != other_weights:
                return dict()
            this_nodes_degrees = {d: [] for d in this_degrees.keys()}
            other_nodes_degrees = {d: [] for d in other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes:
                    if self.degrees(n) == list(d):
                        this_nodes_degrees[d].append(n)
                for n in other.nodes:
                    if other.degrees(n) == list(d):
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p)))
            other_nodes_degrees = list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility):
                    map_dict += [*zip(group, other_nodes_degrees[i])]
                map_dict = dict(map_dict)
                possible = True
                for n, u in map_dict.items():
                    for m, v in map_dict.items():
                        if self.link_weights((n, m)) != other.link_weights((u, v)):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return map_dict
            return dict()
        return super().isomorphicFunction(other)

    def __add__(self, other):
        if not isinstance(other, DirectedGraph):
            raise TypeError(f"Addition not defined between class DirectedGraph and type {type(other).__name__}!")
        if any(self(n) != other(n) for n in self.nodes + other.nodes):
            raise ValueError("Node sorting functions don't match!")
        if isinstance(other, WeightedNodesDirectedGraph):
            return other + self
        res = self.copy()
        if isinstance(other, WeightedLinksDirectedGraph):
            for n in other.nodes:
                if n not in res.nodes:
                    res.add(n)
            for u, v in other.links:
                if v in res.next(u):
                    res.set_weight((u, v), res.link_weights(u, v) + other.link_weights(u, v))
                else:
                    res.connect(v, dict([(u, other.link_weights((u, v)))]))
            return res
        for n in other.nodes:
            if n not in res.nodes:
                res.add(n)
        for u, v in other.links:
            res.connect(v, dict([(u, self.link_weights((u, v)))]))
        return res

    def __eq__(self, other):
        if isinstance(other, WeightedLinksDirectedGraph):
            return self.nodes == other.nodes and self.link_weights() == other.link_weights()
        return False

    def __str__(self):
        return "({" + ", ".join(str(n) for n in self.nodes) + "}, " + f"{self.link_weights()}" + ")"


class WeightedDirectedGraph(WeightedNodesDirectedGraph, WeightedLinksDirectedGraph):
    def __init__(self, neighborhood: dict, f=lambda x: x):
        WeightedNodesDirectedGraph.__init__(self, dict(), f), WeightedLinksDirectedGraph.__init__(self, dict(), f)
        for n, p in neighborhood.items():
            self.add((n, p[0]))
        for u, p in neighborhood.items():
            for v, w in p[1][0].items():
                if v in self.nodes:
                    self.connect(u, dict([(v, w)]))
                else:
                    self.add((v, 0), points_to_weights=dict([(u, w)]))
        for u, p in neighborhood.items():
            for v, w in p[1][1].items():
                if v in self.nodes:
                    self.connect(v, dict([(u, w)]))
                else:
                    self.add((v, 0), dict([(u, w)]))

    @property
    def total_weight(self):
        return self.total_nodes_weight + self.total_links_weight

    def add(self, n_w: (Node, float), pointed_by_weights: dict = dict(), points_to_weights: dict = dict()):
        WeightedLinksDirectedGraph.add(self, n_w[0], pointed_by_weights, points_to_weights)
        if n_w[0] not in self.node_weights():
            self.set_weight(*n_w)
        return self

    def remove(self, u: Node, *rest: Node):
        for n in (u,) + rest:
            WeightedLinksDirectedGraph.disconnect(self, n, self.prev(n), self.next(n)), super().remove(n)
        return self

    def connect(self, u: Node, pointed_by_weights: dict = dict(), points_to_weights: dict = dict()):
        return WeightedLinksDirectedGraph.connect(self, u, pointed_by_weights, points_to_weights)

    def disconnect(self, u: Node, pointed_by: [Node] = (), points_to: [Node] = ()):
        return WeightedLinksDirectedGraph.disconnect(self, u, pointed_by, points_to)

    def set_weight(self, el: Node | tuple, w: float):
        if el in self.nodes:
            super().set_weight(el, w)
        elif el in self.links:
            WeightedLinksDirectedGraph.set_weight(self, el, w)
        return self

    def transposed(self):
        return WeightedDirectedGraph(dict([(u, (self.node_weights(u), (self.link_weights(u), dict([(v, self.link_weights(v, u)) for v in self.prev(u)])))) for u in self.nodes]), self.f())

    def copy(self):
        return WeightedDirectedGraph(dict([(u, (self.node_weights(u), (dict([(v, self.link_weights(v, u)) for v in self.prev(u)]), self.link_weights(u)))) for u in self.nodes]), self.f())

    def component(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], WeightedDirectedGraph(dict([(u, (self.node_weights(u), (dict(), dict())))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, dict([(v, self.link_weights(v, n))]))
                else:
                    res.add((n, self.node_weights(n)), dict([(v, self.link_weights((v, n)))])), queue.append(n)
            for n in self.prev(v):
                if n in res.nodes:
                    res.connect(v, dict([(n, self.link_weights(n, v))]))
                else:
                    res.add((n, self.node_weights(n)), points_to_weights=dict([(v, self.link_weights((n, v)))])), queue.append(n)
        return res

    def subgraph(self, u: Node):
        if u not in self.nodes:
            raise ValueError("Unrecognized node!")
        queue, res = [u], WeightedDirectedGraph(dict([(u, (self.node_weights(u), (dict(), dict())))]), self.f())
        while queue:
            v = queue.pop(0)
            for n in self.next(v):
                if n in res.nodes:
                    res.connect(n, dict([(v, self.link_weights(v, n))]))
                else:
                    res.add((n, self.node_weights(n)), dict([(v, self.link_weights(v, n))])), queue.append(n)
        return res

    def minimalPath(self, u: Node, v: Node):
        def dfs(x, curr_path, curr_w, total_negative, res_path=None, res_w=0):
            if res_path is None:
                res_path = []
            for y in filter(lambda _y: (x, _y) not in curr_path, self.next(x)):
                if curr_w + self.link_weights(x, y) + total_negative >= res_w and res_path:
                    continue
                if y == v and (curr_w + self.link_weights(x, y) + self.node_weights(y) < res_w or not res_path):
                    res_path, res_w = curr_path + [(x, y)], curr_w + self.link_weights(x, y) + self.node_weights(y)
                curr = dfs(y, curr_path + [(x, y)], curr_w + self.link_weights(x, y) + self.node_weights(y), total_negative - self.link_weights(x, y) * (self.link_weights(x, y) < 0) - self.node_weights(y) * (self.node_weights(y) < 0), res_path, res_w)
                if curr[1] < res_w or not res_path:
                    res_path, res_w = curr
            return res_path, res_w

        if u in self.nodes and v in self.nodes:
            if self.reachable(u, v):
                res = dfs(u, [], self.node_weights(u), sum(self.link_weights(l) for l in self.links if self.link_weights(l) < 0) + sum(self.node_weights(n) for n in self.nodes if self.node_weights(n) < 0))
                return [l[0] for l in res[0]] + [res[0][-1][1]], res[1]
            return [], 0
        raise ValueError('Unrecognized node(s)!')

    def isomorphicFunction(self, other):
        if isinstance(other, WeightedDirectedGraph):
            if len(self.links) != len(other.links) or len(self.nodes) != len(other.nodes):
                return dict()
            this_degrees, other_degrees = dict(), dict()
            this_node_weights, other_node_weights = dict(), dict()
            this_link_weights, other_link_weights = dict(), dict()
            for d in map(tuple, self.degrees().values()):
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in map(tuple, other.degrees().values()):
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            for w in self.link_weights().values():
                if w in this_link_weights:
                    this_link_weights[w] += 1
                else:
                    this_link_weights[w] = 1
            for w in other.link_weights().values():
                if w in other_link_weights:
                    other_link_weights[w] += 1
                else:
                    other_link_weights[w] = 1
            for w in self.node_weights().values():
                if w in this_node_weights:
                    this_node_weights[w] += 1
                else:
                    this_node_weights[w] = 1
            for w in other.node_weights().values():
                if w in other_node_weights:
                    other_node_weights[w] += 1
                else:
                    other_node_weights[w] = 1
            if this_degrees != other_degrees or this_node_weights != other_node_weights or this_link_weights != other_link_weights:
                return dict()
            this_nodes_degrees = {d: [] for d in this_degrees.keys()}
            other_nodes_degrees = {d: [] for d in other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes:
                    if self.degrees(n) == list(d):
                        this_nodes_degrees[d].append(n)
                for n in other.nodes:
                    if other.degrees(n) == list(d):
                        other_nodes_degrees[d].append(n)
            this_nodes_degrees = list(sorted(this_nodes_degrees.values(), key=lambda _p: len(_p)))
            other_nodes_degrees = list(sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility):
                    map_dict += [*zip(group, other_nodes_degrees[i])]
                map_dict = dict(map_dict)
                possible = True
                for n, u in map_dict.items():
                    for m, v in map_dict.items():
                        if self.link_weights(n, m) != other.link_weights(u, v) or self.node_weights(n) != other.node_weights(u):
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return map_dict
            return dict()
        if isinstance(other, (WeightedNodesDirectedGraph, WeightedLinksDirectedGraph)):
            return type(other).isomorphicFunction(other, self)
        return DirectedGraph.isomorphicFunction(self, other)

    def __add__(self, other):
        if not isinstance(other, DirectedGraph):
            raise TypeError(f"Addition not defined between class DirectedGraph and type {type(other).__name__}!")
        if any(self(n) != other(n) for n in self.nodes + other.nodes):
            raise ValueError("Node sorting functions don't match!")
        res = self.copy()
        if isinstance(other, WeightedDirectedGraph):
            for n in other.nodes:
                if n in res.nodes:
                    res.set_weight(n, res.node_weights(n) + other.node_weights(n))
                else:
                    res.add((n, other.node_weights(n)))
            for u, v in other.links:
                if v in res.next(u):
                    res.set_weight((u, v), res.link_weights(u, v) + other.link_weights(u, v))
                else:
                    res.connect(v, dict([(u, other.link_weights(u, v))]))
        elif isinstance(other, WeightedNodesDirectedGraph):
            for n in other.nodes:
                if n in res.nodes:
                    res.set_weight(n, res.node_weights(n) + other.node_weights(n))
                else:
                    res.add((n, other.node_weights(n)))
            for (u, v) in other.links:
                if v not in res.next(u):
                    res.connect(v, dict([(u, 0)]))
        elif isinstance(other, WeightedLinksDirectedGraph):
            for n in other.nodes:
                if n not in res.nodes:
                    res.add((n, 0))
            for u, v in other.links:
                if v in res.next(u):
                    res.set_weight((u, v), res.link_weights(u, v) + other.link_weights(u, v))
                else:
                    res.connect(v, dict([(u, other.link_weights(u, v))]))
        else:
            for n in other.nodes:
                if n not in res.nodes:
                    res.add((n, 0))
            for (u, v) in other.links:
                if v not in res.next(u):
                    res.connect(v, dict([(u, 0)]))
        return res

    def __eq__(self, other):
        if isinstance(other, WeightedDirectedGraph):
            return (self.node_weights(), self.link_weights()) == (other.node_weights(), other.link_weights())
        return False

    def __str__(self):
        return f"({self.node_weights()}, {self.link_weights()})"
