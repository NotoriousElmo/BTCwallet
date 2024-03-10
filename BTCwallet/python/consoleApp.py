import requests

API_BASE_URL = 'http://localhost:4000'

def get_exchange_rate():
    response = requests.get(f'{API_BASE_URL}/exchange-rate')
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch exchange rate")
        return None

def view_transactions():
    response = requests.get(f'{API_BASE_URL}/transactions')
    if response.status_code == 200:
        transactions = response.json()
        for transaction in transactions:
            print(transaction)
    else:
        print("Failed to fetch transactions")

def show_balance():
    response = requests.get(f'{API_BASE_URL}/balance')
    if response.status_code == 200:
        balance = response.json()
        print("Balance in UTC:", balance["Balance in UTC"])
        print("Balance in EUR:", balance["Balance in EUR"])
    else:
        print("Failed to fetch balance")

def create_transaction():
    euros = input("Enter the amount in Euros to transfer: ")
    try:
        transefer_amount = float(euros)
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return
    data = {'amount': transefer_amount}
    response = requests.post(f'{API_BASE_URL}/transfer', json=data)
    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print("Failed to create transaction")

def add_transaction():
    deposit = input("Enter the amount in Euros to deposit: ")
    try:
        deposit_amount = float(deposit)
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return
    data = {"amount": deposit_amount}
    response = requests.post(f'{API_BASE_URL}/deposit', json=data)
    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print("Failed to add deposit")

def main():
    while True:
        print("\nAvailable actions:")
        print("1. View Transactions")
        print("2. Show Balance")
        print("3. Withdraw")
        print("4. Deposit")
        print("5. Exit")
        choice = input("Select an action (1-5): \n\n")

        if choice == '1':
            view_transactions()
        elif choice == '2':
            show_balance()
        elif choice == '3':
            create_transaction()
        elif choice == '4':
            add_transaction()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
