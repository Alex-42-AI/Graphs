# Graphs
A graph is a data structure, consisting of nodes and links between some of them. There are different types of graphs, such as directed/undirected, weighted/unweighted and multigraphs.

This project is an implementation of an unweighted undirected graph, a weighted undirected graph, an unweighted directed graph and a weighted directed graph, as well as of a tree, a weighted tree and a binary tree. Weighted graphs can have weights on the nodes, on the links or on both. Weighted trees can only have weights on the nodes.

Regardless of their differences, all graph classes have main getters like nodes and links and setters like add and remove for nodes and connect and disconnect for links.
They also have the following methods in common:
1) listing out the connection components in the graph;
2) checking whether the graph is connected;
3) checking whether two nodes are reachable in the graph;
4) checking whether a path/loop with a given length exists between two nodes;
5) listing out cut nodes in the graph;
6) calculating the shortest path from one node to another in the graph;
7) returning the sorting function of the graph nodes;
8) checking whether an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk exist;
9) actually finding an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk;
10) checking whether the graph is isomorphic to another graph and if so, returning the bijection between the nodes of the graphs;
11) checking whether a node or a link is present in the graph;
12) checking whether two graphs are the same;
13) combining two graphs into one (addition).

Undirected graph classes further have methods for:
1) listing out the neighboring nodes and the degrees (both for one or all nodes);
2) finding the width of the graph (the longest of the shortest possible distances between any two nodes);
3) checking whether the graph could be a tree;
4) returning a possible interval sorting of the nodes of the graph if the graph is an interval graph (if there exists a set of intervals over the real numberline such, that its nodes could represent the intervals in the sense, that there are only links between two nodes when the intervals they represent intersent), otherwise returns the empty list;
5) listing out the cliques of size k in the graph;
6) listing out bridge links in the graph;
7) classifying the nodes/links of the graph into a set of independent sets (anti-cliques);
8) listing out all optimal by cardinality vertex covers of the graph;
9) listing out all optimal by cardinality dominating sets of the grpah;
10) listing out all maximal by cardinality independent sets of the graph;
11) checking whether the graph is full (whether there are links between every two nodes in it).

The unique methods for directed graph classes have unique methods for:
1) listing out the nodes, that point to a given node if such is gives, otherwise it shows this for all nodes;
2) listing out the nodes, that a given node points to if such is gives, otherwise it shows this for all nodes;
3) listing out the sources (nodes, that aren't pointed by any node) and the sinks (nodes, that don't point to any node) of the graph;
4) checking whether the graph is a DAG (directed acyclic graph);
5) returning a topological sort of the graph if it's a DAG;
6) listing out the strongly-connected components in the graph.
Furthermore, instead of having one method for connecting nodes, the directed graph uses two methods - connect_from_to and connect_to_from, that work as their names suggest. Also, the degrees method returns a pair of numbers, the first of which shows how many nodes point to a given one and the second one shows how many nodes it points to, if a node is given, otherwise it returns a dictionary of the same information for all nodes.

Weighted graphs by nodes, in addition to their parental superclass, have methods for:
1) returning the weight of a node, if such is given, otherwise returns the same for all nodes;
2) returning the sum of the weights of all nodes;
3) setting the weight of a given node to a given real value;
4) finding the minimal (lightest) path between two nodes;
5) listing out all optimal by total sum of the weights of the nodes vertex covers of the graph;
6) listing out all optimal by total sum of the weights of the nodes dominating sets of the graph;

Weighted graphs by links, in addition to their parental superclass, have methods for:
1) returning the weight of a link, if such is given, otherwise returns the same for all links;
2) returning the sum of the weights of all links;
3) setting the weight of a given link to a given real value;
4) finding the minimal spanning tree of the graph (for undirected graphs);
5) finding the minimal (lightest) path between two nodes.

Weighted graphs by nodes and links, in addition to their parental superclasses, have a method for finding the minimal (lightest in terms of sum of node and link weights) path between two nodes and for getting the total sum of all nodes and links.

On top of that, the methods for adding and connecting nodes differ such, that instead of accepting a positive number of nodes, which a given node is going to be connected to, they accept a positive number of pairs, each of which contains a node and a real number, that is going to be the value of the link between the two nodes.
Also, their methods for finding an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk also return the sum of the weights of the links in the paths found and the Hamilton methods look for the lightest routes possible (using a greedy algorithm).

The binary tree in this project has:
1) methods left() and right(), that return respectively the left subtree and the right subtree;
2) a method to return the height of the tree (in terms of links);
3) a method to return all nodes on a certain level in the tree and a method, that returns the width of the tree;
4) a method for counting the leaves of the tree;
5) a method for counting the nodes of the tree;
6) a method for finding the Morse code of a node with a given value in the tree (left is dot and right is dash);
7) a method for encrypting a message into morse code;
8) __contains__ and __eq__ methods;
9) a method for inverting the tree and one for returning a copy of the tree being inverted without inverting it;
10) methods for printing all the node values in the tree preorder, in order and post order.

The tree class in the project has methods for:
1) getting the root, the nodes, the links, the leaves and the hierarchy in the tree;
2) getting the descendants of a given node in the tree;
3) making a copy of the tree;
4) adding new nodes to one already in the tree;
5) extending the tree with another one on a given node;
6) removing a node with all of its descendants;
7) returning the parent node of a given one;
8) returning the depth of a given node;
9) returning the height of the tree;
10) getting the path from the root to a given node;
11) returning an optimal (with a minimal cardinality) vertex cover of the nodes of the tree;
12) returning an optimal (with a minimal cardinality) dominating set of the nodes of the tree;
13) returning an optimal (with a maximal cardinality) independent set of the nodes of the tree;
14) checking whether the tree is isomorphic with another tree and if so, returning the isomorphic function between the nodes of the trees;
15) checking whether a node or a link is contained in the tree;
16) comparing the tree with another one.

The weighted tree class in particular has methods for:
1) returning the weight of a node, if such is given, otherwise returns the same for all nodes;
2) setting the weight of a node to a given real numerical value;
3) returning an optimal (with a minimal sum of the node weights) vertex cover of the nodes of the tree;
4) returning an optimal (with a minimal sum of the node weights) dominating set of the nodes of the tree;
