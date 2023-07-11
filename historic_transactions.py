import os.path
import pandas as pd
from pandas.api.types import is_datetime64_dtype, is_object_dtype, is_integer_dtype

CURRENT_DATE = '2023-03-26'
FACTOR = 'factor'
FILENAME = 'historic_transactions.csv'
PARTIAL_AMOUNT = 'partial_amount'
TOTAL_AMOUNT = 'total_amount'
TRANSACTION_DATE = 'transaction_date'
TRANSACTION_ID = 'transaction_id'
TRANSACTION_AMOUNT = 'transaction_amount'


class EmptyDataFrameError(Exception):
    """DataFrame empty - loading exception failed"""


class NoTransactionDateError(Exception):
    """No transaction date column found in data"""


class NoTransactionIdError(Exception):
    """No transaction id column found in data"""


class NoTransactionAmountError(Exception):
    """No transaction amount column found in data"""


class WrongTransactionDateTypeError(Exception):
    """Wrong trancaction date type - values should be of DateTime type"""


class WrongTransactionIdTypeError(Exception):
    """Wrong transaction ID type - values should be of object type"""


class WrongTransactionAmountTypeError(Exception):
    """Wrong transaction amount type - values should be of integer type"""


class Transactions:

    def __init__(self):
        period = pd.Period(CURRENT_DATE)
        self.remaining_days = period.days_in_month - period.day

        self.df = pd.DataFrame()
        self.total_amounts_by_month = pd.DataFrame()
        self.partial_amounts_by_month = pd.DataFrame()
        self.factor_increases = pd.DataFrame()
        self.average_factor_increase = 0.0
        self.estimate = 0

    def load_transactions(self, filename):
        """
        Load a CSV file containing historic transactions
        :param filename:    The CSV file containing the transactions
        """
        if os.path.isfile(filename) is False:
            raise FileNotFoundError

        try:
            self.df = pd.read_csv(r'' + filename)
        except pd.errors.EmptyDataError:
            raise EmptyDataFrameError

        if TRANSACTION_DATE in self.df.columns:
            try:
                self.df[TRANSACTION_DATE] = pd.to_datetime(self.df[TRANSACTION_DATE], format='%Y-%m-%d')
            except ValueError:
                raise WrongTransactionDateTypeError

    def validate_transactions_columns(self):
        """
        Validate the transactions dataframe for the following:
        * The transaction date column is present
        * The transaction ID column is present
        * The transaction amount column is preset
        * The transaction date is a DateTime type
        * The transaction ID is an object type
        * THe transaction amount is an integer
        """
        if TRANSACTION_DATE not in self.df.columns:
            raise NoTransactionDateError

        if TRANSACTION_ID not in self.df.columns:
            raise NoTransactionIdError

        if TRANSACTION_AMOUNT not in self.df.columns:
            raise NoTransactionAmountError

        if is_datetime64_dtype(self.df[TRANSACTION_DATE]) is False:
            raise WrongTransactionDateTypeError

        if is_object_dtype(self.df[TRANSACTION_ID]) is False:
            raise WrongTransactionIdTypeError

        if is_integer_dtype(self.df[TRANSACTION_AMOUNT]) is False:
            raise WrongTransactionAmountTypeError

    def calculate_total_amounts_by_month(self):
        """
        Calculate the total transaction amount per month
        """
        self.total_amounts_by_month = \
            self.df.groupby(pd.Grouper(key=TRANSACTION_DATE, freq="M")) \
                .agg({TRANSACTION_AMOUNT: sum})
        self.total_amounts_by_month.columns = [TOTAL_AMOUNT]

    def calculate_partial_amount(self, x):
        """
        Lambda function to calculate the partial transaction amount per month
        :param x: Dataframe containing all the transactions for a single month
        """
        year = x[TRANSACTION_DATE].dt.year.iloc[0]
        month = x[TRANSACTION_DATE].dt.month.iloc[0]

        period = pd.Period(month=month, year=year, freq='D')
        end_day = period.days_in_month - self.remaining_days

        mask = (x[TRANSACTION_DATE] >= pd.Timestamp(year, month, 1)) & (
                x[TRANSACTION_DATE] <= pd.Timestamp(year, month, end_day))
        partial = x[mask]
        partial_amount = partial[TRANSACTION_AMOUNT].sum()
        return partial_amount

    def calculate_partial_amounts_by_month(self):
        """
        Calculate the partial transaction amount, excluding the last n days from the month
        """
        self.partial_amounts_by_month = self.df.groupby(pd.Grouper(key=TRANSACTION_DATE, freq="M")) \
            .apply(self.calculate_partial_amount) \
            .to_frame(PARTIAL_AMOUNT)

    def calculate_factor_increases(self):
        """
        Calculate the factor increase between the partial transaction amount (with n days remaining) and the total
        transaction amount
        """
        self.factor_increases = self.total_amounts_by_month.join(self.partial_amounts_by_month, on=TRANSACTION_DATE)
        self.factor_increases[FACTOR] = self.factor_increases[TOTAL_AMOUNT] / self.factor_increases[PARTIAL_AMOUNT]

        # Exclude the incomplete month from the amount factor calculations
        self.factor_increases.drop(self.factor_increases.tail(1).index, inplace=True)

    def generate_estimate(self):
        """
        Generate the estimate for the target month using partial transaction amount and average factor increase
        """
        self.average_factor_increase = self.factor_increases[FACTOR].mean()

        partial_amount = self.partial_amounts_by_month[PARTIAL_AMOUNT].iloc[-1]
        self.estimate = round(partial_amount * self.average_factor_increase)


def main():
    print("Current date targeted: " + CURRENT_DATE + "\n")
    t = Transactions()
    t.load_transactions(FILENAME)
    t.validate_transactions_columns()

    t.calculate_total_amounts_by_month()
    print("Total transaction amounts by month:\n")
    print(t.total_amounts_by_month)
    print()

    t.calculate_partial_amounts_by_month()
    print("Partial amounts (excluding the last " + str(t.remaining_days) + " days from results):\n")
    print(t.partial_amounts_by_month)
    print()

    t.calculate_factor_increases()
    print("Factor increase in partial amounts (" + str(t.remaining_days) + " days remaining) versus total amounts per "
                                                                           "month:\n")
    print(t.factor_increases)
    print()

    t.generate_estimate()
    print("Average factor increase: " + str(t.average_factor_increase) + "\n")

    estimate_date = pd.to_datetime(CURRENT_DATE) + pd.offsets.MonthEnd()
    print("Estimated amount for " + estimate_date.strftime('%Y-%m-%d') + ": " + str(t.estimate))


main()
