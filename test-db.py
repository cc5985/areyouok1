#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql_API

mysql_manager=mysql_API.MySQLManager("root","caichong","test")

# test for create a new table
# mysql_manager.create_table("test2","id int not null, age int")

# test for query
# result=mysql_manager.inquire("select * from table12")
# print(result.__class__)  # if successful: a tuple;  else bool
# print(result)

# test for insertion:
# result=mysql_manager.insert_data("insert into table1 (c1,c2) values (7,555) ")
# print(result.__class__)
# print(result)

# test for get the size of a sql schema
# result=mysql_API.MySQLManager.len_of_schema("test","MB")
# print(str(result) + " MB")

# test for get the size of a sql table :failed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# result=mysql_manager.len_of_table("table1")
# print(result)

# 1. create 365 tables
# each of the tables represents the data set of A day, therefore, there should be 365 tables
# naming rules are as following:
#   1. depth_ ; 2. date_; 3. market

# the coding standard of Depth table:
# name= "depth_OKEx_" + str(month).rjust(2,"0") + str(day).rjust(2,"0")
# table structure of Depth table:

# _DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# string=""
# string="id int not null AUTO_INCREMENT, timestamp int, currency_pair varchar(15), data json,  PRIMARY KEY (id)"
# print(string)
#
# for month in range(1,13):
#     days=_DAYS_IN_MONTH[month]
#     # print(str(month) + ": " + str(days))
#     for day in range(1,days+1):
#         table_name= "depth_OKEx_" + str(month).rjust(2,"0") + str(day).rjust(2,"0")
#         print(table_name)
#         mysql_manager.create_table(table_name,string)

