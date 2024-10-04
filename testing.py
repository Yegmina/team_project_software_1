import database_manager as db
db.run(f"UPDATE saved_games"
       f"SET money = 900000,"
       f"WHERE input_name = '123';")