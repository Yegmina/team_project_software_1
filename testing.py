#design game over
print("         / ____|                       / __ \                ")
print("        | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ")
print("        | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|")
print("        | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   ")
print("         \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   ")

import mariadb
import database_initializing as db

connection = mariadb.connect(
    host = 'localhost',
    user = 'root',
    database = 'flight_game',
    password = 'root',
    autocommit = True,
)

## db.run( query )
ans = db.run(
    "select name from airport")
hus = db.run(" select name from country where name = 'HU'")
print(hus)


