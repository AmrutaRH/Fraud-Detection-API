# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import psycopg2
# define your db connection string
connection = psycopg2.connect(dbname='bureaudb', user='postgres', password='fraudapidb', host='database-4.cpym2wmsqw3m.eu-north-1.rds.amazonaws.com', port='5432', sslmode='require')
cursor = connection.cursor()

# SQL command to create a schema
create_schema_query = """
CREATE SCHEMA transaction_data;
"""

try:
    # Execute the SQL command
    cursor.execute(create_schema_query)
    
    # Commit the transaction
    connection.commit()
    print("Schema created successfully!")
    
except psycopg2.Error as e:
    # Rollback the transaction in case of an error
    connection.rollback()
    print("Error creating schema:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()