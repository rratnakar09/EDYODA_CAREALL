import mysql.connector


class CareAll:

    def __init__(self):
        # intilize all the instance variables 
        self.name = None
        self.age = None
        self.availability = True
        self.address = None
        self.reviews = 0
        self.fund = 0
        self.total_count = 0
        self.elders_count = 0

    def registerElder(self, data, db_connection):
        # data = [name, age, is_available, address, reviews, fund]
        self.name = data[0]
        self.age = data[1]
        self.availability = data[2]
        self.address = data[3]
        self.reviews = data[4]
        self.fund = data[5]

        # create data bases cursor
        mycursor = db_connection.cursor()

        # create insert query for inserting new elder user in elders table
        insert_query = "INSERT INTO ELDERS (Name,Age,Availability,Address,Reviews, funds) "
        insert_query += "VALUES ( " + "'" + self.name + "', " + str(self.age) + ", " + str(
            self.availability) + ", '" + self.address + "', " + str(self.reviews) + ", " + str(
            self.fund) + ");"

        #print(insert_query)
        mycursor.execute(insert_query)
        db_connection.commit()
        print("New Elder User Registered")

    def registerYounger(self, data, db_connection):
        # data = [name, age, is_available, address, reviews]
        self.name = data[0]
        self.age = data[1]
        self.availability = data[2]
        self.elders_count = 0
        self.address = data[3]
        self.reviews = data[4]

        # create data bases cursor
        mycursor = db_connection.cursor()

        # create insert query for inserting new youth user in youngers table
        insert_query = "INSERT INTO YOUNGERS (Name,Age,Availability,Elders_Count, Address, Reviews ) "
        insert_query += "VALUES( " + "'" + self.name + "', " + str(self.age) + ", " + str(
            self.availability) + ", " + str(self.elders_count) + ", '" + self.address + "', " + str(
            self.reviews) + ");"

        mycursor.execute(insert_query)
        db_connection.commit()

        print("New Youth User Registered")

    def updateElder_Younger(self, db_connection, data_list):
        # based on the charge of younger we will update the the fund remaining, update the total_count of youth,
        # query to update elder table based on elder_name ,elder_id and younger_name
        # data_list = [elder_reg_id, elder_name, y_name, y_reg_id, elder_count]
        mycursor = db_connection.cursor()
        elder_update_query = "UPDATE ELDERS SET availability = '" + False + "', cared_by = '" + str(data_list[2]) + "' WHERE name = '" + str(data_list[1]) + "', reg_id = '" + str(data_list[0]) + "';" 

        mycursor.execute(elder_update_query)
        db_connection.commit()

        mycursor = db_connection.cursor()
        younger_update_query = "UPDATE YOUNGERS SET Elders_Count = '" + data_list[4] + "' WHERE name = '" + str(data_list[2]) + "', reg_id = '" + str(data_list[3]) + "';" 

        mycursor.execute(younger_update_query)
        db_connection.commit()

    # this method is used to search abailable elders who needs care 
    # based on review, loaction a youth will be assigned to take care of.    
    def searchElder(self, db_connection, y_name, y_reg_id):

        # create data bases cursor
        mycursor = db_connection.cursor()

        # create select query for selecting youth user
        select_query = "Select Elders_count, Address, Reviews from YOUNGERS Where Name =" + "'" + y_name + "' AND " + \
                       "Reg_Id =" + str(y_reg_id) + ";"
        #print(select_query)
        mycursor.execute(select_query)
        result = mycursor.fetchall()


        db_connection.commit()

        #print("youngers search complete")
        # local variables
        elder_count = 0
        younger_city = ''
        younger_ratings = 0

        
        for x in result:
            elder_count = x[0]
            younger_city = x[1]
            younger_ratings = x[2]
            print("outer res", x)

            if elder_count < 4:
                # create sql query to select elder
                sel_query = "Select * from ELDERS where address = '" + younger_city + "' and reviews >= " + str(
                    younger_ratings) + " ORDER BY reviews, age limit 1 ;"
                print(sel_query)
                mycursor.execute(sel_query)
                res = mycursor.fetchall()

                db_connection.commit()

                for j in list(res):
                    # (4, 'Babloo', 62, 1, 'Patna', Decimal('0.00'), 15000) the result format of sql query
                    elder_reg_id = j[0]
                    elder_name = j[1]
                    elder_address = j[4]
                    print("elder slected is ", j)
                    print("Please take care of elder person having IDs: " +str(elder_reg_id) + ", name: " + str(j[1]) + " and address: " + str(j[4]))
                    elder_count += 1

                    # call updateElder_Younger()
                    # this method will update the fund remaining and total_count of younger
                    # create a list to pass elder_reg_id, elder_name, y_name, y_reg_id, elder_count
                    data_list = [elder_reg_id, elder_name, y_name, y_reg_id, elder_count]
                    user.updateElder_Younger(db_connection, date_list)

                #print("search complete")

            else:
                print("There is no elder available based on your own reviews and loaction")

    def rateElder(self, db_connection, elder_name, elder_id, reviews):

        # this variable will be used to calculate avg_review which will be updated once this method will be called 
        avg_review = reviews


        # create data bases cursor
        mycursor = db_connection.cursor()

        # create select query for selecting youth user
        review_query = "Select Reviews from ELDERS Where Name =" + "'" + elder_name + "' AND " + \
                       "Reg_Id =" + str(elder_id) + ";"
        print(review_query)
        mycursor.execute(review_query)
        result = mycursor.fetchall()

        db_connection.commit()

        for r in list(result):
            # calculate average reviews
            avg_review = (avg_review + float(r[0])) /2
            # rounf off the review to 2 decimal point to match with the data bases table data type
            avg_review = round(avg_review, 2)

        # query to update the review filed in elder table
        update_review_query = "Update ELDERS SET reviews = " + str(avg_review) + " where reg_id = " + str(elder_id) + \
                              " and name = '" + elder_name + "';"  

        mycursor.execute(update_review_query)
        
        db_connection.commit()

        print("You have sucessfully rated ", elder_name)
        

    def rateYoung(self, db_connection, younger_name, younger_id, reviews):
        # this variable will be used to calculate avg_review which will be updated once this method will be called 
        avg_review = reviews


        # create data bases cursor
        mycursor = db_connection.cursor()

        # create select query for selecting youth user
        review_query = "Select Reviews from YOUNGERS Where Name =" + "'" + younger_name + "' AND " + \
                       "Reg_Id =" + str(younger_id) + ";"
        print(review_query)
        mycursor.execute(review_query)
        result = mycursor.fetchall()

        db_connection.commit()

        for r in list(result):
            # calculate average reviews
            avg_review = (avg_review + float(r[0])) /2
            # rounf off the review to 2 decimal point to match with the data bases table data type
            avg_review = round(avg_review, 2)

        # query to update the review filed in elder table
        update_review_query = "Update YOUNGERS SET reviews = " + str(avg_review) + " where reg_id = " + str(younger_id) + \
                              " and name = '" + younger_name + "';"  

        mycursor.execute(update_review_query)
        
        db_connection.commit()

        print("You have sucessfully rated ", younger_name)

    def taking_care_detail(self, db_connection):

        # create data bases cursor
        mycursor = db_connection.cursor()

        # create select query for selecting youth user
        select_query = "Select Name, Reg_Id from YOUNGERS Where Elders_Count > " + 0 + ";"
        print(select_query)
        mycursor.execute(select_query)
        result = mycursor.fetchall()

        db_connection.commit()

        #print all the youngers names who are taking care of elders
        for x in result:

            print("Name: ", x[0], + " and Reg Ids: " + str(x[1]))

    def youngChapCarying(self, db_connection):

        # create data bases cursor
        mycursor = db_connection.cursor()

        # create select query for selecting youth user
        select_query = "Select Name from YOUNGERS Where Elders_Count > " + 0 + ";"
        print(select_query)
        mycursor.execute(select_query)
        result = mycursor.fetchall()

        db_connection.commit()

        #print all the youngers names who are taking care of elders
        for x in result:
            fetch_query = "Select Name from ELDERS Where Cared_BY = '" +str(x[0])  + "';"
            mycursor.execute(select_query)
            res_fetch = mycursor.fetchall()

            # print all the elders names whome a young chap is taking care of
            print(x[0], "is taking care of: ")
            for eld in res_fetch:
                print(str(eld[0]))

                    
    
        

# Program will start from here 

print("*****    Welcome to CareAll    *****")

print("New User Enter Option 1")
print("Existing User Enter Option 2")

option = int(input("option: "))

db_connection = mysql.connector.connect(host='localhost', user='root', passwd='480948', database='careall')

# Option 1 will be used to register new user (elders/youngers)
if option == 1:
    data = []
    is_available = True

    # create a CareAll object
    reg_New = CareAll()

    print("Welcome to Register Section")

    name = input("Please enter your name: ")
    age = int(input("Please enter your age: "))

    availability = input("Are you available yes/no? ")
    if availability == 'yes':
        is_available = True
    else:
        is_available = False

    address = input("Please enter your address: ")

    reviews = 0

    # create a data list which will keep the values of all the variables
    data = [name, age, is_available, address, reviews]

    elder_youth = input("Enter either you are elder or youth: ").upper()

    if elder_youth == 'ELDER':
        fund = int(input("Please enter your fund allocation: "))
        data.append(fund)

        reg_New.registerElder(data, db_connection)
    else:
        reg_New.registerYounger(data, db_connection)

# option 2 will be used for existing user.
elif option == 2:
    print("Welcome Existing User")

    print("What you want to do choose from the options: ")
    print("1. Search the available elder person who needs care: ")

    print("2. Rate the Elders: ")

    print("3: Rate the Younger: ")

    print("4: Showing who is taking care of older couple: ")

    print("5: Showing who all a young chap is currently taking care of: ")

    in_operation = int(input("Please choose any options from the above available options: "))

    # create a new object of CareAll for existing user
    user = CareAll()

    if in_operation == 1:
        # 1. Search the available elder person who needs care: 
        print("Please Provide Your Details: ")
        y_name = input("Please enter your name: ")
        y_reg_id = input("Please enter your registration id: ")
        user.searchElder(db_connection, y_name, y_reg_id)

    elif in_operation == 2:
        # 2. Rate the Elders:
        elder_name = input("Please provide the name of elder person: ").strip()
        elder_id = int(input("Please provide the IDs of elder person: ").strip())
        print(
            "Please review the elder person between 5 to 1 as: \n 5 -> Excellent Behaviour \n 4 -> Very Good Behaviour "
            + "\n 3 -> Good Behaviour \n 2 -> Bad Behaviour \n 1 -> Worst Behaviour")
        reviews = int(input("Please rate the elder person ").strip())

        user.rateElder(db_connection, elder_name, elder_id, reviews)

    elif in_operation == 3:
        # 3: Rate the Younger:
        younger_name = input("Please provide the name of younger person: ").strip()
        younger_id = int(input("Please provide the IDs of younger person: ").strip())
        print(
            "Please review the elder person between 5 to 1 as: \n 5 -> Excellent Behaviour \n 4 -> Very Good Behaviour "
            + "\n 3 -> Good Behaviour \n 2 -> Bad Behaviour \n 1 -> Worst Behaviour")
        reviews = int(input("Please rate the younger person ").strip())

        user.rateYoung(db_connection, younger_name, younger_id, reviews)

    elif in_operation == 4:
        # 4: Showing who is taking care of older couple:
        user.taking_care_detail(self, db_connection)
        
    
    elif in_operation == 5:
        #5: Showing who all a young chap is currently taking care of: 
        user.youngChapCarying(self, db_connection)

    else:
        print("Entered option is not available. Please choose from 1,2,3")
