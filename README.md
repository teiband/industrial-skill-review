# Capability-based Frameworks for Industrial Robot Skills: a Survey

This is the supporting material for the paper "Capability-based Frameworks for Industrial Robot Skills: a Survey". Within this repo the code used to extract information automatically from a review table about skill-taxonomies togheter with supplementary material (i.e., figures) are provided.  If you find this work useful please consider citing it.

## News 

[2022/03/01] Arxiv preprint uploaded and CASE 2022 submission

[2022/02/10] Bibtex of the reviewed papers available.

[2022/02/07] First version of the review with review table has been loaded.

## Paper clustering upon topic

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

In [`data/out/bibtex`](data/out/bibtex.bib) you can find the list which contains the bibtex entry of the reviewed papers.

#### **Review table**

The review table containing the raw data is stored under [`data/in`](data/in/).

#### **Code for extraction**

For info about the code to extract wordclouds and create clusters visit [README](src/README.md).

#### **Support material**

In order to visualize the different wordclouds and supporting images you can visit [`data/out`](data/out/). Within the folder the data is organized upon all, task, skill and primitive. Moreover, the definition of the requirements is as follows:

Requirement nr | Definition
--- | --- 
#1 | List hazards for the application
#2 | List safety elements included 
#3 | Identify and apply risk reduction for industrial robots. Moreover, intended use of the robotic system
#4 | Identify and apply risk reduction for and collaborative robots with precise velocities with testing. Moreover, intended use of the collaborative system
#5 | Identify and apply risk reduction for care robots with testing
#6 | Interaction with other systems
#7 | Intended hardware where to run the system
#8 | Version of relevant software and firmware
#9 | Forms in which the system should be used 
#10 | Instructions to use the system and where applicable installation
#11 | Dataset used with explanations
#12 | Human interaction (e.g., experience) tested on target users
#13 | Has customizable features

#### **Contributors**

* **Matteo Pantano** - [matteopantano](https://github.com/matteopantano)
* **Thomas Eiband** - [teiband](https://github.com/teiband)

#### **Citation**

    @misc{pantano2022capability,
      title={Capability-based Frameworks for Industrial Robot Skills: a Survey}, 
      author={Matteo Pantano and Thomas Eiband and Dongheui Lee},
      year={2022},
      archivePrefix={arXiv},
      primaryClass={cs.RO}
    }
