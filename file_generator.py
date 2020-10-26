import csv
from random import randrange
import datetime


def random_date():
    # This function will return a random datetime between two datetime

    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2020, 1, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def generate_csv(nb_users, max_bank_balance):
    with open('bank_data.csv', 'w') as new_file:
        # Generate csv file with the following fields 'userid','lastname','bank balance','registration date'
        names = ['Michael', 'Jones', 'Williams', 'John', 'Rose', 'Daniel', 'Jonathan', 'Donald', 'Julia', 'Stephanie', 'Karl', 'Laura']
        csv_writer = csv.writer(new_file, delimiter=',')

        csv_writer.writerow(['userid', 'lastname', 'bank balance', 'registration date'])
        for i in range(nb_users):
            n_name = randrange(len(names))
            bank_balance = randrange(max_bank_balance)
            csv_writer.writerow([i, names[n_name], bank_balance, random_date()])


def get_keywords(file: str):
    with open(file, 'w') as f:
        reader = csv.reader(file)
        # select the right field and return them as keyword


if __name__ == '__main__':
    generate_csv(5, 10000)
