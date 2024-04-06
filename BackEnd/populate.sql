# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 17:48:01 2024

@author: Disha Srinivas
"""
import psycopg2

connection = psycopg2.connect(dbname='bureaudb', user='postgres', password='fraudapidb', host='database-4.cpym2wmsqw3m.eu-north-1.rds.amazonaws.com', port='5432', sslmode='require')
cursor = connection.cursor()


# Path to your CSV file
csv_file_path = 'C:\\Users\\Disha Srinivas\\Downloads\\dataset_2.csv'

# SQL command to copy data from CSV into table
copy_sql = """
           COPY transaction_data.transactions FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """

with open(csv_file_path, 'r') as file:
    try:
        cursor.copy_expert(sql=copy_sql, file=file)
        connection.commit()
        print("Data imported successfully!")
    except psycopg2.Error as e:
        connection.rollback()
        print("Error:", e)

# Close the cursor and connection
cursor.close()
connection.close()
