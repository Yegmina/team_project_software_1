import database_manager as db
game_name = 'Noah4'

game_id = db.run(f"SELECT id FROM saved_games WHERE input_name = '{game_name}';")[0][0]

icao_code_list = db.run(f'SELECT airport_id '
                        f'FROM airport_info '
                        f'WHERE game_id = "{game_id}";')

for i in range(0, len(icao_code_list)):
       print(icao_code_list[i][0])


print(game_id)
