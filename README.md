# Genetic Algorithm for MWISP
This is the implementation of genetic algorithm for maximum weighted independent set problem. Each graph should be given as a text file. An example graph can be found in *test.txt* file. Format of each graph file:
* First line consists of an integer **n** which represents the number of nodes.
* Second line contains an integer **m** which represents the number of edges in graph.
* Next **n** lines' format is **'node weight'**, and  *node* indicates the node itself and *weight* indicates its weight.
* Next **m** lines' format is **'node1 node2'** which represents an edge from *node1* to *node2*.

For each run some input parameters are required for the calculation:
* Name of the Graph File
* Generation Limit
* Population Size
* Crossover Probability
* Mutation Probability

## How to Use It?
* Clone the repo.
* Run 'python3 genetic.py'.
* Be sure that graph file is at the same location as 'genetic.py'.