import mysql.connector

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'flight_game',
    autocommit = True,
    collation = 'utf8mb4_general_ci'
)
cursor = connection.cursor()

cursor.execute("Select * from country where iso_country = 'FI'")
answer = cursor.fetchall()
print(answer)