# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 16:49:22 2024

@author: Disha Srinivas
"""
import psycopg2
connection = psycopg2.connect(dbname='bureaudb', user='postgres', password='fraudapidb', host='database-4.cpym2wmsqw3m.eu-north-1.rds.amazonaws.com', port='5432', sslmode='require')
cursor = connection.cursor()


# SQL command to create a table in a schema
create_table_query = """
CREATE TABLE  transaction_data.transactions (
    mti VARCHAR(255),
    processingCode VARCHAR(255),
    transactionAmount VARCHAR(255),
    dateTimeTransaction VARCHAR(255),
    cardholderBillingConversionRate VARCHAR(255),
    stan VARCHAR(255),
    timeLocalTransaction VARCHAR(255),
    dateLocalTransaction VARCHAR(255),
    expiryDate VARCHAR(255),
    conversionDate VARCHAR(255),
    merchantCategoryCode VARCHAR(255),
    posEntryMode VARCHAR(255),
    acquiringInstitutionCode VARCHAR(255),
    forwardingInstitutionCode VARCHAR(255),
    rrn VARCHAR(255),
    cardAcceptorTerminalId VARCHAR(255),
    cardAcceptorId VARCHAR(255),
    cardAcceptorNameLocation VARCHAR(255),
    cardBalance VARCHAR(255),
    additionalData48 VARCHAR(255),
    transactionCurrencyCode VARCHAR(255),
    cardholderBillingCurrencyCode VARCHAR(255),
    posDataCode VARCHAR(255),
    originalDataElement VARCHAR(255),
    channel VARCHAR(255),
    encryptedPan VARCHAR(255),
    network VARCHAR(255),
    dcc VARCHAR(255),
    kitNo VARCHAR(255),
    factorOfAuthorization VARCHAR(255),
    authenticationScore VARCHAR(255),
    contactless VARCHAR(255),
    international VARCHAR(255),
    preValidated VARCHAR(255),
    enhancedLimitWhiteListing VARCHAR(255),
    transactionOrigin VARCHAR(255),
    transactionType VARCHAR(255),
    isExternalAuth VARCHAR(255),
    encryptedHexCardNo VARCHAR(255),
    isTokenized VARCHAR(255),
    entityId VARCHAR(255),
    moneySendTxn VARCHAR(255),
    mcRefundTxn VARCHAR(255),
    mpqrtxn VARCHAR(255),
    authorisationStatus VARCHAR(255),
    latitude VARCHAR(255),
    longitude VARCHAR(255)
);
"""

try:
    # Execute the SQL command
    cursor.execute(create_table_query)
    
    # Commit the transaction
    connection.commit()
    print("Table created successfully!")
    
except psycopg2.Error as e:
    # Rollback the transaction in case of an error
    connection.rollback()
    print("Error creating table:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
