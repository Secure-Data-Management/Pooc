import csv
from random import randrange
import datetime
import os

names = ['Michael', 'Jones', 'Williams', 'John', 'Rose', 'Daniel', 'Jonathan', 'Donald', 'Julia', 'Stephanie', 'Karl', 'Laura']
banks = ['ABN AMRO','Rabobank','ING','bunq','SNS Bank']
fieldnames = ['transaction_type','destination','transaction','transaction_date','bank']

def random_date():

    # This function will return a random datetime between two datetime 

    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2020, 1, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days) 
    return random_date

def generate_record(filename, nb_transactions_max = 20, amount_transaction_max = 1000):
    with open("data_users/" + filename, 'w') as new_file:
        #Generate csv file with the following fields corresponding to the record of a client
        
        csv_writer = csv.DictWriter(new_file, delimiter=',', fieldnames = fieldnames)

        nb_transactions = randrange(nb_transactions_max) #number of records in this file
        amount_transaction = randrange(amount_transaction_max)

        for t in range(nb_transactions):
            #random for each transaction
            n_name = randrange(len(names))#Destination
            transaction = randrange(amount_transaction)#amount of transaction
            b = randrange(2)#Credit or Debit
            n_bank = randrange(len(banks))
            if(b):
                csv_writer.writerow({'transaction_type':'Credit','destination':names[n_name], 'transaction':transaction, 'transaction_date':random_date(), 'bank':banks[n_bank]})
            else:
                csv_writer.writerow({'transaction_type':'Debit','destination':names[n_name], 'transaction':transaction, 'transaction_date':random_date(), 'bank':banks[n_bank]})


def get_keywords(file: str, keyword_type_queried=None): #return keywords from a specific file
    with open(file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', fieldnames = fieldnames)
        keywords=[]
        if keyword_type_queried==None: #return all keywords in the file
            for row in reader:
                for keyword_type in fieldnames:
                  keywords.append(row[keyword_type]) if row[keyword_type] not in keywords else keywords
        else:
            for row in reader: #return keywords in the file from a specific type
               keywords.append(row[keyword_type_queried]) if row[keyword_type_queried] not in keywords else keywords   
    return keywords


def generate(nb_users=10, nb_files_max=5): #for each user generates a number of files, and for each file generates a number of records
    #creating /data_users folder
    if(os.path.isdir("./data_users")==True):
        filelist = [ f for f in os.listdir("./data_users") if f.endswith(".csv") ]
        for f in filelist:
            os.remove(os.path.join("./data_users", f))
        print("Previous data deleted")
    else:
        os.mkdir("./data_users")

    for records in range(nb_users):
        nb_files = randrange(nb_files_max)
        for f in range(nb_files):
            filename = names[records]+'_'+str(f)+'.csv'
            generate_record(filename)
            print(str(filename)+" generated")
    
if __name__ == '__main__':
    generate()
    # print(get_keywords('data_users/John_3.csv',"destination"))
