# Graphs
A graph is a data structure, consisting of nodes and links between some of them. There are different types of graphs, such as directed/undirected, weighted/unweighted and multigraphs.

This project is an implementation of an unweighted undirected graph, a weighted undirected graph, an unwaighted directed graph and a weighted directed graph, as well as of a tree.

Regardless of their differences, all graph classes have methods for:
1) returning a list of the nodes;
2) returning a list of the links;
3) returning a list of nodes, connected to a given node;
4) returning the dictionary of neighboring nodes for every node;
5) returning the degree of a given node;
6) returning the degrees of all nodes in the graph;
7) adding a new node to the graph;
8) removing a positive number of nodes from the graph;
9) connecting a node to a positive number of other nodes in the graph;
10) disconnecting a node from a positive number of other nodes in the graph;
11) returning the complementary graph of the original;
12) returning a copy of the graph;
13) listing out the connection components in the graph;
14) checking whether the graph is connected;
15) checking whether two nodes are reachable in the graph;
16) evaluating whether a path with a given length exists between two nodes;
17) evaluating whether a loop with a given length exists in the graph at all;
18) listing out bridge nodes in the graph;
19) listing out bridge links in the graph;
20) calculating the shortest path between two nodes in the graph;
21) calculating only the length of the shortest path between two nodes in the graph;
22) checking whether an Euler tour exists, whether an Euler walk exists, whether a Hamilton tour exists and whether a Hamilton walk exists;
23) actually finding an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk;
24) checking whether a node or a link is present in the graph;
25) checking whether two graphs are the same;
26) combining two graphs into one (addition);
27) representing the graph.

Undirected graph classes further have methods for:
1) checking whether the graph could be a tree;
2) listing out the cliques with a given number of nodes in the graph;
3) finding the chromatic number of the nodes of the graph;
4) finding the chromatic number of the links of the graph;
5) evaluating the smallest number of holes on the surface, which the graph can be drawn on without any of its links intersecting;
6) evaluating whether the graph is planar;
7) counting how many faces the graph separates the surface with least holes, on which it can be drawn without any of its links intersecting, into;
8) checking whether the graph is full (whether there are links between every two nodes in it). 

The only method, unique for the directed graphs, is the one, that evaluates whether the graph is strongly connected (whether a path exists between every two nodes in it).

However, there are differences in some of the common methods, unique to the directed graphs only, and they are, that:
1) the method for adding a new node accepts a mutable, containing nodes, that point to the new node and an iter, containing nodes, that the new node points to;
2) instead of one method for connecting nodes, there are two methods - connect_from_to and connect_to_from, that work as their names suggest;
3) the degrees method returns a pair of numbers, the first of which shows how many nodes point to it and the second one shows how many nodes it points to, if a node is given, otherwise it returns the same for all nodes;
4) the neighboring method only returns the nodes, pointed by a node, if such is given, otherwise it returns the same for all nodes;
5) the method, that checks whether two nodes are reachable, uses BFS to check whether there is a path between the two given nodes.

Weighted graphs, in addition to their parental superclasses, have methods for:
1) returning the weight of a link, if such is given, otherwise returns the same for all links;
2) returning the sum of the weights of all links;
3) finding the minimal spanning tree of the graph;
4) finding the lightest (or minimal) path between two nodes.

On top of that, the methods for adding and connecting nodes differ such, that instead of accepting a positive number of nodes, which a given node is going to be connected to,
they accept a positive number of pairs, each of which contains a node and a real number, that is going to be the value of the link between the two nodes.
Also, their methods for finding an Euler tour, an Euler walk, a Hamilton tour and a Hamilton walk also return the sum of the weights of the links in the paths found and the Hamilton methods look for the lightest routes possible.
And finally, weighted graphs are represented with their nodes and their dictionary of the weights, rather than the nodes and the links alone.
