import database_manager as db
import noah as nh

count = db.run(f"SELECT COUNT(*) FROM airport_info "
               f"LEFT JOIN airport ON airport.ident = airport_id "
               f"WHERE continent = 'SA' "
               f"AND infected = 0 "
               f"AND closed = 0 "
               f"AND game_id = 90;")[0][0]
nh.print_all_icao_codes(90, 'EU')
print(count)
