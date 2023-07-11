from pandas.testing import assert_frame_equal
from historic_transactions import Transactions, EmptyDataFrameError, NoTransactionDateError, NoTransactionIdError, \
    NoTransactionAmountError, WrongTransactionDateTypeError, WrongTransactionIdTypeError, \
    WrongTransactionAmountTypeError
import pandas as pd
import pytest

FILENAME = 'historic_transactions.csv'
NON_EXISTENT_FILE = "non-existent_file"
EMPTY_FILE = "tests/empty.csv"

NO_TRANSACTION_DATE = "tests/no_transaction_date.csv"
NO_TRANSACTION_ID = "tests/no_transaction_id.csv"
NO_TRANSACTION_AMOUNT = "tests/no_transaction_amount.csv"
WRONG_TRANSACTION_DATE_TYPE = "tests/wrong_transaction_date_type.csv"
WRONG_TRANSACTION_ID_TYPE = 'tests/wrong_transaction_id_type.csv'
WRONG_TRANSACTION_AMOUNT_TYPE = 'tests/wrong_transaction_amount_type.csv'

TOTAL_AMOUNTS_BY_MONTH = 'tests/total_amounts_by_month.csv'
PARTIAL_AMOUNTS_BY_MONTH = 'tests/partial_amounts_by_month.csv'
FACTOR_INCREASES = 'tests/factor_increases.csv'


def test_load_transactions():
    t = Transactions()

    with pytest.raises(FileNotFoundError):
        t.load_transactions(NON_EXISTENT_FILE)

    with pytest.raises(EmptyDataFrameError):
        t.load_transactions(EMPTY_FILE)

    t.load_transactions(FILENAME)


def test_validate_transactions():
    t = Transactions()

    with pytest.raises(NoTransactionDateError):
        t.load_transactions(NO_TRANSACTION_DATE)
        t.validate_transactions_columns()

    with pytest.raises(NoTransactionIdError):
        t.load_transactions(NO_TRANSACTION_ID)
        t.validate_transactions_columns()

    with pytest.raises(NoTransactionAmountError):
        t.load_transactions(NO_TRANSACTION_AMOUNT)
        t.validate_transactions_columns()

    with pytest.raises(WrongTransactionDateTypeError):
        t.load_transactions(WRONG_TRANSACTION_DATE_TYPE)
        t.validate_transactions_columns()

    with pytest.raises(WrongTransactionIdTypeError):
        t.load_transactions(WRONG_TRANSACTION_ID_TYPE)
        t.validate_transactions_columns()

    with pytest.raises(WrongTransactionAmountTypeError):
        t.load_transactions(WRONG_TRANSACTION_AMOUNT_TYPE)
        t.validate_transactions_columns()

    t.load_transactions(FILENAME)
    t.validate_transactions_columns()


def test_calculate_total_amounts():
    t = Transactions()
    t.load_transactions(FILENAME)
    t.calculate_total_amounts_by_month()

    expected_result = pd.read_csv(r'' + TOTAL_AMOUNTS_BY_MONTH, header=0, index_col=0)
    assert_frame_equal(expected_result.reset_index(drop=True), t.total_amounts_by_month.reset_index(drop=True))


def test_calculate_partial_amounts():
    t = Transactions()
    t.load_transactions(FILENAME)
    t.calculate_partial_amounts_by_month()

    expected_result = pd.read_csv(r'' + PARTIAL_AMOUNTS_BY_MONTH, header=0, index_col=0)
    assert_frame_equal(expected_result.reset_index(drop=True), t.partial_amounts_by_month.reset_index(drop=True))


def test_calculate_factor_increases():
    t = Transactions()
    t.load_transactions(FILENAME)

    t.calculate_total_amounts_by_month()
    t.calculate_partial_amounts_by_month()
    t.calculate_factor_increases()

    expected_result = pd.read_csv(r'' + FACTOR_INCREASES, header=0, index_col=0)
    assert_frame_equal(expected_result.reset_index(drop=True), t.factor_increases.reset_index(drop=True))


def test_generate_estimate():
    t = Transactions()
    t.load_transactions(FILENAME)

    t.calculate_total_amounts_by_month()
    t.calculate_partial_amounts_by_month()
    t.calculate_factor_increases()

    t.generate_estimate()
    assert (t.estimate == 371871)
