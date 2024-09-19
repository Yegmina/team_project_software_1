import database_manager as db
answer = db.run("select name from country")
print(answer)