import json
from flask import Flask, request
from flask import jsonify
import mysql.connector
import requests

app = Flask(__name__)

def getExchangeRate():
    response = requests.get('http://api-cryptopia.adca.sh/v1/prices/ticker')

    data = response.json()

    for item in data["data"]:
        if item["symbol"] == "BTC/EUR":
            btc_eur_result = item
            break 

    return float(btc_eur_result['value'])

@app.route('/transactions', methods=['GET'])
def viewTransactions():

    connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database='db')
    print("DB connected")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    transactions_list = [dict(zip([key[0] for key in cursor.description], row)) for row in transactions]
    connection.close()
    return jsonify(transactions_list)

@app.route('/balance', methods=['GET'])
def showBalance():

    connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database='db')
    print("DB connected")
    cursor = connection.cursor()
    cursor.execute('SELECT amount FROM transactions WHERE spent = FALSE')

    unspentTransactions = cursor.fetchall()

    balanceInUTC = 0
    for transaction in unspentTransactions:
        balanceInUTC += float(transaction[0])
    
    exchangeRate = getExchangeRate();
    balanceInEUR = balanceInUTC * exchangeRate
    connection.close()
    return {"Balance in UTC": balanceInUTC, "Balance in EUR": round(balanceInEUR, 2)}

@app.route('/transfer', methods=['POST'])
def createTransaction():
    try:
        euros = request.json.get('amount')
        exchangeRate = getExchangeRate()

        btcTransfer = euros / exchangeRate

        if btcTransfer <= 0.00001:
            return {'transfer': 'failure', 'error': 'transfer amount is too small'}

        connection = mysql.connector.connect(
        user='root', password='root', host='mysql', port="3306", database='db')
        print("DB connected")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM transactions WHERE spent = FALSE')
        unspentTransactions = cursor.fetchall()

        totalBalance = 0
        for transaction in unspentTransactions:
            totalBalance += float(transaction[0])

        if totalBalance < btcTransfer:
            connection.close()
            return {'transfer': 'failure', 'error': 'insufficient balance'}

        for transaction in unspentTransactions:
            if (btcTransfer >= float(transaction[1])):
                btcTransfer -= float(transaction[1])
                cursor.execute("UPDATE transactions SET spent = TRUE WHERE transactionID = %s", (transaction[0],))
                if btcTransfer == 0:
                    break
            elif float(transaction[1]) > btcTransfer:
                remainingAmount = float(transaction[1]) - btcTransfer
                cursor.execute("UPDATE transactions SET amount = %s WHERE transactionID = %s", (remainingAmount, transaction[0]))
                cursor.execute("INSERT INTO transactions (amount, spent) VALUES (%s, %s)", (btcTransfer, True))
                btcTransfer = 0
                break

        connection.commit()
        connection.close()
        return {'transfer': 'success'}
    except:
        return {'transfer': 'failure'}

@app.route('/deposit', methods=['POST'])
def addTransaction():

    try:
        deposit = request.json.get('amount')
        exchangeRate = getExchangeRate()

        btcDeposit = deposit / exchangeRate

        if btcDeposit <= 0.00001:
            return {'transfer': 'failure', 'error': 'transfer amount is too small'}

        connection = mysql.connector.connect(
        user='root', password='root', host='mysql', port="3306", database='db')
        print("DB connected")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO transactions (amount, spent) VALUES (%s, %s)", (btcDeposit, False))
        connection.commit();
        connection.close();

        return {'deposit': 'success'}

    except:
        connection.close();
        return {'deposit': 'failure'}

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
