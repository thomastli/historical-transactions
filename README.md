# historical-transactions
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/thomastli/historical-transactions/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/thomastli/historical-transactions/tree/main)
[![CodeFactor](https://www.codefactor.io/repository/github/thomastli/historical-transactions/badge)](https://www.codefactor.io/repository/github/thomastli/historical-transactions) 
[![codecov](https://codecov.io/gh/thomastli/historical-transactions/branch/main/graph/badge.svg?token=hS7WpH8DMh)](https://codecov.io/gh/thomastli/historical-transactions)

Predicts future transaction amounts based on historical transaction data using Python and Pandas.

## Usage
* `transactions.ipyndb` contains the executable and unit tests in a Jupyter notebook for the assessment.
* `historicaL_transactions.py` is a standalone `.py` copy of the solution.
* `tests/` contains various files used by the unit tests.

The demo uses `pandas` to perform the data analysis. 

Unit tests are written in `pytest` and utilize `ipytest` to get them to work in the `Jupyter` notebook.

### Output
`transactions.ipynb` / `historical_transactions.py` will output the following:
* Total transaction amounts by month.
* Partial transaction amounts (excluding the last n days from results).
* Factor increase in partial amounts (n days remaining) versus total monthly amounts.
* Average factor increase of all completed months.
* Estimated transaction amount (volume) for the end of the current month.

### Limitations
* Validation of the `DataFrame` is somewhat basic.
* Custom exceptions could provide more specific information to help users debug errors.
* Unit tests could include more corner cases of unexpected data or failures - most of the tests are written
to test the correct path of execution.

### Future considerations
* More specific validation of the `DataFrame` contents generated from `historic_transactions.csv`
* More verbose custom exception messages/information.
* Unit tests around edge cases in standard execution.
* Generate plots of the total amount, partial amount, and factor increases.
