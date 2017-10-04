---
layout: post
title:  "Mapping Inheritance to Relational Databases"
date:   2015-06-16
description: "Alternative approaches to map inheritance to relational model"
tags:
    - programming
    - Databases
---

Inheritance is the key concept of object-oriented programming.
A subclass is basically inherits the properties of its parent class.
Let's say, for our application we define basic class `User`.
We need also `Customer` and `Maintainer` classes as a custom type of `User`,
so we inherit them from the super class.


![Domain Object Model for inheritance mapping](/images/inheritance-map.png)


<!--
abstract User {
  string username
  string password
}

class Customer{
  int customerNumber
}

class Maintainer{
  int employeeNumber
}
User <|-down- Customer
User <|-down- Maintainer -->

`Customer` and `Maintainer` subclasses, which are inherited from `User`,
have `username` and `password` fields as common but also some additional specific fields.
When we want to store those objects into a relational database system,
they need to be mapped as tables.
However, relational databases don't support inheritance.
In this example we have one base class and two subclasses to map into the relational database as tables.
There are three approaches with their trade-offs to do that.

## 1) Single table

User table:

|id|username|password|customerNumber|employeeNumber|type|
|--|
|1 |Alice|123|10001|NULL|Customer|
|2 |Bob|abc|NULL|10001|Maintaner|

In this approach, all fields, which are defined under a super (parent) class, are stored in a single table.
It is easy to query and retrieve different types from one table without need of join statements.
However, a query to get `Customer` class object would also return irrelevant `employeeNumber` field;
hence all regarding fields should be specified in the select statement.

Another problem is that, it is not possible to use constrains such as not null for a subclass.
For example, `customerNumber` is an essential field for all `Customer` records.
Yet applying not null constrain for `customerNumber` would prevent us from storing other objects without `customerNumber` such as `Maintainer`.

## 2) Class Table Inheritance

User table

|id|username|password|type|
|--|
|1 |Alice   |123     |Customer|
|2 |Bob     |abc     |Maintaner|

Customer table

|id|customerNumber|
|--|
|1|10001|

Maintainer table

|id|employeeNumber|
|--|
|2 |10001|

In this approach, there exist one database table per class.
Separate tables provide consistent data storage with constrain definitions but it is more complex to query a subclass.
It requires to write some join statements which reduces the performance.
For example, to get a `Customer` object, it needs to be join with `User` table.


## 3) Concrete Table Inheritance

Customer table

|id|username|password|customerNumber|
|--|
|1|Alice|123|10001|

Maintainer table

|id|username|password|employeeNumber|
|--|
|2|Bob|abc|10001|

In this approach, there exist a table for each concrete class.
Every concrete class has a table with duplicated fields.
In case of updating a field type of the base class would require to migrate multiple tables.
For example, if we change character size of `password` field, we need to alter both `Maintaner` and `Customer` tables.
It might lead a conflict.
