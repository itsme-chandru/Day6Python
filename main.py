from datetime import datetime

import mysql.connector


def establish_connection():
    global mydb
    mydb = mysql.connector.connect(host="localhost", user=config['db_user'], passwd=config['db_pwd'],
                                   database=config['db_name'])


class AddUser:
    reason = ''

    def _init_(self):
        self.first_name = None,
        self.middle_name = None,
        self.last_name = None,
        self.date_of_birth = None,
        self.age = None,
        self.gender = None,
        self.nationality = None,
        self.city = None,
        self.state = None,
        self.pincode = None,
        self.qualification = None,
        self.salary = None,
        self.pan_number = None
        self.request_id = None
        self.success_or_failure = None

    def validate_first_name(self, f_name):
        self.first_name = "-"
        ans = True
        if f_name == "":
            self.reason += "First name is empty. "
            ans = False
        else:
            self.first_name = f_name
        return ans

    def validate_mid_name(self, m_name):
        self.middle_name = m_name
        return True

    def validate_last_name(self, l_name):
        self.last_name = "-"
        ans = True
        if l_name == "":
            self.reason += "Last name is empty. "
            ans = False
        else:
            self.last_name = l_name
        return ans

    def validate_date_of_birth(self, dob):
        ans = True

        try:
            self.date_of_birth = datetime.strptime(dob, "%Y/%m/%d")
        except ValueError:
            self.date_of_birth = datetime(1800, 1, 1)
            self.reason += "Invalid Input for DOB. "
            ans = False

        return ans

    def calculate_age(self, birthdate):
        today = datetime.today()
        self.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return self.age

    def validate_gender(self, gen):
        self.gender = '-'
        ans = True
        if gen == "" or gen not in ("Male", "Female"):
            self.reason += "Gender is invalid. "
            ans = False
        else:
            self.gender = gen
        return ans

    def validate_age_gender(self, age, gender):
        if age is not None and gender != "-":
            if age < 21 and gender == "Male":
                self.reason += "Age should be 21 or above for male. "
            if age < 18 and gender == "Female":
                self.reason += "Age should be 18 or above for female. "

    def validate_nationality(self, nat):
        self.nationality = '-'
        ans = True
        if nat == "":
            self.reason += "Nationality is empty. "
            ans = False
        elif nat not in ("Indian", "American"):
            self.nationality = nat
            self.reason += "Nationality should be Indian or American. "
            ans = False
        else:
            self.nationality = nat

        return ans

    def validate_city(self, cit):
        self.city = '-'
        ans = True
        if cit == "":
            self.reason += "City is empty. "
            ans = False
        else:
            self.city = cit
        return ans

    def validate_state(self, sta):
        self.state = '-'
        ans = True
        if sta == "":
            self.reason += "State is empty. "
            ans = False
        elif sta not in (
                "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Karnataka", "Tamil Nadu",
                "Telangana",
                "West Bengal"):
            self.state = sta
            self.reason += "State entered is not valid. "
            ans = False
        else:
            self.state = sta

        return ans

    def validate_pincode(self, pin):
        self.pincode = 0
        ans = True
        if pin == "":
            self.reason += "Pin is empty. "
            ans = False
        elif len(pin) != 6:
            self.reason += "Invalid pin. "
            ans = False
        else:
            self.pincode = int(pin)

        return ans

    def validate_qualification(self, quali):
        self.qualification = '-'
        ans = True
        if quali == "":
            self.reason += "Qualification is empty. "
            ans = False
        else:
            self.qualification = quali

        return ans

    def validate_salary(self, sal):
        self.salary = 0
        ans = True
        if sal == "":
            self.reason += "Salary is empty. "
            ans = False
        elif int(sal) < 10000:
            self.reason += "Salary is less than expected. "
            ans = False
        elif int(sal) > 90000:
            self.reason += "Salary is more than expected. "
            ans = False
        else:
            self.salary = int(sal)

        return ans

    def validate_pan(self, pan):
        self.pan_number = '-'
        ans = True
        if pan == "":
            self.reason += "Pan number is empty"
            ans = False
        elif len(pan) != 10:
            self.pan_number = pan
            self.reason += "Pan number should be 10 digits"
            ans = False
        else:
            self.pan_number = pan

        return ans

    def validate_success_or_failure(self):
        if self.reason == "":
            self.success_or_failure = "Success"
            self.reason = "-"
        else:
            self.success_or_failure = "Failure"

    def get_details(self):
        first_name = input("Enter your first name: ")
        self.validate_first_name(first_name)
        middle_name = input("Enter your middle name (optional) : ")
        self.validate_mid_name(middle_name)
        last_name = input("Enter your last name: ")
        self.validate_last_name(last_name)
        date_of_birth = input("Enter your date of birth (YYYY/MM/DD): ")
        self.validate_date_of_birth(date_of_birth)
        gender = input("Enter your gender: ")
        self.validate_gender(gender)
        self.calculate_age(self.date_of_birth)
        self.validate_age_gender(self.age, self.gender)
        nationality = input("Enter your nationality (Indian/American): ")
        self.validate_nationality(nationality)
        city = input("Enter your city: ")
        self.validate_city(city)
        state = input("Enter your state: ")
        self.validate_state(state)
        pincode = input("Enter your pin code: ")
        self.validate_pincode(pincode)
        qualification = input("Enter your qualification: ")
        self.validate_qualification(qualification)
        salary = input("Enter your salary: ")
        self.validate_salary(salary)
        pan_number = input("Enter your pan number: ")
        self.validate_pan(pan_number)
        self.validate_success_or_failure()

    def push_request_to_db(self):
        mycursor = mydb.cursor()
        add_user = ("Insert into Request_Info(first_name, middle_name, last_name, date_of_birth, gender, nationality, "
                    "city, state, pincode, qualification, salary, pan_number)"
                    "Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
        data_user = (
            self.first_name, self.middle_name, self.last_name, self.date_of_birth, self.gender, self.nationality,
            self.city,
            self.state, self.pincode, self.qualification, self.salary, self.pan_number)
        mycursor.execute(add_user, data_user)

        self.request_id = mycursor.lastrowid
        mydb.commit()

    def push_response_to_db(self):
        mycursor = mydb.cursor()
        add_response = ("Insert into Response_Info(request_id, response, reason)"
                        "Values(%s, %s, %s)")
        data_response = (self.request_id, self.success_or_failure, self.reason)
        mycursor.execute(add_response, data_response)

        mydb.commit()


if __name__ == '__main__':
    file_name = "external.config"
    with open(file_name, mode='r') as config_file:
        contents = config_file.read()
        config = eval(contents)

        establish_connection()

        user = AddUser()
        user.get_details()
        user.push_request_to_db()
        user.push_response_to_db()

        def select_from_responseinfo_db(self):
            mydb = mysql.connector.connect(host="localhost", user=config['db_user'], passwd=config['db_pwd'],
                                           database=config['db_name'])
            mycursor = mydb.cursor()
            sql = "select request_id,response from response_info where response = %s"
            params = "Success  "
            mycursor.execute(sql, (params,))
            res = mycursor.fetchall()
            for i in res:
                print(i)
            mydb.commit()