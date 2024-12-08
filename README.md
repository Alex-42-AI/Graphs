# Graphs
A graph is a data structure, consisting of nodes and links between some of them. There are different types of graphs, such as directed/undirected, weighted/unweighted and multigraphs.

This project is an implementation of an unweighted undirected graph, a weighted undirected graph, an unweighted directed graph and a weighted directed graph, as well as of a tree, a weighted tree and a binary tree. Weighted graphs can have weights on the nodes, on the links or on both. Weighted trees can only have weights on the nodes.

In file General.py, there's an implementation of a node and an implementation of an abstract base class Graph. It implements the following methods, that are common for both direted and undirected graphs:
1) nodes, links and degrees getters;
2) remove nodes;
3) returning a copy of the graph;
4) returning the complementary graph of the given one;
5) returning the graph component of a given node;
6) listing out the connection components in the graph;
7) checking whether the graph is connected;
8) checking whether one node can reach another one in the graph;
9) checking whether the graph is full (whether there are links between every two nodes in it);
10) calculating the shortest path from one node to another in the graph;
11) checking whether a path/loop with a given length exists between from one node to another;
12) checking whether an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk exist;
13) actually finding an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk;
14) checking whether the graph is isomorphic to another graph and if so, returning the bijection between the sets of nodes of the graphs;
15) returning the reverse (complementary) graph of the original one;
16) defining __bool__ as whether the graph has any nodes;
17) checking whether a node is present in the graph;
18) checking whether two graphs are equal;
19) combining two graphs into one (addition);
20) representing the graph (__str__ and __repr__).

All graphs also have methods for adding a node to already present nodes, connecting a node to already present nodes and disconnecting a node from already present nodes, but they're implemented differently in undirected graps and directed graphs.

In file UndirectedPath.py are implemented class Link for an undirected link and the undirected graph classes.

Undirected graph classes further have methods for:
1) listing out the leaves in the graph (nodes with a degree of 1);
2) checking whether a given node is a leaf;
3) listing out the neighboring nodes (for one or all nodes);
4) returning the total sum of all degrees in the graph;
5) finding the excentricity of a given node (the longest of the shortest possible from that node to any other);
6) finding the diameter of the graph (the greatest possible excentricity in it);
7) checking whether the graph could be a tree;
8) returning a tree with a given node as a root (if the graph isn't connected, it only takes the connection component, to which the given node belongs and if its connection component couldn't be a tree, it sacrifices some links by using BFS to get the hierarchy);
9) listing out cut nodes in the graph;
10) listing out bridge links in the graph;
11) returning the links graph of the original one (a graph, which has the original graph's links as nodes and there're links between them exactly when the links they represent share a node);
12) returning a possible interval sorting of the nodes of the graph if the graph is an interval graph (if there exists a set of intervals over the real numberline such, that its nodes could represent the intervals in the sense, that there are only links between two nodes exactly when the intervals they represent intersent), otherwise returns the empty list. The sort is based on how early a given node's interval starts;
13) checking whether the graph is full k-partite (whether it has k independent sets, where all nodes in one independent set are connected to all other nodes outside that independent set). k could be given, but it doesn't have to be;
14) checking whether a given set of nodes is a clique in the graph;
15) listing out the cliques of a given size k in the graph;
16) listing all maximum by cardinality cliques in the graph, to which a given node belongs;
17) listing out all maximum by cardinality cliques in the graph;
18) listing out all maximal by inclusion (not cardinality) cliques in the graph, to which a given node belongs;
19) returning the clique graph of the original one (where a node represents a maximal by inclusion clique in the original one and links represent clique intersections);
20) partitioning the nodes/links of the graph into a set of independent sets (anti-cliques) such, that the partition has as few elements as possible;
21) returning a minimum by cardinality vertex cover of the graph;
22) returning a minimum by cardinality dominating set of the graph;
23) returning a minimum by cardinality independent set of the graph;

Unique methods for directed graph classes are:
1) listing out the previous nodes of a given one (if such is gives, otherwise it shows this for all nodes);
2) listing out the next nodes of a given one (if such is gives, otherwise it shows this for all nodes);
3) listing out the sources (nodes, that aren't pointed by any node) and the sinks (nodes, that don't point to any node) of the graph;
4) checking whether a given node is a source and whether it's a sink;
5) returning the transpposed graph of the original (where each link points in the exact opposite direction);
6) checking whether the graph has a loop and whether it's a DAG (directed acyclic graph);
7) returning a topological sort of the graph if it's a DAG, otherwise - an empty list;
8) returning the strongly connected component of a given node in the graph (a maximum by cardinality set of nodes, where there exists a path from any node in it to any other node in it);
9) listing out all strongly-connected components in the graph;
10) returning the dag of strongly-connected components of the original one (where each node represents a maximum by inclusion strongly connected component and a link exists from one node to another exactly when there's at least one link from a node in the first SCC to a node in the second SCC (This graph is always a DAG).

Furthermore, the degrees method returns a pair of numbers, the first of which shows how many nodes point to a given one and the second one shows how many nodes it points to, if a node is given, otherwise it returns a dictionary of the same information for all nodes.

Weighted graphs by nodes, in addition to their parental superclass, have methods for:
1) returning the weight of a node, if such is given, otherwise returns the same for all nodes;
2) returning the sum of the weights of all nodes;
3) setting/increasing the weight of a given node to/with a given real value;
4) finding the minimal (lightest) path between two nodes;
5) returning a minimum by total sum of the weights of the nodes vertex cover of the graph;
6) returning a minimum by total sum of the weights of the nodes dominating set of the graph;
7) returning a maximum by total sum of the weights of the nodes independent set of the graph.
The last tree methods are only present in the undirected graphs.

Weighted graphs by links, in addition to their parental superclass, have methods for:
1) returning the weight of a link, if such is given, otherwise returns the same for all links;
2) returning the sum of the weights of all links;
3) setting/increasing the weight of a given link to/with a given real value;
4) finding the minimal spanning tree of the graph (for undirected graphs);
5) finding the minimal (lightest) path between two nodes.

Weighted graphs by nodes and links, in addition to their parental superclasses, have a method for finding the minimal (lightest in terms of sum of node and link weights) path between two nodes and for getting the total sum of all nodes and links.

On top of that, the methods for adding and connecting nodes differ such, that instead of accepting a positive number of nodes, which a given node is going to be connected to, they accept a positive number of pairs, each of which contains a node and a real number, that is going to be the value of the link between the two nodes.

The binary tree in this project has:
1) methods root, left and right, that return respectively the root, the left subtree and the right subtree;
2) copy() methed;
3) rotate_left and rotate_right methods;
4) a method to get the subtree with a given node as a root in the tree;
5) a method to return the height of the tree (in terms of links);
6) a method to return all nodes on a certain level in the tree and a method, that returns the width of the tree;
7) a method to return the leaves of the tree;
8) a method for counting the nodes of the tree;
9) a method for finding the Morse code of a node with a given value in the tree (left is dot and right is dash);
10) a method for encrypting a message into morse code;
11) a method to get an inverted copy of the tree;
12) traverse method, where the traversal type can be specified;
13) __contains__ and __eq__ methods;
14) __invert__ for inverting the tree;
15) __bool__, asking whether the tree has a root;
16) __str__ method, which basically draws the tree;
17) __repr__ method, that returns the same as method traverse with default traversal type in-order.

The tree class in the project has methods for:
1) getting the root, the nodes, the links, the leaves and the hierarchy in the tree;
2) getting the descendants of a given node in the tree;
3) making a copy of the tree;
4) adding new nodes to one already in the tree;
5) extending the tree with another one on a given node;
6) removing a node with or without its subtree;
7) returning the parent node of a given one;
8) returning the depth of a given node;
9) returning the height of the tree;
10) getting the path from the root to a given node;
11) returning a minimum by cardinality vertex cover of the tree;
12) returning a minimum by cardinality dominating set of the tree;
13) returning a minimum by cardinality independent set of the tree;
14) checking whether the tree is isomorphic with another tree and if so, returning an isomorphic function between the nodes of the trees;
15) checking whether the tree has nodes;
16) checking whether a node is in the tree;
17) comparing the tree with another one;
18) drawing the tree (__str__);
19) representing the tree (__repr__).

The weighted tree class in particular has methods for:
1) returning the weight of a node, if such is given, otherwise returns the same for all nodes;
2) setting the weight of a node to a given real numerical value;
3) returning a minimum by total sum of the weights of the nodes vertex cover of the tree;
4) returning a minimum by total sum of the weights of the nodes dominating set of the tree;
5) returning a maximum by total sum of the weights of the nodes independent set of the tree.
