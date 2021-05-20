import psycopg2

connection = psycopg2.connect(user="postgres",
                                password="nguyentienduong1",
                                host="localhost",
                                port="5432",
                                database="nhom12")

    # Create a cursor to perform database operations
cursor = connection.cursor()

