import sqlite3
import mysql.connector 
connection = sqlite3.connect("PhonePe.db")
curs = connection.cursor()

query1 = """CREATE TABLE Aggregate_Transaction(State Text Not null,
Year INT Not null,
Quatar Text Not null,
Transaction_Type Text Not null,
Transaction_count Int Not null,
Transaction_amount Int Not null)"""
curs.execute(query1)

query2 = """CREATE TABLE Aggregate_User(State Text Not null,
Year INT Not null,
Quatar Text Not null,
User_Brand Text Not null,
User_Count Int Not null,
User_Percentage Float Not null)"""
curs.execute(query2)

query3 = """CREATE TABLE Map_Transaction(State Text Not null,
Year INT Not null,
Quatar Text Not null,
District_Name Text Not null,
Transaction_count Int Not null,
Transaction_amount Int Not null)"""
curs.execute(query3)

query4 = """CREATE TABLE Map_User(State Text Not null,
Year INT Not null,
Quatar Text Not null,
District_Name Text Not null,
Registered_Users Int Not null)"""
curs.execute(query4)

query5 = """CREATE TABLE Top_Transaction(State Text Not null,
Year INT Not null,
Quatar Text Not null,
Pincode INT Not null,
Transaction_count Int Not null,
Transaction_amount Int Not null)"""
curs.execute(query5)

query6 = """CREATE TABLE Top_User(State Text Not null,
Year INT Not null,
Quatar Text Not null,
Pincode Int Not null,
Registered_Users Int Not null)"""
curs.execute(query6)