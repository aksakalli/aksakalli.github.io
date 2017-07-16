---
layout: post
title:  "k-Means Clustering Algorithms"
date:   2016-02-04
description: "Comparison of different clutering algorithms: Lyod's, Hartgian's, and McQueen's"
tags:
    - pattern recognition
---

_k_-means clustering is a method to partition $$n$$ observation into $$k$$ clusters where  $$k \ll n$$.
Each observation $$x$$ belongs to a cluster $$C_i$$ with nearest mean $$\mu_i$$ compared to other clusters $$\mu_l$$:

$$
  C_i = \{ x \in X | \| x-\mu_i \|^2 	\leq \| x-\mu_l \|^2  \}
$$

The objection function is based on optimizing the sum of squared distances of each observation to its cluster mean.   

$$
\operatorname*{argmin}_{\mu_i,...,\mu_k} E(k) = \sum_{i=1}^{k} \sum_{x_j \in C_i}  \|x_j-\mu_i \|^2
$$

Since $$ E(k) $$ has numerous local minima, there is no algorithm known today to guarantee an optimal solution.

## Lloyd’s algorithm

It is most widely known algorithm to solve _k_-means clustering
and sometimes it is mistaken for the method itself. However it is:

* Sensitive to the initialization of the means
* Promise nothing about quality, hard to decide about number of iterations

## Hartigan's Algorithm

* Converges quickly
* Sensitive to initial random class assignment of points.
  * First animation
  ![Hartigan's algorithm for k-means clustering](http://imgur.com/RhRQ53u.gif?1)
  * Second animation with different initialization
  ![Hartigan's Algorithm 2](http://i.imgur.com/X8W5FDW.gif?1)

## MacQueen's Algorithm

* Convenient for streams
* Sensitive to the order of stream and the initialization of the means
  * First animation
  ![MacQueen's algorithm for k-means clustering](http://i.imgur.com/ZT9ftCk.gif?1)
  * Second animation with shuffled data
  ![MacQueen's Algorithm 2](http://i.imgur.com/czGbXZU.gif?1)


[[code](https://github.com/motjuste/patt-rex/blob/master/pattrex/fun_with_k_means.py)]
[[presentation](http://motjuste.github.io/patt-rex/project-03-demo.slides.html)]

**References**

C. Bauckhage. *"NumPy/SciPy Recipes for Data Science: Computing Nearest Neighbors."*
