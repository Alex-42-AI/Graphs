from Graphs.General import Node, Link, Dict, SortedKeysDict, SortedList


class UndirectedGraph:
    def __init__(self, *nodes: Node, f=lambda x: x):
        self.__nodes, self.__f = SortedList(f), f
        for n in nodes:
            if n not in self.__nodes: self.__nodes.insert(n)
        self.__links, self.__neighboring, self.__degrees = [], SortedKeysDict(*[(n, SortedList(f=f)) for n in self.__nodes.value()], f=f), SortedKeysDict(*[(n, 0) for n in self.__nodes.value()], f=f)

    def nodes(self):
        return self.__nodes

    def links(self):
        return self.__links

    def neighboring(self, u: Node = None):
        return self.__neighboring if u is None else self.__neighboring[u]

    def degrees(self, u: Node = None):
        return self.__degrees if u is None else self.__degrees[u]

    def degrees_sum(self):
        return 2 * len(self.links())

    def add(self, u: Node, *current_nodes: Node):
        if u not in self.nodes():
            res = SortedList(self.__f)
            for c in current_nodes:
                if c in self.nodes() and c not in res: res.insert(c)
            self.__degrees[u] = len(res)
            for v in res.value():
                self.__degrees[v] += 1
                self.__links.append(Link(v, u)), self.__neighboring[v].insert(u)
            self.__nodes.insert(u)
            self.__neighboring[u] = res

    def remove(self, n: Node, *rest: Node):
        for u in (n,) + rest:
            if u in self.nodes():
                for v in self.neighboring(u).value():
                    self.__degrees[v] -= 1
                    self.__links.remove(Link(v, u)), self.__neighboring[v].remove(u)
                self.__nodes.remove(u), self.__degrees.pop(u), self.__neighboring.pop(u)

    def connect(self, u: Node, v: Node, *rest: Node):
        for n in (v,) + rest:
            if u != n and n not in self.neighboring(u) and n in self.nodes():
                self.__degrees[u] += 1
                self.__degrees[n] += 1
                self.__neighboring[u].insert(n), self.__neighboring[n].insert(u), self.__links.append(Link(u, n))

    def disconnect(self, u: Node, v: Node, *rest: Node):
        for n in (v,) + rest:
            if n in self.neighboring(u):
                self.__degrees[u] -= 1
                self.__degrees[n] -= 1
                self.__neighboring[u].remove(n), self.__neighboring[n].remove(u), self.__links.remove(Link(u, n))

    def width(self):
        res = 0
        for u in self.nodes().value():
            _res, total, queue = 0, SortedList(self.__f), [u]
            total.insert(u)
            while queue:
                u = queue.pop(0)
                for v in filter(lambda x: x not in total, self.neighboring(u).value()): total.insert(v), queue.append(v)
                _res += 1
            if _res > res: res = _res
        return res

    def complementary(self):
        res = UndirectedGraph(*self.nodes().value())
        for i, n in enumerate(self.nodes().value()):
            for j in range(i + 1, len(self.nodes())):
                if self.nodes()[j] not in self.neighboring(n): res.connect(n, self.nodes()[j])
        return res

    def copy(self):
        res = UndirectedGraph(*self.nodes().value())
        for n in self.nodes().value():
            if self.degrees(n): res.connect(n, *self.neighboring(n).value())
        return res

    def connection_components(self):
        if len(self.nodes()) in (0, 1): return [self.nodes()]
        components, queue, total, k, n = [[self.nodes()[0]]], [self.nodes()[0]], SortedList(self.__f), 1, len(self.nodes())
        total.insert(self.nodes()[0])
        while k < n:
            while queue:
                u = queue.pop(0)
                for v in filter(lambda x: x not in total, self.neighboring(u).value()):
                    components[-1].append(v), queue.append(v), total.insert(v)
                    k += 1
                    if k == n: return components
            if k < n:
                new = [[n for n in self.nodes().value() if n not in total][0]]
                components.append(new), total.insert(new[0])
                k, queue = k + 1, [new[0]]
                if k == n: return components
        return components

    def connected(self):
        if len(self.links()) < len(self.nodes()) - 1: return False
        if 2 * len(self.links()) > (len(self.nodes()) - 1) * (len(self.nodes()) - 2) or len(self.nodes()) == 1: return True
        queue, total, k, n = [self.nodes()[0]], SortedList(self.__f), 1, len(self.nodes())
        total.insert(self.nodes()[0])
        while queue:
            u = queue.pop(0)
            for v in filter(lambda x: x not in total and x in self.neighboring(u), self.nodes().value()):
                total.insert(v), queue.append(v)
                k += 1
            if k == n: return True
        return False

    def tree(self):
        if len(self.nodes()) != len(self.links()) + 1: return False
        nodes, duplicates = SortedList(self.__f), SortedList(self.__f)
        for l in self.links():
            if l[0] not in nodes:
                nodes.insert(l[0])
            else:
                if l[1] in duplicates: return False
                duplicates.insert(l[0])
            if l[1] not in nodes:
                nodes.insert(l[1])
            else:
                if l[0] in duplicates: return False
                duplicates.insert(l[1])
        return True

    def reachable(self, u: Node, v: Node):
        if u not in self.nodes() or v not in self.nodes(): raise Exception('Unrecognized node(s).')
        if u == v: return True
        total, queue = SortedList(self.__f), [u]
        total.insert(u)
        while queue:
            n = queue.pop(0)
            for m in filter(lambda x: x not in total, self.neighboring(n).value()):
                if m == v: return True
                total.insert(m), queue.append(m)
        return False

    def component(self, u: Node):
        queue, res = [u], UndirectedGraph(u)
        while queue:
            v = queue.pop(0)
            for n in self.neighboring(v).value():
                if n in res.nodes():
                    res.connect(v, n)
                else:
                    res.add(n, v), queue.append(n)
        return res

    def cut_nodes(self):
        def dfs(u: Node, l: int):
            colors[u], levels[u], min_back, is_root, count, is_cut = 1, l, l, not l, 0, False
            for v in self.neighboring(u).value():
                if not colors[v]:
                    count += 1
                    b = dfs(v, l + 1)
                    if b >= l and not is_root: is_cut = True
                    min_back = min(min_back, b)
                if colors[v] == 1 and levels[v] < min_back and levels[v] + 1 != l: min_back = levels[v]
            if is_cut or is_root and count > 1: res.append(u)
            colors[u] = 2
            return min_back

        levels = SortedKeysDict(*[(n, 0) for n in self.nodes().value()], f=self.__f)
        colors, res = levels.copy(), []
        dfs(self.nodes()[0], 0)
        return res

    def bridge_links(self):
        def dfs(u: Node, l: int):
            colors[u], levels[u], min_back = 1, l, l
            for v in self.neighboring(u).value():
                if not colors[v]:
                    b = dfs(v, l + 1)
                    if b > l:
                        res.append(Link(u, v))
                    else:
                        min_back = min(min_back, b)
                if colors[v] == 1 and levels[v] < min_back and levels[v] + 1 != l: min_back = levels[v]
            colors[u] = 2
            return min_back

        levels, res = SortedKeysDict(*[(n, 0) for n in self.nodes().value()], f=self.__f), []
        colors = levels.copy()
        dfs(self.nodes()[0], 0)
        return res

    def full(self):
        return 2 * len(self.links()) == len(self.nodes()) * (len(self.nodes()) - 1)

    def get_shortest_path(self, u: Node, v: Node):
        if u not in self.nodes() or v not in self.nodes(): raise Exception('Unrecognized node(s)!')
        previous = SortedKeysDict(*[(n, None) for n in self.nodes().value()], f=self.__f)
        queue, total = [u], SortedList(self.__f)
        total.insert(u), previous.pop(u)
        while queue:
            n = queue.pop(0)
            if n == v:
                res, curr_node = [], n
                while curr_node != u:
                    res.insert(0, Link(previous[curr_node], curr_node))
                    curr_node = previous[curr_node]
                return res
            for m in filter(lambda x: x not in total, self.neighboring(n).value()):
                queue.append(m), total.insert(m)
                previous[m] = n

    def shortest_path_length(self, u: Node, v: Node):
        if u not in self.nodes() or v not in self.nodes(): raise Exception('Unrecognized node(s).')
        distances = SortedKeysDict(*[(n, 0) for n in self.nodes().value()], f=self.__f)
        queue, total = [u], SortedList(self.__f)
        total.insert(u)
        while queue:
            n = queue.pop(0)
            for m in filter(lambda x: x not in total, self.neighboring(n).value()):
                if m == v: return 1 + distances[n]
                queue.append(m), total.insert(m)
                distances[m] = distances[n] + 1
        return float('inf')

    def euler_tour_exists(self):
        for n in self.nodes().value():
            if self.degrees(n) % 2: return False
        return self.connected()

    def euler_walk_exists(self, u: Node, v: Node):
        for n in self.nodes().value():
            if self.degrees(n) % 2 and n not in [u, v]: return False
        return self.degrees(u) % 2 + self.degrees(v) % 2 == [2, 0][u == v] and self.connected()

    def euler_tour(self):
        if self.euler_tour_exists():
            u, v = self.links()[0][0], self.links()[0][1]
            self.disconnect(u, v)
            res = self.euler_walk(u, v)
            self.connect(u, v)
            return res
        return False

    def euler_walk(self, u: Node, v: Node):
        def dfs(x, stack):
            for y in self.neighboring(x).value():
                if Link(x, y) not in result + stack:
                    if y == n:
                        stack.append(Link(x, y))
                        for j in range(len(stack)): result.insert(i + j, stack[j])
                        return
                    dfs(y, stack + [Link(x, y)])

        if u in self.nodes() and v in self.nodes():
            if self.euler_walk_exists(u, v):
                result = self.get_shortest_path(u, v)
                for i, l in enumerate(result):
                    n = l[0]
                    dfs(n, [])
                return result
            return False
        raise Exception('Unrecognized nodes!')

    def clique(self, n: Node, *nodes: Node):
        res = SortedList()
        for u in nodes:
            if u not in res and u in self.nodes(): res.insert(u)
        if not res: return True
        nodes = res.value()
        if any(u not in self.neighboring(n) and u in nodes for u in nodes): return False
        return self.clique(*nodes)

    def interval_sort(self):
        if not self.links(): return self.nodes().value()
        if not self.connected():
            res = []
            for c in self.connection_components():
                r = self.component(c[0]).interval_sort()
                if not r: return []
                res += r
            return res
        if len(self.nodes()) < 3 or self.full(): return self.nodes().value()
        res = []
        for n in self.nodes().value():
            if self.clique(n, *self.neighboring(n).value()):
                queue, total, res, continuer = [n], SortedList(self.__f), [n], False
                total.insert(n)
                while queue:
                    u, can_be = queue.pop(0), True
                    for v in filter(lambda x: x not in total, self.neighboring(u).value()):
                        can_be = False
                        if self.clique(v, *filter(lambda x: x not in total, self.neighboring(v).value())):
                            can_be = True
                            queue.append(v), total.insert(v), res.append(v)
                            break
                    if not can_be:
                        res, continuer = [], True
                        break
                if continuer: continue
        return res

    def cliques(self, k: int):
        from itertools import permutations
        k = abs(k)
        if not k: return [[]]
        if k > len(self.nodes()): return []
        if k == 1: return list(map(list, self.nodes().value()))
        if k == len(self.nodes()): return [[], [self.nodes()]][self.full()]
        result = []
        for p in permutations(self.nodes().value(), k):
            can = True
            for i, _n in enumerate(p):
                for j in range(i + 1, len(p)):
                    if Link(_n, p[j]) not in self.links():
                        can = False
                        break
                if not can: break
            if can:
                exists = False
                for clique in result:
                    if all(_n in clique for _n in p):
                        exists = True
                        break
                if not exists: result.append(list(p))
        return result

    def chromaticNumberNodes(self):
        def helper(res):
            if not self.nodes(): return res
            nodes = list(map(lambda x: [x], self.nodes().value()))
            for anti_clique in self.independentSet():
                neighbors = SortedKeysDict(*[(n, self.neighboring(n).value()) for n in anti_clique], f=self.__f)
                for n in anti_clique: self.remove(n)
                curr = helper(res + [anti_clique])
                for n in anti_clique: self.add(n, *neighbors[n])
                if len(curr) < len(nodes): nodes = curr
            return nodes

        s = self.interval_sort()
        if s:
            result, total = [[s[0]]], SortedList(self.__f)
            total.insert(s[0])
            for u in filter(lambda x: x not in total, s[1:]):
                found = False
                for r in range(len(result)):
                    if all(v not in self.neighboring(u) for v in result[r]):
                        result[r].append(u)
                        found = True
                        break
                if not found: result.append([u])
            return result
        if self.tree():
            queue, colors, c0, c1, total = [self.nodes()[0]], SortedKeysDict(*[(n, 0) for n in self.nodes()],
                                                                             f=self.__f), [], [], SortedList(self.__f)
            while queue:
                u = queue.pop(0)
                for v in filter(lambda x: x not in total, self.neighboring(u).value()):
                    colors[v] = 1 - colors[u]
                    queue.append(v), total.insert(v)
            for n, c in colors.items().value():
                if c:
                    c1.append(n)
                else:
                    c0.append(n)
            return [c0, c1]
        return helper([])

    def chromaticNumberLinks(self):
        res_graph = UndirectedGraph(*[Node(l) for l in self.links()])
        for n in res_graph.nodes().value():
            for m in res_graph.nodes().value():
                if m != n and (n.value()[0] in m.value() or n.value()[1] in m.value()): res_graph.connect(n, m)
        return res_graph.chromaticNumberNodes()

    def pathWithLength(self, u: Node, v: Node, length: int):
        def dfs(x: Node, l: int, stack: [Link]):
            if not l: return (False, stack)[x == v]
            for y in filter(lambda _x: Link(x, _x) not in stack, self.neighboring(x).value()):
                res = dfs(y, l - 1, stack + [Link(x, y)])
                if res: return res
            return False

        tmp = self.get_shortest_path(u, v)
        if len(tmp) > length: return False
        if length == len(tmp): return tmp
        return dfs(u, length, [])

    def loopWithLength(self, length: int):
        if abs(length) < 3: raise False
        for l in self.links():
            u, v = l
            self.disconnect(u, v)
            res = self.pathWithLength(v, u, abs(length) - 1)
            self.connect(u, v)
            if res: return [l] + res
        return False

    def vertexCover(self):
        nodes = self.nodes().copy()

        def helper(curr, i=0):
            if not self.links(): return [curr.copy()]
            result, j = [nodes], 1
            for u in nodes.value()[i:]:
                neighbors = self.neighboring(u).value()
                self.remove(u), curr.insert(u)
                res = helper(curr, i + j)
                self.add(u, *neighbors), curr.remove(u)
                if len(res[0]) == len(result[0]):
                    result += res
                elif len(res[0]) < len(result[0]):
                    result = res
                j += 1
            return result

        return helper(SortedList(self.__f))

    def dominatingSet(self):
        nodes = self.nodes().copy()

        def helper(curr, total=SortedList(), i=0):
            if total == self.nodes(): return [curr.copy()]
            result, j = [nodes], 1
            for u in nodes.value()[i:]:
                new = SortedList()
                curr.insert(u), new.insert(u)
                for n in self.neighboring(u).value():
                    if n not in total: new.insert(n)
                res = helper(curr, total + new, i + j)
                if len(res[0]) == len(result[0]):
                    result += res
                elif len(res[0]) < len(result[0]):
                    result = res
                curr.remove(u)
                j += 1
            return result

        return helper(SortedList())

    def independentSet(self):
        result = []
        for res in self.vertexCover(): result.append(list(filter(lambda x: x not in res, self.nodes().value())))
        return result

    def hamiltonTourExists(self):
        def dfs(x):
            if 2 * len(self.links()) > (len(self.nodes()) - 2) * (len(self.nodes()) - 1) + 3: return True
            if any(self.degrees(n) <= 1 for n in self.nodes().value()) or not self.connected(): return False
            if all(2 * self.degrees(n) >= len(self.nodes()) for n in self.nodes().value()) or 2 * len(self.links()) > (
                    len(self.nodes()) - 1) * (len(self.nodes()) - 2) + 2: return True
            if all(y not in self.nodes() for y in can_end_in): return False
            tmp = self.neighboring(x).value()
            self.remove(x)
            for y in tmp:
                res = dfs(y)
                if res:
                    self.add(x, *tmp)
                    return True
            self.add(x, *tmp)
            return False

        u = self.nodes()[0]
        can_end_in = self.neighboring(u).value()
        return dfs(u)

    def hamiltonWalkExists(self, u: Node, v: Node):
        if v in self.neighboring(u): return True if all(
            n in (u, v) for n in self.nodes().value()) else self.hamiltonTourExists()
        self.connect(u, v)
        res = self.hamiltonTourExists()
        self.disconnect(u, v)
        return res

    def hamiltonTour(self):
        if any(self.degrees(n) < 2 for n in self.nodes().value()) or not self.connected(): return False
        u = self.nodes()[0]
        for v in self.neighboring(u).value():
            res = self.hamiltonWalk(u, v)
            if res: return res + [u]
        return False

    def hamiltonWalk(self, u: Node = None, v: Node = None):
        def dfs(x, stack):
            for n in self.nodes().value():
                if self.degrees(n) < 2 - (n in (x, v)): return False
            if not self.nodes(): return stack
            tmp = self.neighboring(x).value()
            self.remove(x)
            for y in tmp:
                if y == v:
                    if [*self.nodes().value()] == [v]:
                        self.add(x, *tmp)
                        return stack + [v]
                    continue
                res = dfs(y, stack + [y])
                self.add(x, *tmp)
                if res: return res
            return False

        if u is None:
            for _u in sorted(self.nodes().value(), key=lambda _x: self.degrees(_x)):
                result = dfs(_u, [_u])
                if result: return result
            return False
        return dfs(u, [u])

    def isomorphic(self, other):
        if isinstance(other, UndirectedGraph):
            if len(self.links()) != len(other.links()) or len(self.nodes()) != len(other.nodes()): return False
            this_degrees, other_degrees = dict(), dict()
            for d in self.degrees().values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.degrees().values():
                if d in other_degrees:
                    other_degrees[d] += 1
                else:
                    other_degrees[d] = 1
            if this_degrees != other_degrees: return False
            this_nodes_degrees, other_nodes_degrees = {d: [] for d in this_degrees.keys()}, {d: [] for d in
                                                                                             other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes().value():
                    if self.degrees(n) == d: this_nodes_degrees[d].append(n)
                    if other.degrees(n) == d: other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(
                sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(
                sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility): map_dict += [*zip(group, other_nodes_degrees[i])]
                possible = True
                for n, u in map_dict:
                    for m, v in map_dict:
                        if (m in self.neighboring(n)) ^ (v in other.neighboring(u)):
                            possible = False
                            break
                    if not possible: break
                if possible: return True
            return False
        return False

    def __reversed__(self):
        return self.complementary()

    def __contains__(self, item):
        return item in self.nodes() or item in self.links()

    def __add__(self, other):
        if isinstance(other, (
        WeightedUndirectedGraph, WeightedNodesUndirectedGraph, WeightedLinksUndirectedGraph)): return other + self
        if isinstance(other, UndirectedGraph):
            res = self.copy()
            for n in other.nodes().value():
                if n not in res.nodes(): res.add(n)
            for l in other.links():
                if l not in res.links(): res.connect(l[0], l[1])
            return res
        raise TypeError(f"Addition not defined between class UndirectedGraph and type {type(other).__name__}!")

    def __eq__(self, other):
        if isinstance(other, UndirectedGraph):
            if len(self.links()) != len(other.links()) or self.nodes() != other.nodes(): return False
            for l in self.links():
                if l not in other.links(): return False
            return True
        return False

    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.nodes().value()) + '}, {' + ', '.join(
            str(l) for l in self.links()) + '})'

    def __repr__(self):
        return str(self)


class WeightedNodesUndirectedGraph(UndirectedGraph):
    def __init__(self, *pairs: (Node, float), f=lambda x: x):
        super().__init__(*[p[0] for p in pairs], f=f)
        self.__node_weights = SortedKeysDict(f=f)
        for (n, w) in pairs:
            if n not in self.__node_weights: self.__node_weights[n] = w

    def node_weights(self, u: Node = None):
        return self.__node_weights[u] if u is not None else self.__node_weights

    def total_nodes_weight(self):
        return sum(self.node_weights().values())

    def copy(self):
        res = WeightedNodesUndirectedGraph(*[(n, self.node_weights(n)) for n in self.nodes().value()])
        for n in self.nodes().value():
            if self.degrees(n): res.connect(n, *self.neighboring(n).value())
        return res

    def add(self, n_w: (Node, float), *current_nodes: Node):
        if n_w[0] not in self.nodes(): self.__node_weights[n_w[0]] = n_w[1]
        super().add(n_w[0], *current_nodes)

    def remove(self, n: Node, *rest: Node):
        for u in (n,) + rest: self.__node_weights.pop(u)
        super().remove(n, *rest)

    def component(self, u: Node):
        queue, res = [u], WeightedNodesUndirectedGraph((u, self.node_weights(u)))
        while queue:
            v = queue.pop(0)
            for n in self.neighboring(v).value():
                if n in res.nodes():
                    res.connect(v, n)
                else:
                    res.add((n, self.node_weights(n)), v), queue.append(n)
        return res

    def minimalPathNodes(self, u: Node, v: Node):
        def dfs(x, curr_path, curr_w, total_negative, res_path=None, res_w=0):
            if res_path is None: res_path = []
            for y in filter(lambda _x: Link(_x, x) not in curr_path, self.neighboring(x).value()):
                if curr_w + self.node_weights(y) + total_negative >= res_w and res_path: continue
                if y == v and (curr_w + self.node_weights(y) < res_w or not res_path): res_path, res_w = curr_path + [
                    Link(x, y)], curr_w + self.node_weights(y)
                curr = dfs(y, curr_path + [Link(x, y)], curr_w + self.node_weights(y),
                           total_negative - self.node_weights(y) * (self.node_weights(y) < 0), res_path, res_w)
                if curr[1] < res_w or not res_path: res_path, res_w = curr
            return res_path, res_w

        if u in self.nodes() and v in self.nodes():
            if self.reachable(u, v): return dfs(u, [], 0, sum(
                self.node_weights(n) for n in self.nodes().value() if self.node_weights(n) < 0))
            return [], 0
        raise ValueError("Unrecognized node(s)!")

    def chromaticNumberNodes(self):
        def helper(res):
            if not self.nodes(): return res
            nodes = list(map(list, self.nodes().value()))
            for anti_clique in self.independentSet():
                weights, neighbors = SortedKeysDict(*[(n, self.node_weights(n)) for n in anti_clique],
                                                    f=self._UndirectedGraph__f), SortedKeysDict(
                    *[(n, self.neighboring(n).value()) for n in anti_clique], f=self._UndirectedGraph__f)
                for n in anti_clique: self.remove(n)
                curr = helper(res + [anti_clique])
                for n in anti_clique: self.add((n, weights[n]), *neighbors[n])
                if len(curr) < len(nodes): nodes = curr
            return nodes

        if self.tree(): return super().chromaticNumberNodes()
        return helper([])

    def vertexCover(self):
        nodes = self.nodes().copy()

        def helper(curr, i=0):
            if not self.links(): return [curr.copy()]
            result, result_sum, j = [nodes], self.total_nodes_weight(), 1
            for u in nodes.value()[i:]:
                neighbors, w = self.neighboring(u).value(), self.node_weights(u)
                self.remove(u), curr.insert(u)
                res = helper(curr, i + j)
                self.add((u, w), *neighbors), curr.remove(u)
                res_sum = sum(self.node_weights(n) for n in res[0])
                if res_sum == result_sum:
                    result += res
                elif res_sum < result_sum:
                    result, result_sum = res, res_sum
                j += 1
            return result

        return helper(SortedList(self.__f))

    def dominatingSet(self):
        nodes = self.nodes().copy()

        def helper(curr, total=SortedList(), i=0):
            if total == self.nodes(): return [curr.copy()]
            result, result_sum, j = [nodes], self.total_nodes_weight(), 1
            for u in nodes.value()[i:]:
                new = SortedList()
                curr.insert(u), new.insert(u)
                for n in self.neighboring(u).value():
                    if n not in total: new.insert(n)
                res = helper(curr, total + new, i + j)
                res_sum = sum(self.node_weights(n) for n in res[0])
                if res_sum == result_sum:
                    result += res
                elif res_sum < result_sum:
                    result, result_sum = res, res_sum
                curr.remove(u)
                j += 1
            return result

        return helper(SortedList())

    def independentSet(self):
        result = []
        for res in super().vertexCover(): result.append(list(filter(lambda x: x not in res, self.nodes().value())))
        return result

    def hamiltonTourExists(self):
        def dfs(x):
            if 2 * len(self.links()) > (len(self.nodes()) - 2) * (len(self.nodes()) - 1) + 3: return True
            if any(self.degrees(n) <= 1 for n in self.nodes().value()) or not self.connected(): return False
            if all(2 * self.degrees(n) >= len(self.nodes()) for n in self.nodes()) or 2 * len(self.links()) > (
                    len(self.nodes()) - 1) * (len(self.nodes()) - 2) + 2: return True
            if all(y not in self.nodes() for y in can_end_in): return False
            tmp, w = self.neighboring(x).value(), self.node_weights(x)
            self.remove(x)
            for y in tmp:
                res = dfs(y)
                if res:
                    self.add((x, w), *tmp)
                    return True
            self.add(x, *tmp)
            return False

        u = self.nodes()[0]
        can_end_in = self.neighboring(u).value()
        return dfs(u)

    def hamiltonWalk(self, u: Node = None, v: Node = None):
        def dfs(x, stack):
            for n in self.nodes().value():
                if self.degrees(n) < 2 - (n in (x, v)): return False
            if not self.nodes(): return stack
            tmp, w = self.neighboring(x).value(), self.node_weights(x)
            self.remove(x)
            for y in tmp:
                if y == v:
                    if [*self.nodes().value()] == [v]:
                        self.add((x, w), *tmp)
                        return stack + [v]
                    continue
                res = dfs(y, stack + [y])
                self.add((x, w), *tmp)
                if res: return res
            return False

        if u is None:
            for _u in sorted(self.nodes().value(), key=lambda _x: self.degrees(_x)):
                result = dfs(_u, [_u])
                if result: return result
            return False
        return dfs(u, [u])

    def isomorphic(self, other: UndirectedGraph):
        if isinstance(other, WeightedNodesUndirectedGraph):
            if len(self.links()) != len(other.links()) or len(self.nodes()) != len(other.nodes()): return False
            this_degrees, other_degrees, this_weights, other_weights = dict(), dict(), dict(), dict()
            for d in self.degrees().values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.degrees().values():
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
            if this_degrees != other_degrees or this_weights != other_weights: return False
            this_nodes_degrees, other_nodes_degrees = {d: [] for d in this_degrees.keys()}, {d: [] for d in
                                                                                             other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes().value():
                    if self.degrees(n) == d: this_nodes_degrees[d].append(n)
                    if other.degrees(n) == d: other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(
                sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(
                sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility): map_dict += [*zip(group, other_nodes_degrees[i])]
                possible = True
                for n, u in map_dict:
                    for m, v in map_dict:
                        if (m in self.neighboring(n)) ^ (v in other.neighboring(u)) or self.node_weights(
                                n) != other.node_weights(u):
                            possible = False
                            break
                    if not possible: break
                if possible: return True
            return False
        return super().isomorphic(other)

    def __add__(self, other):
        if isinstance(other, WeightedUndirectedGraph): return other + self
        if isinstance(other, WeightedNodesUndirectedGraph):
            res = self.copy()
            for n in other.nodes().value():
                if n in res.nodes():
                    res.__node_weights[n] += other.node_weights(n)
                else:
                    res.add(n, other.node_weights(n))
            for l in other.links(): res.connect(l[0], l[1])
            return res
        if isinstance(other, WeightedLinksUndirectedGraph): return WeightedUndirectedGraph() + self + other
        if isinstance(other, UndirectedGraph):
            res = self.copy()
            for n in other.nodes().value():
                if n not in res.nodes(): res.add(n, 0)
            for l in other.links(): res.connect(l[0], l[1])
            return res
        raise TypeError(
            f"Addition not defined between class WeightedNOdesUndirectedGraph and type {type(other).__name__}!")

    def __eq__(self, other):
        if isinstance(other, WeightedNodesUndirectedGraph):
            if self.node_weights() != other.node_weights() or len(self.links()) != len(other.links()): return False
            for l in self.links():
                if l not in other.links(): return False
            return True
        return False

    def __str__(self):
        return '({' + ', '.join(f'{str(n)} -> {self.node_weights(n)}' for n in self.nodes().value()) + '}, ' + str(
            self.links()) + ')'


class WeightedLinksUndirectedGraph(UndirectedGraph):
    def __init__(self, *nodes: Node, f=lambda x: x):
        super().__init__(*nodes, f=f)
        self.__link_weights = Dict()

    def link_weights(self, u_or_l: Node | Link = None, v: Node = None):
        if u_or_l is None:
            return self.__link_weights
        elif isinstance(u_or_l, Node):
            if v is None: return SortedKeysDict(
                *[(n, self.__link_weights[Link(n, u_or_l)]) for n in self.neighboring(u_or_l).value()])
            return self.__link_weights[Link(u_or_l, v)]
        elif isinstance(u_or_l, Link):
            return self.__link_weights[u_or_l]

    def total_links_weight(self):
        return sum(self.link_weights().values())

    def add(self, u: Node, *nodes_weights: (Node, float)):
        if u not in self.nodes():
            res = SortedKeysDict()
            for v, w in nodes_weights:
                if v in self.nodes() and v not in res: res[v] = w
            for w in res.values():
                if not isinstance(w, (int, float)): raise TypeError('Real numerical values expected!')
            super().add(u, *res.keys())
            for v, w in res.items(): self.__link_weights[Link(u, v)] = w

    def remove(self, n: Node, *rest: Node):
        for u in (n,) + rest:
            for v in self.neighboring(u).value(): self.__link_weights.pop(Link(u, v))
        super().remove(n, *rest)

    def connect(self, u: Node, v_w: (Node, float), *nodes_weights: (Node, float)):
        if u in self.nodes():
            for v, w in (v_w,) + nodes_weights:
                if v not in self.neighboring(u): self.__link_weights[Link(u, v)] = w
        super().connect(u, *[p[0] for p in (v_w,) + nodes_weights])

    def disconnect(self, u: Node, v: Node, *rest: Node):
        super().disconnect(u, v, *rest)
        for n in (v,) + rest:
            if Link(u, n) in [l for l in self.link_weights().keys()]: self.__link_weights.pop(Link(u, n))

    def copy(self):
        res = WeightedLinksUndirectedGraph(*self.nodes().value())
        for u in self.nodes().value():
            for v in self.neighboring(u).value(): res.connect(u, (v, self.link_weights(u, v)))
        return res

    def component(self, u: Node):
        queue, res = [u], WeightedLinksUndirectedGraph(u)
        while queue:
            v = queue.pop(0)
            for n in self.neighboring(v).value():
                if n in res.nodes():
                    res.connect(v, (n, self.link_weights(v, n)))
                else:
                    res.add(n, v), queue.append(n)
        return res

    def euler_tour(self):
        if self.euler_tour_exists():
            u, v, w = self.links()[0][0], self.links()[0][1], self.link_weights(self.links()[0])
            self.disconnect(u, v)
            res = self.euler_walk(u, v)
            self.connect(u, (v, w))
            return res
        return False

    def minimal_spanning_tree(self):
        if self.tree(): return self.links(), self.total_links_weight()
        if not self.connected():
            res = []
            for comp in self.connection_components():
                curr = self.component(comp[0])
                res.append(curr.minimal_spanning_tree())
            return res
        if not self.nodes(): return [], 0
        res_links, total, bridge_links = [], SortedList(self._UndirectedGraph__f), SortedList(
            lambda x: self.link_weights(x))
        total.insert(self.nodes()[0])
        for u in self.neighboring(self.nodes()[0]).value(): bridge_links.insert(Link(self.nodes()[0], u))
        k, n = 1, len(self.nodes())
        while k < n:
            u, v, k = bridge_links[0][0], bridge_links[0][1], k + 1
            res_links.append(bridge_links.pop(0))
            if u in total:
                total.insert(v)
                for _v in self.neighboring(v).value():
                    if _v in total:
                        bridge_links.remove(Link(v, _v))
                    else:
                        bridge_links.insert(Link(v, _v))
            else:
                total.insert(u)
                for _u in self.neighboring(u).value():
                    if _u in total:
                        bridge_links.remove(Link(u, _u))
                    else:
                        bridge_links.insert(Link(u, _u))
        return res_links, sum(map(lambda x: self.link_weights(x), res_links))

    def minimalPathLinks(self, u: Node, v: Node):
        def dfs(x, curr_path, curr_w, total_negative, res_path=None, res_w=0):
            if res_path is None: res_path = []
            for y in filter(lambda _y: Link(x, _y) not in curr_path, self.neighboring(x).value()):
                if curr_w + self.link_weights(Link(y, x)) + total_negative >= res_w and res_path: continue
                if y == v and (
                        curr_w + self.link_weights(Link(x, y)) < res_w or not res_path): res_path, res_w = curr_path + [
                    Link(x, y)], curr_w + self.link_weights(Link(x, y))
                curr = dfs(y, curr_path + [Link(x, y)], curr_w + self.link_weights(Link(x, y)),
                           total_negative - self.link_weights(Link(x, y)) * (self.link_weights(Link(x, y)) < 0),
                           res_path, res_w)
                if curr[1] < res_w or not res_path: res_path, res_w = curr
            return res_path, res_w

        if u in self.nodes() and v in self.nodes():
            if self.reachable(u, v): return dfs(u, [], 0, sum(
                self.link_weights(l) for l in self.links() if self.link_weights(l) < 0))
            return [], 0
        raise ValueError('Unrecognized node(s)!')

    def chromaticNumberNodes(self):
        def helper(res):
            if not self.nodes(): return res
            nodes = list(map(list, self.nodes().value()))
            for anti_clique in self.independentSet():
                neighbors = SortedKeysDict(*[(n, self.link_weights(n).items().value()) for n in anti_clique],
                                           f=self._UndirectedGraph__f)
                for n in anti_clique: self.remove(n)
                curr = helper(res + [anti_clique])
                for n in anti_clique: self.add(n, *neighbors[n])
                if len(curr) < len(nodes): nodes = curr
            return nodes

        if self.tree(): return super().chromaticNumberNodes()
        return helper([])

    def vertexCover(self):
        nodes = self.nodes().copy()

        def helper(curr, i=0):
            if not self.links(): return [curr.copy()]
            result, j = [nodes], 1
            for u in nodes.value()[i:]:
                neighbors = self.link_weights(u).items().value()
                self.remove(u), curr.insert(u)
                res = helper(curr, i + j)
                self.add(u, *neighbors), curr.remove(u)
                if len(res[0]) == len(result[0]):
                    result += res
                elif len(res[0]) < len(result[0]):
                    result = res
                j += 1
            return result

        return helper(SortedList(self.__f))

    def hamiltonTourExists(self):
        def dfs(x):
            if 2 * len(self.links()) > (len(self.nodes()) - 2) * (len(self.nodes()) - 1) + 3: return True
            if any(self.degrees(n) <= 1 for n in self.nodes().value()) or not self.connected(): return False
            if all(2 * self.degrees(n) >= len(self.nodes()) for n in self.nodes().value()) or 2 * len(self.links()) > (
                    len(self.nodes()) - 1) * (len(self.nodes()) - 2) + 2: return True
            if all(y not in self.nodes() for y in can_end_in): return False
            tmp, weights = self.neighboring(x).value(), self.link_weights(x)
            self.remove(x)
            for y in tmp:
                res = dfs(y)
                if res:
                    self.add(x, *[(t, weights(x, t)) for t in tmp])
                    return True
            self.add(x, *[(t, weights(x, t)) for t in tmp])
            return False

        u = self.nodes()[0]
        can_end_in = self.neighboring(u).value()
        return dfs(u)

    def hamiltonWalkExists(self, u: Node, v: Node):
        if v in self.neighboring(u): return True if all(
            n in (u, v) for n in self.nodes().value()) else self.hamiltonTourExists()
        self.connect(u, (v, 0))
        res = self.hamiltonTourExists()
        self.disconnect(u, v)
        return res

    def hamiltonWalk(self, u: Node = None, v: Node = None):
        def dfs(x, stack):
            for n in self.nodes().value():
                if self.degrees(n) < 2 - (n in (x, v)): return False
            if not self.nodes(): return stack
            tmp, weights = self.neighboring(x).value(), self.link_weights(x)
            self.remove(x)
            for y in tmp:
                if y == v:
                    if [*self.nodes().value()] == [v]:
                        self.add(x, *[(t, weights(x, t)) for t in tmp])
                        return stack + [v]
                    continue
                res = dfs(y, stack + [y])
                self.add(x, *[(t, weights(x, t)) for t in tmp])
                if res: return res
            return False

        if u is None:
            for _u in sorted(self.nodes().value(), key=lambda _x: self.degrees(_x)):
                result = dfs(_u, [_u])
                if result: return result
            return False
        return dfs(u, [u])

    def isomorphic(self, other: UndirectedGraph):
        if isinstance(other, WeightedLinksUndirectedGraph):
            if len(self.links()) != len(other.links()) or len(self.nodes()) != len(other.nodes()): return False
            this_degrees, other_degrees, this_weights, other_weights = dict(), dict(), dict(), dict()
            for d in self.degrees().values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.degrees().values():
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
            if this_degrees != other_degrees or this_weights != other_weights: return False
            this_nodes_degrees, other_nodes_degrees = {d: [] for d in this_degrees.keys()}, {d: [] for d in
                                                                                             other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes().value():
                    if self.degrees(n) == d: this_nodes_degrees[d].append(n)
                    if other.degrees(n) == d: other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(
                sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(
                sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility): map_dict += [*zip(group, other_nodes_degrees[i])]
                possible = True
                for n, u in map_dict:
                    for m, v in map_dict:
                        if self.link_weights(Link(n, m)) != other.link_weights(Link(u, v)):
                            possible = False
                            break
                    if not possible: break
                if possible: return True
            return False
        return super().isomorphic(other)

    def __add__(self, other):
        if isinstance(other, (WeightedUndirectedGraph, WeightedNodesUndirectedGraph)): return other + self
        if isinstance(other, WeightedLinksUndirectedGraph):
            res = self.copy()
            for n in other.nodes().value():
                if n not in res.nodes(): res.add(n)
            for l in other.links():
                if l in res.links():
                    res.__link_weights[l] += other.link_weights(l)
                else:
                    res.connect(l[0], (l[1], other.link_weights(l)))
            return res
        if isinstance(other, UndirectedGraph):
            res = self.copy()
            for n in other.nodes().value():
                if n not in res.nodes(): res.add(n)
            for l in other.links():
                if l not in res.links(): res.connect(l[0], (l[1], 0))
            return res
        raise TypeError(
            f"Addition not defined between class WeightedLinksUndirectedGraph and type {type(other).__name__}!")

    def __eq__(self, other):
        if isinstance(other,
                      WeightedLinksUndirectedGraph): return self.nodes() == other.nodes() and self.link_weights() == other.link_weights()
        return False

    def __str__(self):
        return '({' + ', '.join(str(n) for n in self.nodes().value()) + '}, ' + str(self.link_weights()) + ')'


class WeightedUndirectedGraph(WeightedNodesUndirectedGraph, WeightedLinksUndirectedGraph):
    def __init__(self, *pairs: (Node, float), f=lambda x: x):
        WeightedNodesUndirectedGraph.__init__(self, *pairs, f=f)

    def total_weight(self):
        return self.total_nodes_weight() + self.total_links_weight()

    def add(self, n_w: (Node, float), *nodes_link_weights: (Node, float)):
        if n_w[0] not in self.node_weights(): self._WeightedNodesUndirectedGraph__node_weights[n_w[0]] = n_w[1]
        WeightedLinksUndirectedGraph.add(n_w[0], *nodes_link_weights)

    def remove(self, u: Node, *rest: Node):
        for n in (u,) + rest: self._WeightedNodesUndirectedGraph__node_weights.pop(n)
        WeightedLinksUndirectedGraph.remove(self, u, *rest)

    def connect(self, u: Node, v_w: (Node, float), *nodes_weights: (Node, float)):
        WeightedLinksUndirectedGraph.connect(self, u, v_w, *nodes_weights)

    def disconnect(self, u: Node, v: Node, *rest: Node):
        WeightedLinksUndirectedGraph.disconnect(self, u, v, *rest)

    def copy(self):
        res = WeightedUndirectedGraph(*self.node_weights().items())
        for u in self.nodes().value():
            if self.degrees(u): res.connect(u, *self.link_weights(u).items())
        return res

    def component(self, u: Node):
        queue, res = [u], WeightedUndirectedGraph((u, self.node_weights(u)))
        while queue:
            v = queue.pop(0)
            for n in self.neighboring(v).value():
                if n in res.nodes():
                    res.connect(v, (n, self.link_weights(v, n)))
                else:
                    res.add((n, self.node_weights(n)), v), queue.append(n)
        return res

    def minimalPath(self, u: Node, v: Node):
        def dfs(x, curr_path, curr_w, total_negative, res_path=None, res_w=0):
            if res_path is None: res_path = []
            for y in filter(lambda _y: Link(x, _y) not in curr_path, self.neighboring(x).value()):
                if curr_w + self.link_weights(Link(y, x)) + total_negative >= res_w and res_path: continue
                if y == v and (curr_w + self.link_weights(Link(x, y)) + self.node_weights(
                    y) < res_w or not res_path): res_path, res_w = curr_path + [Link(x, y)], curr_w + self.link_weights(
                    Link(x, y)) + self.node_weights(y)
                curr = dfs(y, curr_path + [Link(x, y)], curr_w + self.link_weights(Link(x, y)) + self.node_weights(y),
                           total_negative - self.link_weights(Link(x, y)) * (
                                       self.link_weights(Link(x, y)) < 0) - self.node_weights(y) * (
                                       self.node_weights(y) < 0), res_path, res_w)
                if curr[1] < res_w or not res_path: res_path, res_w = curr
            return res_path, res_w

        if u in self.nodes() and v in self.nodes():
            if self.reachable(u, v): return dfs(u, [], self.node_weights(u), sum(
                self.link_weights(l) for l in self.links() if self.link_weights(l) < 0) + sum(
                self.node_weights(n) for n in self.nodes() if self.node_weights(n) < 0))
            return [], 0
        raise ValueError('Unrecognized node(s)!')

    def chromaticNumberNodes(self):
        def helper(res):
            if not self.nodes(): return res
            nodes = list(map(list, self.nodes().value()))
            for anti_clique in self.independentSet():
                weights, neighbors = SortedKeysDict(*[(n, self.node_weights(n)) for n in anti_clique],
                                                    f=self._UndirectedGraph__f), SortedKeysDict(
                    *[(n, self.link_weights(n).items().value()) for n in anti_clique], f=self._UndirectedGraph__f)
                for n in anti_clique: self.remove(n)
                curr = helper(res + [anti_clique])
                for n in anti_clique: self.add((n, weights[n]), *neighbors[n])
                if len(curr) < len(nodes): nodes = curr
            return nodes

        if self.tree():  UndirectedGraph(self).chromaticNumberNodes()
        return helper([])

    def vertexCover(self):
        nodes = self.nodes().copy()

        def helper(curr, i=0):
            if not self.links(): return [curr.copy()]
            result, result_sum, j = [nodes], self.total_nodes_weight(), 1
            for u in nodes.value()[i:]:
                neighbors, w = self.link_weights(u).items().value(), self.node_weights(u)
                self.remove(u), curr.insert(u)
                res = helper(curr, i + j)
                self.add((u, w), *neighbors), curr.remove(u)
                res_sum = sum(self.node_weights(n) for n in res[0])
                if res_sum == result_sum:
                    result += res
                elif res_sum < result_sum:
                    result, result_sum = res, res_sum
                j += 1
            return result

        return helper(SortedList(self.__f))

    def independentSet(self):
        result = []
        for res in UndirectedGraph.vertexCover(self): result.append(
            list(filter(lambda x: x not in res, self.nodes().value())))
        return result

    def isomorphic(self, other: UndirectedGraph):
        if isinstance(other, WeightedUndirectedGraph):
            if len(self.links()) != len(other.links()) or len(self.nodes()) != len(other.nodes()): return False
            this_degrees, other_degrees, this_node_weights, other_node_weights, this_link_weights, other_link_weights = dict(), dict(), dict(), dict(), dict(), dict()
            for d in self.degrees().values():
                if d in this_degrees:
                    this_degrees[d] += 1
                else:
                    this_degrees[d] = 1
            for d in other.degrees().values():
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
            if this_degrees != other_degrees or this_node_weights != other_node_weights or this_link_weights != other_link_weights: return False
            this_nodes_degrees, other_nodes_degrees = {d: [] for d in this_degrees.keys()}, {d: [] for d in
                                                                                             other_degrees.keys()}
            for d in this_degrees.keys():
                for n in self.nodes().value():
                    if self.degrees(n) == d: this_nodes_degrees[d].append(n)
                    if other.degrees(n) == d: other_nodes_degrees[d].append(n)
            this_nodes_degrees, other_nodes_degrees = list(
                sorted(this_nodes_degrees.values(), key=lambda _p: len(_p))), list(
                sorted(other_nodes_degrees.values(), key=lambda _p: len(_p)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_degrees]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility): map_dict += [*zip(group, other_nodes_degrees[i])]
                possible = True
                for n, u in map_dict:
                    for m, v in map_dict:
                        if self.link_weights(Link(n, m)) != other.link_weights(Link(u, v)) or self.node_weights(
                                n) != other.node_weights(u):
                            possible = False
                            break
                    if not possible: break
                if possible: return True
            return False
        if isinstance(other, WeightedNodesUndirectedGraph):
            return WeightedNodesUndirectedGraph.isomorphic(self, other)
        if isinstance(other, WeightedLinksUndirectedGraph):
            return WeightedLinksUndirectedGraph.isomorphic(self, other)
        return UndirectedGraph.isomorphic(self, other)

    def __add__(self, other):
        res = self.copy()
        if isinstance(other, WeightedUndirectedGraph):
            for n in other.nodes().value():
                if n in res.nodes():
                    res._WeightedNodesUndirectedGraph__node_weights[n] += other.node_weights(n)
                else:
                    res.add((n, other.node_weights(n)))
            for u in other.nodes().value():
                for v in other.neighboring(u).value():
                    if v in res.neighboring(u):
                        res._WeightedNodesUndirectedGraph__link_weights[Link(u, v)] += other.link_weights(u, v)
                    else:
                        res.connect(u, (v, other.link_weights(u, v)))
        elif isinstance(other, WeightedNodesUndirectedGraph):
            for n in other.nodes().value():
                if n in res.nodes():
                    res._WeightedNodesUndirectedGraph__node_weights[n] += other.node_weights(n)
                else:
                    res._WeightedNodesUndirectedGraph__node_weights = other.node_weights(n)
            for u in other.nodes().value():
                for v in other.neighboring(u).value():
                    if v not in res.neighboring(u): res.connect(u, (v, 0))
        elif isinstance(other, WeightedLinksUndirectedGraph):
            for n in other.nodes().value():
                if n not in res.nodes(): res.add((n, 0))
            for u in other.nodes().value():
                for v in other.neighboring(u).value():
                    if v in res.neighboring(u):
                        res._WeightedNodesUndirectedGraph__link_weights[Link(u, v)] += other.link_weights(u, v)
                    else:
                        res.connect(u, (v, other.link_weights(u, v)))
        elif isinstance(other, UndirectedGraph):
            for n in other.nodes().value():
                if n not in res.nodes(): res.add((n, 0))
            for u in other.nodes().value():
                for v in other.neighboring(u).value():
                    if v not in res.neighboring(u): res.connect(u, (v, 0))
        else:
            raise TypeError(
                f"Addition not defined between class WeightedUndirectedGraph and type {type(other).__name__}!")
        return res

    def __eq__(self, other):
        if isinstance(other, WeightedUndirectedGraph): return (self.node_weights(), self.link_weights()) == (
        other.node_weights(), other.link_weights())
        return False

    def __str__(self):
        return f"({self.node_weights()}, {self.link_weights()})"
