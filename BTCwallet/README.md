For setup:
* Open Docker.
* Go to the BTCwallet application and open terminal.
* Use command `docker-compose up`.
* Test the application using Postman and the instructions below or use the consoleApp.
* Go to python folder using `cd python`.
* Use command `python consoleApp.py`.
* Type 1 - to view all transactions, 2 - to view current wallet balance,
  3 - to create a transfer of given amount, 4 - to deposit a given amount, 5 - to exit.


1) To list all transactions use Postman to generate a GET request to `http://localhost:4000/transactions`.
2) To view the current balance use Postman to generate a GET request to `http://localhost:4000/balance`.
3) To create a transaction use Postman to generate a POST request to `http://localhost:4000/transfer`,
    with body of json looking like:
   `{
      "amount": amount you want to transfer (example: 40, 0.5, etc)
   }`
   If the amount is less than 0.00001 BTC then the transfer doesn't work, since the amount is too small.
   Also if the amount to transfer is more than the current balance then the transfer also doesn't go through.
5) To add money to your walle use Postman to generate a POST request to `http://localhost:4000/deposit`,
   with body of json looking like:
   `{
      "amount": amount you want to deposit (example: 40, 0.5, etc)
   }`
   If the amount is less than 0.00001 BTC then the deposit doesn't work, since the amount is too small.
