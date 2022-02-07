What's your ability? A survery of industrial robot skills
=======

This is the supporting material for the paper "What's your ability? A Survey about Industrial Robot Skills". Within this repo the code used to extract information automatically from a review table about skill-taxonomies togheter with supplementary material (i.e., figures) are provided. 

## News 
[2022/02/07] First version of the review with review table has been loaded.

# Paper clustering upon topic

![alt text](https://github.com/teiband/industrial-skill-review/blob/main/data/out/all/kmeans10all.png?raw=true)

The above graph shows the general clustering of all the identified actions (task, skill, primitive) found during the review. For a better analysis of the results this repo provided links and clustering across the different classes.

### Clustering of primitives

![alt text](https://github.com/teiband/industrial-skill-review/blob/main/data/out/primitive/kmeans10primitive.png?raw=true)

For more information on the clusters within primitives visit the [README](data/out/primitive/README.md)

### Clustering of skills

![alt text](https://github.com/teiband/industrial-skill-review/blob/main/data/out/skill/kmeans10skill.png?raw=true)

For more information on the clusters within skills visit the [README](data/out/skill/README.md)

### Clustering of tasks

![alt text](https://github.com/teiband/industrial-skill-review/blob/main/data/out/task/kmeans10task.png?raw=true)

For more information on the clusters within tasks visit the [README](data/out/task/README.md)

## Useful material

#### **Bibtex of all reviewed papers**

In *** you can find the list which contains the bibtex entry of the relevant papers.

#### **Review table**

The review table containing the raw data is stored under [`data/in`](data/in/).

#### **Code for extraction**

For info about the code visit [README](src/README.md).

#### **Support material**

In order to visualize the different wordclouds and supporting images you can visit [`data/out`](data/out/). Within the folder the data is organiyed upon all, task, skill and primitive.

#### **Contributors**

* **Matteo Pantano** - [matteopantano](https://github.com/matteopantano)
* **Thomas Eiband** - [teiband](https://github.com/matteopantano)