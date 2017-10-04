---
layout: post
title:  "Database Normalization and Normal Forms with an Example"
date:   2012-03-12
description: Database normalization is essential procedure to avoid inconsistency in a relational database management system. This article aims to explain database normalization in a nutshell by giving a simple and effective example.
tags:
  - databases
---

This article aims to explain database normalization in a nutshell by giving a simple and effective example.

Concept of normalization and normal forms were introduced, after the invention of relational model.
Database normalization is essential procedure to avoid inconsistency in a relational database management system.
It should be performed in design phase. To achieve this, redundant fields should be refactored into smaller pieces.

## Normal forms

Normals forms are defined structures for relations with set of constraints that relations must satisfy in order
to detect data redundancy and correct anomalies.
There can be following anomalies while performing a database operation:

* **insert:** data is known but can not be inserted
* **update:** updating data requires modifications in multiple tuples (rows)
* **delete:** deleting some data causes some other data to be lost

First Normal Form has initial constraints, further normal forms like 2NF, 3NF, BCNF, 4NF, 5NF would add new constraints cumulatively.
In other words, every 2NF is also in 1NF; every relation in 3NF is also in 2NF.
If all group of relations are represented as sets, following figure can be drawn:

<img src="{{ site.url }}/images/db-norm/levels-of-normalization.svg" alt="Levels of normalization" style="width: 400px;"/>

<!-- ![Levels of normalization]({{ site.url }}/images/db-norm/levels-of-normalization.png) -->

As it can be seen, the relations satisfy 5NF also would satisfy all other normal forms.

## 1NF - First Normal Form

This is the most basic form of relation. Constraints:

* Attribute values have to be atomic
* Each record should be unique and have a primary key as identifier

As an example, we have movies and actors to be store in a relational database.
We have following dependency model:

![Dependency diagram for 1NF](/images/db-norm/1nf-dependency.png)

Here is the table for 1NF:

| <u>MOVIEID</u> | TITLE |COU|LANG|<u>ACTORID</u>|NAME|ORD|
|-:|:-|:-:|:-:|-:|:-|-:|
|6|Usual Suspects|UK|EN|308|Gabriel Byrne|2|
|228|Ed Wood|US|EN|26|Johnny Depp|1|
|70|Being John Malkovich|US|EN|282|Cameron Diaz|2|
|1512|Suspiria|IT|IT|745|Udo Kier|9|
|70|Being John Malkovich|US|EN|503|John Malkovich|14|

Anomaly examples for this model:

* **inserting** a new movie record without an actor information is not possible
* **updating** the language of the movie Being John Malkovich requires two rows to be updated
* **deleting** that Gabriel Byrne acts in the movie "Usual Suspects" also deletes that the movie was made in the UK

## 2NF - Second Normal Form

To correct these anomalies, the new constraint is introduced:

* Every non-key attribute functionally should depend on the primary key

Regarding this new constraint, the table should be divided into three tables that every attribute has only functional primary key.
Now dependency model became like this:

![Dependency diagram for 2NF](/images/db-norm/2nf-dependency.png)

Here are the three tables for 2NF:

|<u>MOVIEID</u>|TITLE|COU|LANG|
|-:|:-|:-:|:-:|
|6|Usual Suspects|UK|EN|
|228|Ed Wood|US|EN|
|70|Being John Malkovich|US|EN|
|1512|Suspiria|IT|IT|

|<u>ACTORID</u>|NAME|
|-:|:-|
|308|Gabriel Byrne|
|26|Johnny Depp|
|282|Cameron Diaz|
|745|Udo Kier|
|503|John Malkovich|

|<u>MOVIEID</u>| ACTORID| ORD|
|-:|-:|-:|
|6|308|2|
|228|26|1|
|70|282|2|
|1512|745|9|
|70|503|14|

2NF can correct anomalies listed for 1NF but there are some remaining anomalies:

* **inserting** the information that movies made in Germany are in German, is not possible if there exists no German movie record.
* **updating** the language of movies made in the US requires three rows to be updated
* **deleting** the record for the movie "Suspiria" also deletes that movies made in Italy are in Italian.

## 3NF - Third Normal Form

For this form following constraint is added:

* All non key attributes should only depends on a primary key

With this new constraint, country and language should be part of an individual table and country field should be the primary key of this new table.
Here is the new dependency model:

![Dependency diagram for 3NF](/images/db-norm/3nf-dependency.png)

Here are all tables for 3NF. (There is no change for Actor and Actor-Movie Matching table.)


|<u>COU</u>|LANG|
|:-:|:-:|
|UK|EN|
|US|EN|
|IT|IT|

|<u>MOVIEID</u>|TITLE|COU|
|-:|-:|-:|
|6| Usual Suspects|UK|
|228|Ed Wood|US|
|70|Being John Malkovich|US|
|1512|Suspiria|IT|

3NF can correct anomalies listed for 2NF. Although 3NF is sufficient to avoid delete, update and insert conflicts in most cases, there are some further normal forms like BCNF, 4NF and 5NF.


**References**

* Date, C. J., *An Introduction to Database Systems*. Addison-Wesley, 2004.
* Uyar, H. T. and Oguducu, S., *Database Management Systems* [[lecture slides](http://www.slideshare.net/uyar/tag/blg361e)].
