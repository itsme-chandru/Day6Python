"""
performs various operations in sql and python.
prints some to console.
final request_info database is written as json
"""
from datetime import datetime
import json
import logging
import mysql.connector


logging.basicConfig(filename="test.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=1)


class Users:
    """
    main class to create users and has functions to connect and write data to db
    """
    logging.info("The class is called and the operations will start")
    reason = ""
    validation_msg = ""
    success_or_failure = ""
    request_id = 0

    def __init__(self):
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.date_of_birth = None
        self.age = None
        self.gender = None
        self.nationality = None
        self.city = None
        self.state = None
        self.pincode = None
        self.qualification = None
        self.salary = None
        self.pan_number = None

    def test_first_name(self, f_name):
        """
         assigns the first name to the variable
         :return: true or false based on operations
        """

        if len(f_name) == 0:
            self.first_name = "NULL"
            self.validation_msg += "First Name is empty "
            return False

        if len(f_name) != 0:
            self.first_name = f_name
        return True

    def test_last_name(self, l_name):
        """
        assigns the last name to the variable
        :return: true or false based on operations
        """

        if len(l_name) == 0:
            self.last_name = "NULL"
            self.validation_msg += "Last Name is empty "

            return False
        if len(l_name) != 0:
            self.last_name = l_name
        return True

    def test_date_of_birth(self, dob):
        """
        assigns the dob to the variable
        :return: true or false based on operations
        """

        try:
            self.date_of_birth = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            self.date_of_birth = datetime(1800, 1, 1)
            self.validation_msg += "Invalid input for DOB  "
            return False

        return True

    def calculate_age(self, birthdate):
        """
        calculates the age based on birthday given as input
        :return: the calculated age
        """
        today = datetime.today()
        self.age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))
        return self.age

    def test_gender(self, gen):
        """
         assigns the gender to the variable
         :return: true or false based on operations
        """

        if len(gen) == 0:
            self.gender = "NULL"
            ret_stmnt = False
            self.validation_msg += "Invalid input Gender Empty  "

        else:
            self.gender = gen
            ret_stmnt = True

        return ret_stmnt

    def eligibility_age(self):
        """
         checks the eligibility of age and gender based on requirements
         :return: true or false based on operations
        """
        if self.age < 21 and self.gender in ["male", "Male"]:
            self.reason = "Age should be greater than 21 Yrs for Male "
            ret_stmnt = False
        elif self.age < 18 and self.gender in ["female", "Female"]:
            ret_stmnt = False
            self.reason = "Age should be greater than 18 Yrs for Female "
        else:
            self.reason = ""
            ret_stmnt = True
        return ret_stmnt

    def test_nationality(self, nat):
        """
         assigns nationality to the variable
         :return: true or false based on operations
        """

        if nat == "" or nat not in ["Indian", "American"]:
            self.nationality = "NULL"
            self.reason += "Nationality should be “Indian” or “American”.  "
            ret_stmnt = False
        else:
            self.nationality = nat
            ret_stmnt = False
        return ret_stmnt

    def test_city(self, cit):
        """
         assigns the city name to the variable
         :return: true or false based on operations
        """

        if len(cit) == 0:
            ret_stmnt = False
            self.city = "NULL"
            self.validation_msg += "City is empty invalid input  "

        else:
            self.city = cit
            ret_stmnt = True

        return ret_stmnt

    def test_state(self, sta):
        """
         assigns the state name to the variable
         :return: true or false based on operations
        """

        if len(sta) == 0 or sta not in ["Andhra Pradesh", "Arunachal Pradesh",
                                        "Assam", "Bihar", "Chhattisgarh", "Karnataka",
                                        "Madhya Pradesh", "Odisha",
                                        "Tamil Nadu", "Telangana", "West Bengal"]:
            self.state = "NULL"
            ret_stmnt = False
            self.reason += "Invalid input for state  "
        else:
            self.state = sta
            ret_stmnt = True
        return ret_stmnt

    def test_pincode(self, pin):
        """
         assigns the pincode to the variable
         :return: true or false based on operations
        """

        if len(pin) == 0 or len(pin) != 6:
            self.pincode = 000000
            ret_stmnt = False
            self.validation_msg += "Empty pin code "

        else:
            self.pincode = int(pin)
            ret_stmnt = True

        return ret_stmnt

    def test_qualification(self, quali):
        """
         assigns the qualifications to the variable
         :return: true or false based on operations
        """

        if len(quali) == 0:
            ret_stmnt = False
            self.qualification = "NULL"
            self.validation_msg += "Empty Qualification Invalid input  "
        else:
            self.qualification = quali
            ret_stmnt = True
        return ret_stmnt

    def test_salary(self, sal):
        """
         checks elgibility of the salary to the variable
         :return: true or false based on operations
        """

        if len(sal) == 0:
            self.salary = 0
            self.validation_msg += "Empty salary Invalid input  "
            ret_stmnt = False
        elif int(sal) < 10000:
            self.salary = 0
            self.reason = "Salary should not be less than 10,000  "
            ret_stmnt = False
        elif int(sal) > 90000:
            self.salary = 0
            self.reason = "Salary Should not be greater than 90,000  "
            ret_stmnt = False
        else:
            self.salary = int(sal)
            ret_stmnt = True

        return ret_stmnt

    def test_pan(self, pan):
        """
         assigns the pan number  to the variable
         :return: true or false based on operations
        """
        self.pan_number = "NULL"
        if pan == "" or len(pan) != 10:
            ret_stmnt = False
            self.pan_number = "NULL"
            self.validation_msg += "Invalid Pan number "
        else:
            self.pan_number = pan
            ret_stmnt = True

        return ret_stmnt

    def test_success_or_failure(self):
        """
         checks whether the request was a success or a failure based on the reason statements
         :return: success or failure
        """
        if self.reason == "" and self.validation_msg == "":
            self.success_or_failure = "Success  "
            self.reason = ""
        elif len(self.validation_msg) != 0:
            self.success_or_failure = "Validation Failure  "
            self.reason = self.validation_msg
        else:
            self.success_or_failure = "Failure  "
        return self.success_or_failure

    def null_all_strings(self):
        """
         clears all the string present and makes it to null
         :return: none
        """
        self.reason = ""
        self.validation_msg = ""
        self.success_or_failure = ""

    def get_details(self):
        """
         gets the details and performs all the functions
         :return: none
        """
        logging.info("The get details function is called and the operations will start")
        first_name = input("Enter your first name: ")
        self.test_first_name(first_name)
        last_name = input("Enter your last name: ")
        self.test_last_name(last_name)
        date_of_birth = input("Enter your date of birth (YYYY/MM/DD): ")
        self.test_date_of_birth(date_of_birth)
        print("the age is ", self.calculate_age(self.date_of_birth))
        gender = input("Enter your gender: ")
        self.test_gender(gender)
        self.eligibility_age()
        nationality = input("Enter your nationality (Indian/American): ")
        self.test_nationality(nationality)
        city = input("Enter your city: ")
        self.test_city(city)
        state = input("Enter your state: ")
        self.test_state(state)
        pincode = input("Enter your pin code: ")
        self.test_pincode(pincode)
        qualification = input("Enter your qualification: ")
        self.test_qualification(qualification)
        salary = input("Enter your salary: ")
        self.test_salary(salary)
        pan_number = input("Enter your pan number: ")
        self.test_pan(pan_number)
        print(self.test_success_or_failure())
        print(self.reason)
        print(self.first_name, self.last_name, self.date_of_birth,
              self.gender, self.nationality, self.city, self.state,
              self.pincode, self.qualification,
              self.salary,
              self.pan_number)
        logging.info("The get details functions has ended")

    def push_to_requestinfo_db(self):
        """
         inserts all the data to the database
         :return: none
        """
        logging.info("The push to request info db function is called")
        mydb = mysql.connector.connect(host="localhost",
                                       user=config['db_user'],
                                       passwd=config['db_pwd'],
                                       database=config['db_name'])
        mycursor = mydb.cursor()
        add_user = ("Insert into request_info(First_Name,"
                    "Last_Name,DOB,Gender,Nationality,City,"
                    "State,Pincode,Qualification,Salary,PAN_Number) "
                    "Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
        data_user = (
            self.first_name, self.last_name, self.date_of_birth,
            self.gender, self.nationality, self.city, self.state,
            self.pincode, self.qualification, self.salary, self.pan_number)
        mycursor.execute(add_user, data_user)
        self.request_id = mycursor.lastrowid
        mydb.commit()
        print("Data inserted into 1stDB successfully ")
        logging.info("Data is inserted into request info db successfully")

    def push_to_responseinfo_db(self):
        """
         inserts all the responses to the 2nd database
         :return: none
        """
        logging.info("The push to response info db function is called")
        mydb = mysql.connector.connect(host="localhost",
                                       user=config['db_user'],
                                       passwd=config['db_pwd'],
                                       database=config['db_name'])
        mycursor = mydb.cursor()
        add_response = ("Insert into Response_Info(request_id, response, reason)"
                        "Values(%s, %s, %s)")
        data_response = (self.request_id, self.success_or_failure, self.reason)
        mycursor.execute(add_response, data_response)
        mydb.commit()
        print("Data inserted into 2ndDB successfully\n")
        logging.info("Data is inserted into response info db successfully")


def print_result_tojson():
    """
     retrieves all the data from the database and creates a nested dict and writes to a file
     :return: none
    """
    logging.info("writing to json file is called")
    mydb = mysql.connector.connect(host="localhost",
                                   user=config['db_user'],
                                   passwd=config['db_pwd'],
                                   database=config['db_name'])

    mycursor = mydb.cursor()
    get_response = "Select * from Response_Info"
    mycursor.execute(get_response, )
    result = mycursor.fetchall()
    mydict = {}
    for i in range(len(result)):
        mydict[i] = {}
        if result[i][2] == "Success  ":
            mydict[i]["Request_id"] = result[i][1]
            mydict[i]["Response"] = result[i][2]
        elif result[i][2] == "Validation Failure  ":
            mydict[i]["Request_id"] = result[i][1]
            mydict[i]["Response"] = result[i][2]
            mydict[i]["Reason"] = result[i][3]
        elif result[i][2] == "Failure  ":
            mydict[i]["Request_id"] = result[i][1]
            mydict[i]["Response"] = result[i][2]
            mydict[i]["Reason"] = result[i][3]
        print(mydict[i])
        dump = json.dumps(mydict[i])
        obj = json.loads(dump)

        with open("result.txt", mode="a", encoding="UTF-8") as response_file:
            response_file.write(str(obj))
            response_file.write("\n")
            response_file.close()
    logging.info("the write to json function has ended")


if __name__ == '__main__':
    file_name = "configfile.config"
    with open(file_name, mode='r', encoding="UTF-8") as config:
        contents = config.read()
        config = eval(contents)
    num_users = int(input("enter the number of users\n"))
    logging.info("class object is created")
    create_users = Users()
    while num_users != 0:
        create_users.get_details()
        create_users.push_to_requestinfo_db()
        create_users.push_to_responseinfo_db()
        create_users.null_all_strings()
        num_users -= 1
    print_result_tojson()
    logging.info("program is finished")
