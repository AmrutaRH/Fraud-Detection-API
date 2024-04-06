from flask import Flask, request, jsonify
from datetime import datetime
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import recall_score
app = Flask(__name__)

@app.route('/check', methods=['POST'])
def process_json():
    if request.is_json:
        json_data = request.json
        card_balance=float(json_data.get('cardBalance'))
        transactions=float(json_data.get('transactionAmount'))
        if transactions >= 0.7 * card_balance and card_balance >= 300000:
            status = "ALERT"
        else:
            status = "OK"
        output_dict = {
            "status": status,
            "ruleViolated": ["RULE-001"],
            "timestamp":"3677"
        }
        return jsonify(output_dict)
    else:
        
        return jsonify({'error': 'Request must contain JSON data'}), 400
    
@app.route('/check2', methods=['POST'])
def process_json1():
    if request.is_json:
        json_data = request.json
        transactions = json_data.get('transactions')
        card_transactions = {}

        # Initialize variables to track unique locations and total transaction amount
        unique_locations = {}
        total_transaction_amount = {}

        # Parse transactions and calculate relevant metrics
        for transaction in transactions:
            # Extract transaction details
            card_no = transaction['encryptedHexCardNo']
            transaction_time = datetime.strptime(transaction['dateTimeTransaction'], '%d%m%y%H%M%S')
            latitude = float(transaction['latitude'])
            longitude = float(transaction['longitude'])
            transaction_amount = float(transaction['transactionAmount'])

            # Initialize card details if not present
            if card_no not in card_transactions:
                card_transactions[card_no] = []
                unique_locations[card_no] = set()
                total_transaction_amount[card_no] = 0

            # Add transaction amount to total amount for the card
            total_transaction_amount[card_no] += transaction_amount

            # Store transaction in history by card
            card_transactions[card_no].append((transaction_time, latitude, longitude))

            # Add location to unique locations set for the card
            location = (latitude, longitude)
            unique_locations[card_no].add(location)

        # Check rule violations for each card
        for card_no in card_transactions:
            # Check if there are more than 5 unique locations with a minimum difference of 200KM between them
            if len(unique_locations[card_no]) > 5:
                for loc1 in unique_locations[card_no]:
                    for loc2 in unique_locations[card_no]:
                        if loc1 != loc2 and geodesic(loc1, loc2).kilometers < 200:
                            return "ALERT"  # Rule violated: Less than 200KM between two locations
            else:
                return "OK"  # Less than 5 unique locations, rule not violated

            # Check if total transaction amount exceeds 1,00,000 Rs
            if total_transaction_amount[card_no] > 100000:
                return "ALERT"  # Rule violated: Total transaction amount exceeds 1,00,000 Rs

        return "OK"  # No rule violated for any card
    else:
        
        return jsonify({'error': 'Request must contain JSON data'}), 400

@app.route('/check3',methods=['POST'])
def process_json3():
    if request.is_json:
        json_data = request.json
        df = pd.read_csv("dataset_1.csv")

        # Drop 'latitude' and 'longitude' features
        df = df.drop(columns=["Unnamed: 0",'latitude', 'longitude'])
        print(df.head())

        # Separate features and target variable
        X = df.drop(columns=['is_fraud'])  # Features
        y = df['is_fraud']  # Target variable

        # Split the dataset into 80% for training and 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, train_size=0.8, random_state=42)

        # Train the Isolation Forest model
        iforest = IsolationForest(n_estimators=100)
        iforest.fit(X_train)

        # Evaluate the model considering 'IsFraud' during testing
        y_pred_test = iforest.predict(X_test)
        y_pred_test[y_pred_test == 1] = 0  # Convert inliers (non-fraud) to 0
        y_pred_test[y_pred_test == -1] = 1  # Convert outliers (fraud) to 1

        # Calculate recall for fraud detection
        recall = recall_score(y_test, y_pred_test)
        
        encryptedHexCardNo=json_data.get("encryptedHexCardNo")
        merchantCategoryCode=json_data.get("merchantCategoryCode")
        transactionAmount=json_data.get("transactionAmount")
        dateTimeTransaction=json_data.get("dateTimeTransaction")
        data={
            "encryptedHexCardNo":encryptedHexCardNo,
    "merchantCategoryCode": merchantCategoryCode,
    "transactionAmount" : transactionAmount,
    "dateTimeTransaction": dateTimeTransaction}
        df_test=pd.DataFrame(data,index=[0])
        y_pred=iforest.predict(df_test)
        if(y_pred!=-1):
            output_dict = {
                        "status": "ALERT",
                        "ruleViolated": ["RULE-003"],
                        "timestamp":"3677"
                    }
        else:
            output_dict = {
                        "status": "OK",
                        "timestamp":"3677"
                    }

            
        return jsonify(output_dict)
    else:
                
        return jsonify({'error': 'Request must contain JSON data'}), 400
    

@app.route('/check4',methods=['POST'])
def process_json4():
    if request.is_json:
        json_data = request.json
        model=None
        df = pd.read_csv("dataset_1.csv")

        # Drop unnecessary features
        df = df.drop(columns=['Unnamed: 0', 'latitude', 'longitude'])

        # Extract features from 'encryptedHexCardNo' column
        # For example, you can extract the length of the hexadecimal string
        df['encryptedHexCardNo_length'] = df['encryptedHexCardNo'].apply(lambda x: len(str(x)))

        # Separate features and target variable
        X = df.drop(columns=['is_fraud'])  # Features
        y = df['is_fraud']  # Target variable

        # Split the dataset into 80% for training and 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, train_size=0.8, random_state=42)

        # Perform dimensionality reduction using PCA
        pca = PCA(n_components=2, random_state=42)
        X_train_pca = pca.fit_transform(X_train)
        X_test_pca = pca.transform(X_test)

        # Train the Local Outlier Factor (LOF) model
        lof = LocalOutlierFactor(n_neighbors=10, novelty=True)
        lof.fit(X_train_pca)

        # Evaluate the LOF model
        y_pred_test = lof.predict(X_test_pca)


        # Calculate recall for fraud detection
        recall = recall_score(y_test, y_pred_test)
        
        encryptedHexCardNo=json_data.get("encryptedHexCardNo")
        merchantCategoryCode=json_data.get("merchantCategoryCode")
        transactionAmount=json_data.get("transactionAmount")
        dateTimeTransaction=json_data.get("dateTimeTransaction")
        data={
    "merchantCategoryCode": merchantCategoryCode,
    "transactionAmount" : transactionAmount,
    "dateTimeTransaction": dateTimeTransaction}
        df_test=pd.DataFrame(data,index=[0])
        y_pred=LOF.predict(df_test)
        if(y_pred!=-1):
            output_dict = {
                        "status": "ALERT",
                        "ruleViolated": ["RULE-003"],
                        "timestamp":"3677"
                    }
        else:
            output_dict = {
                        "status": "OK",
                        "timestamp":"3677"
                    }

            
        return jsonify(output_dict)
    else:
                
        return jsonify({'error': 'Request must contain JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
