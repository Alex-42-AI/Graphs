from Graphs.General import Node, SortedKeysDict, SortedList, BinNode


class BinTree:
    def __init__(self, root=None):
        self.root = root if isinstance(root, BinNode) else BinNode(root)

    def copy(self, curr_from: BinNode, curr_to: BinNode):
        if curr_from is None or curr_to is None: return
        if curr_from.left is not None:
            self.copy(curr_from.left, curr_to.left)
            curr_to.left = curr_from.left
        if curr_from.right is not None:
            self.copy(curr_from.right, curr_to.right)
            curr_to.right = curr_from.right

    def left(self):
        return BinTree(self.root.left)

    def right(self):
        return BinTree(self.root.right)

    def nodes_on_level(self, level: int):
        if level > self.get_height() or level < 0: return []

        def helper(l, curr_node: BinNode):
            if not l: return [curr_node]
            if curr_node.left is None and curr_node.right is None: return []
            left, right = [], []
            if curr_node.left is not None: left = helper(l - 1, curr_node.left)
            if curr_node.right is not None: right = helper(l - 1, curr_node.right)
            return left + right

        return helper(level, self.root)

    def width(self):
        res = 0
        for i in range(self.get_height()): res = max(len(self.nodes_on_level(i)), res)
        return res

    def get_height(self):
        def helper(curr_node):
            if curr_node is None: return -1
            return 1 + max(helper(curr_node.left), helper(curr_node.right))

        return helper(self.root)

    def count_leaves(self):
        def helper(curr_node):
            if curr_node is None: return 0
            if curr_node.left is None and curr_node.right is None: return 1
            return helper(curr_node.left) + helper(curr_node.right)

        return helper(self.root)

    def count_nodes(self):
        def helper(curr_node):
            if curr_node is None: return 0
            if curr_node.left is None and curr_node.right is None: return 1
            return (curr_node.value() is not None) + helper(curr_node.left) + helper(curr_node.right)

        return helper(self.root)

    def code_in_morse(self, v):
        def helper(tree):
            if tree.root.value() is False: return
            if tree.root.left is not None:
                if tree.root.left.value() == v: return '.'
            res = helper(tree.left())
            if res: return '. ' + res
            if tree.root.right is not None:
                if tree.root.right.value() == v: return '-'
            res = helper(tree.right())
            if res: return '- ' + res

        return helper(self)

    def encode(self, message: str):
        res = ''
        for c in message.upper():
            if c in self:
                res += self.code_in_morse(c) + '   '
            else:
                res += c + '  '
        return res[:-2]

    def invert(self):
        def dfs(node):
            if node is None: return
            dfs(node.left), dfs(node.right)
            node.left, node.right = node.right, node.left

        dfs(self.root)

    def __invert__(self):
        self.invert()

    def __contains__(self, item):
        if self.root.value() == item: return True
        if self.root.left is not None and item in self.left(): return True
        if self.root.right is not None: return item in self.right()

    def __eq__(self, other):
        if self.root.left ^ other.root.left: return False
        if self.root.right ^ other.root.right: return False
        return (self.root, self.left(), self.right()) == (other.root, other.left(), other.right())

    def __bool__(self):
        return self.root is not None

    def __preorder_print(self):
        def dfs(start: BinNode, traversal: [BinNode]):
            if start is not None:
                traversal += [start]
                traversal = dfs(start.left, traversal)
                traversal = dfs(start.right, traversal)
            return traversal

        return dfs(self.root, [])

    def __in_order_print(self):
        def dfs(start: BinNode, traversal: [BinNode]):
            if start is not None:
                traversal = dfs(start.left, traversal)
                traversal += [start]
                traversal = dfs(start.right, traversal)
            return traversal

        return dfs(self.root, [])

    def __post_order_print(self):
        def dfs(start: BinNode, traversal: [BinNode]):
            if start is not None:
                traversal = dfs(start.left, traversal)
                traversal = dfs(start.right, traversal)
                traversal += [start]
            return traversal

        return dfs(self.root, [])

    def print(self, traversal_type: str = 'in-order'):
        if traversal_type.lower() == 'preorder':
            print(self.__preorder_print())
        elif traversal_type.lower() == 'in-order':
            print(self.__in_order_print())
        elif traversal_type.lower() == 'post-order':
            print(self.__post_order_print())
        else:
            print('Traversal type ' + str(traversal_type) + ' is not supported!')

    def __str__(self):
        return str(self.__in_order_print())

    def __repr__(self):
        return str(self)


class Tree:
    def __init__(self, root: Node, *descendants: Node, f=lambda x: x):
        self.__root, self.__f = root, f
        if root in descendants: raise ValueError('Can\'t have a node twice in a tree!')
        for i in range(len(descendants)):
            for j in range(i + 1, len(descendants)):
                if descendants[i] == descendants[j]: raise ValueError('Can\'t have a node twice in a tree!')
        self.__hierarchy, self.__nodes, self.__links, self.__leaves = SortedKeysDict((self.__root, SortedList(f)),
                                                                                     f=self.__f) + SortedKeysDict(
            *[(n, SortedList(f)) for n in descendants], f=self.__f), SortedList(f), [(root, n) for n in
                                                                                     descendants], SortedList(f)
        for n in [root] + [*descendants]: self.__nodes.insert(n)
        if descendants:
            for d in descendants: self.__leaves.insert(d), self.__hierarchy[root].insert(d)
        else:
            self.__leaves.insert(root)

    def root(self):
        return self.__root

    def nodes(self):
        return self.__nodes

    def links(self):
        return self.__links

    def leaves(self):
        return self.__leaves

    def hierarchy(self, u: Node = None):
        return self.__hierarchy if u is None else self.__hierarchy[u]

    def descendants(self, n: Node):
        return self.hierarchy(n)

    def add_nodes_to(self, curr: Node, u: Node, *rest: Node):
        if curr not in self.nodes(): raise Exception('Node not found!')
        if curr in self.leaves(): self.__leaves.remove(curr)
        for v in [u] + [*rest]:
            if v not in self.nodes():
                self.__nodes.insert(v)
                self.__hierarchy[curr].insert(v)
                self.__links.append((curr, v))
                self.__leaves.insert(v)
                self.__hierarchy[v] = SortedList(self.__f)

    def copy(self):
        res = Tree(self.root(), *self.descendants(self.root()).value())
        queue = self.descendants(res.root()).value()
        while queue:
            u = queue.pop(0)
            res_descendants = self.descendants(u).value()
            if res_descendants:
                res.add_nodes_to(u, *res_descendants)
                queue += res_descendants
        return res

    def subtree(self, u: Node):
        queue, res = [u], Tree(u)
        while queue:
            v = queue.pop(0)
            for n in self.descendants(v).value(): res.add_nodes_to(v, n), queue.append(n)
        return res

    def extend_tree_at(self, n: Node, tree):
        if n not in self.nodes(): raise Exception('Node not found!')
        if not isinstance(tree, Tree): raise TypeError('Tree expected!')
        self.add_nodes_to(n, tree.root())
        queue = [tree.root()]
        while queue:
            u = queue.pop(0)
            res = list(filter(lambda x: x not in self.nodes(), tree.descendants(u).value()))
            if res:
                self.add_nodes_to(u, *res)
                queue += res

    def move_node(self, u: Node, at_new: Node):
        if u not in self.nodes(): return
        if at_new not in self.nodes(): raise ValueError("Unrecognized node!")
        descendants, p = self.descendants(u), self.parent(u)
        self.__hierarchy[p].remove(u)
        if not self.hierarchy(p): self.__leaves.insert(p)
        self.__links.remove((p, u)), self.__nodes.remove(u), self.add_nodes_to(at_new, u)
        self.__hierarchy[u] = descendants

    def remove(self, u: Node):
        if u not in self.nodes(): raise ValueError("Node not in tree!")
        if u == self.root(): raise ValueError("Can't remove root!")
        self.__nodes.remove(u)
        v, l = self.parent(u), 0
        while l < len(self.links()):
            if u in self.links()[l]:
                self.__links.remove(self.links()[l])
                l -= 1
            l += 1
        self.__hierarchy[v] += self.hierarchy(u)
        if u in self.leaves():
            self.__leaves.remove(u)
            if not self.hierarchy(v): self.__leaves.insert(v)
        self.__hierarchy.pop(u)

    def parent(self, u: Node):
        if u in self.nodes():
            for l in self.links():
                if u == l[1]: return l[0]
        raise ValueError('Node not in tree!')

    def node_depth(self, u: Node):
        if u in self.nodes():
            d = 0
            while u != self.root():
                u = self.parent(u)
                d += 1
            return d
        raise ValueError('Node not in graph!')

    def height(self):
        def helper(x: Node): return 1 + max([0, *map(helper, self.descendants(x).value())])

        return helper(self.root())

    def path_to(self, u: Node):
        x, res = u, []
        while x != self.root():
            res = [x] + res
            x = self.parent(x)
        return res

    def vertex_cover(self):
        return list(filter(lambda x: x not in self.independent_set(), self.nodes().value()))

    def dominating_set(self):
        dp = SortedKeysDict(*[(n, [[n], []]) for n in self.nodes().value()], f=self.__f)

        def dfs(r):
            if r in self.leaves(): return
            only_leaves, min_no_root = True, None
            for d in self.descendants(r):
                if d in self.leaves():
                    dp[r][1].append(d)
                    min_no_root = d
                else:
                    only_leaves = False
            if only_leaves: return
            for d in self.descendants(r):
                if d not in self.leaves():
                    dfs(d)
                    dp[r][0] += dp[d][0] if len(dp[d][0]) < len(dp[d][1]) else dp[d][1]
                    if min_no_root is None or len(dp[d][0]) < len(dp[min_no_root][0]): min_no_root = d
            for d in self.descendants(r): dp[r][1] += dp[d][1] if len(dp[d][1]) < len(
                dp[d][0]) and d != min_no_root else dp[d][0]

        dfs(self.root())
        return dp[self.root()][0] if len(dp[self.root()][0]) <= len(dp[self.root()][1]) else dp[self.root()][1]

    def independent_set(self):
        dp = SortedKeysDict(*[(n, [[n], []]) for n in self.nodes().value()], f=self.__f)

        def dfs(x: Node):
            for y in self.descendants(x).value():
                dfs(y)
                dp[x][0] += dp[y][1]
                dp[x][1] += dp[y][0] if len(dp[y][0]) >= len(dp[y][1]) else dp[y][1]

        dfs(self.root())
        return dp[self.root()][0] if len(dp[self.root()][0]) >= len(dp[self.root()][1]) else dp[self.root()][1]

    def isomorphic(self, other):
        if isinstance(other, Tree):
            if len(self.nodes()) != len(other.nodes()) or len(self.links()) != len(other.links()) or len(
                self.leaves()) != len(other.leaves()) or len(self.descendants(self.root())) != len(
                other.descendants(other.root())): return False
            this_hierarchies, other_hierarchies = dict(), dict()
            for n in self.nodes().value():
                descendants = len(self.descendants(n))
                if descendants not in this_hierarchies:
                    this_hierarchies[descendants] = 1
                else:
                    this_hierarchies[descendants] += 1
            for n in other.nodes().value():
                descendants = len(other.descendants(n))
                if descendants not in other_hierarchies:
                    other_hierarchies[descendants] = 1
                else:
                    other_hierarchies[descendants] += 1
            if this_hierarchies != other_hierarchies: return False
            this_nodes_descendants, other_nodes_descendants = {d: [] for d in this_hierarchies.keys()}, {d: [] for d in
                                                                                                         other_hierarchies.keys()}
            for n in self.nodes().value(): this_nodes_descendants[len(self.descendants(n))].append(n)
            for n in other.nodes().value(): other_nodes_descendants[len(self.descendants(n))].append(n)
            this_nodes_descendants, other_nodes_descendants = list(
                sorted(this_nodes_descendants.values(), key=lambda x: len(x))), list(
                sorted(other_nodes_descendants.values(), key=lambda x: len(x)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_descendants]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility): map_dict += [*zip(group, other_nodes_descendants[i])]
                possible = True
                for n, v0 in map_dict:
                    for m, v1 in map_dict:
                        if ((n, m) in self.links()) ^ ((v0, v1) in other.links()) or ((m, n) in self.links()) ^ (
                                (v1, v0) in other.links()):
                            possible = False
                            break
                    if not possible: break
                if possible: return True
            return False
        return False

    def __contains__(self, item):
        return item in self.nodes() or item in self.links()

    def __eq__(self, other):
        if isinstance(other, Tree):
            for u in self.nodes().value():
                if u not in other.nodes(): return False
            if len(self.nodes()) != len(other.nodes()): return False
            for u in self.nodes().value():
                if len(self.hierarchy(u)) != len(other.hierarchy(u)): return False
                for v in self.hierarchy(u).value():
                    if v not in other.hierarchy(u): return False
            return True
        return False

    def __str__(self):
        return '\n'.join(str(k) + ' -- ' + str(v) for k, v in filter(lambda p: p[1], self.hierarchy().items()))

    def __repr__(self):
        return str(self)


class WeightedNodesTree(Tree):
    def __init__(self, root_and_weight: (Node, float), *pairs: (Node, float), f=lambda x: x):
        super().__init__(root_and_weight[0], *[p[0] for p in pairs], f=f)
        self.__weights = SortedKeysDict(root_and_weight, f=f)
        for d, w in pairs:
            if d not in self.__weights: self.__weights[d] = w

    def weights(self, u: Node = None):
        return self.__weights if u is None else self.__weights[u]

    def copy(self):
        res = WeightedNodesTree((self.root(), self.__weights[self.root()]),
                                *[(d, self.__weights[d]) for d in self.descendants(self.root())])
        queue = self.descendants(res.root()).value()
        while queue:
            u = queue.pop(0)
            res_descendants = self.descendants(u).value()
            if res_descendants:
                res.add_nodes_to(u, *res_descendants)
                for d in res_descendants: res.__weights[d] = self.weights(d)
                queue += res_descendants
        return res

    def subtree(self, u: Node):
        queue, res = [u], WeightedNodesTree((u, self.weights(u)))
        while queue:
            v = queue.pop(0)
            for n in self.descendants(v).value(): res.add_nodes_to(v, (n, self.weights(n))), queue.append(n)
        return res

    def add_nodes_to(self, u: Node, new_p: (Node, float), *rest_p: (Node, float)):
        if u not in self.nodes(): raise Exception('Node not found!')
        for v, w in [new_p] + [*rest_p]:
            if v not in self.nodes(): self.__weights[v] = w
        super().add_nodes_to(u, new_p[0], *[p[0] for p in rest_p])

    def extend_tree_at(self, n: Node, tree):
        super().extend_tree_at(n, tree)
        if isinstance(tree, WeightedNodesTree):
            queue = [tree.root()]
            while queue:
                u = queue.pop(0)
                res = list(filter(lambda _n: _n not in self.nodes(), tree.descendants(u).value()))
                if res:
                    self.__weights[u] = tree.weights(u)
                    queue += res

    def remove(self, u: Node):
        self.__weights.pop(u), super().remove(u)

    def vertex_cover(self):
        dp = SortedKeysDict(*[(n, [[n], []]) for n in self.nodes().value()], f=self._Tree__f)

        def dfs(u: Node):
            for v in self.descendants(u).value():
                dfs(v)
                dp[u][0] += dp[v][0] if sum(map(self.weights, dp[v][0])) <= sum(map(self.weights, dp[v][1])) else dp[v][
                    1]
                dp[u][1] += dp[v][0]

        dfs(self.root())
        return dp[self.root()][0] if sum(map(self.weights, dp[self.root()][0])) <= sum(
            map(self.weights, dp[self.root()][1])) else dp[self.root()][1]

    def dominating_set(self):
        dp = SortedKeysDict(*[(n, [[n], []]) for n in self.nodes().value()], f=self._Tree__f)

        def dfs(r):
            if r in self.leaves(): return
            only_leaves, min_no_root = True, None
            for d in self.descendants(r):
                if d in self.leaves():
                    dp[r][1].append(d)
                    min_no_root = d
                else:
                    only_leaves = False
            if only_leaves: return
            for d in self.descendants(r):
                if d not in self.leaves():
                    dfs(d)
                    dp[r][0] += dp[d][0] if sum(map(self.weights, dp[d][0])) < sum(map(self.weights, dp[d][1])) else \
                    dp[d][1]
                    if min_no_root is None or sum(map(self.weights, dp[d][0])) < sum(
                        map(self.weights, dp[min_no_root][0])): min_no_root = d
            for d in self.descendants(r): dp[r][1] += dp[d][1] if sum(map(self.weights, dp[d][1])) < sum(
                map(self.weights, dp[d][0])) and d != min_no_root else dp[d][0]

        dfs(self.root())
        return dp[self.root()][0] if sum(map(self.weights, dp[self.root()][0])) <= sum(
            map(self.weights, dp[self.root()][1])) else dp[self.root()][1]

    def isomorphic(self, other):
        if isinstance(other, Tree):
            if len(self.nodes()) != len(other.nodes()) or len(self.links()) != len(other.links()) or len(
                self.leaves()) != len(other.leaves()) or len(self.descendants(self.root())) != len(
                other.descendants(other.root())): return False
            this_hierarchies, other_hierarchies = dict(), dict()
            for n in self.nodes().value():
                descendants = len(self.descendants(n))
                if descendants not in this_hierarchies:
                    this_hierarchies[descendants] = 1
                else:
                    this_hierarchies[descendants] += 1
            for n in other.nodes().value():
                descendants = len(other.descendants(n))
                if descendants not in other_hierarchies:
                    other_hierarchies[descendants] = 1
                else:
                    other_hierarchies[descendants] += 1
            if this_hierarchies != other_hierarchies: return False
            this_nodes_descendants, other_nodes_descendants = {d: [] for d in this_hierarchies.keys()}, {d: [] for d in
                                                                                                         other_hierarchies.keys()}
            for n in self.nodes().value(): this_nodes_descendants[len(self.descendants(n))].append(n)
            for n in other.nodes().value(): other_nodes_descendants[len(self.descendants(n))].append(n)
            this_nodes_descendants, other_nodes_descendants = list(
                sorted(this_nodes_descendants.values(), key=lambda x: len(x))), list(
                sorted(other_nodes_descendants.values(), key=lambda x: len(x)))
            from itertools import permutations, product
            _permutations = [list(permutations(this_nodes)) for this_nodes in this_nodes_descendants]
            possibilities = product(*_permutations)
            for possibility in possibilities:
                map_dict = []
                for i, group in enumerate(possibility): map_dict += [*zip(group, other_nodes_descendants[i])]
                possible = True
                for n, u in map_dict:
                    for m, v in map_dict:
                        if ((n, m) in self.links()) ^ ((u, v) in other.links()) or ((m, n) in self.links()) ^ (
                                (v, u) in other.links()) or isinstance(other, WeightedNodesTree) and self.weights(
                                n) != other.weights(u):
                            possible = False
                            break
                    if not possible: break
                if possible: return True
            return False
        return False

    def __eq__(self, other):
        if isinstance(other, WeightedNodesTree):
            if self.weights() != other.weights(): return False
        return super().__eq__(other)

    def __str__(self):
        return '\n'.join(f'{k}, {self.weights(k)} -- {v}' for k, v in self.hierarchy().items().value())
