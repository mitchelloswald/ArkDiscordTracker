import sqlite3


enemylist = []

#create DB
def create_table():
    connection = sqlite3.connect('enemys.db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS enemys (name text , isFriend bool)")

#add enemy from db
def add_enemy(name):
    
    #Connect To DB
    connection = sqlite3.connect('enemys.db')
    cursor = connection.cursor()

    enemyName = name
    friend = False
    #Add Enemy To DBx 
    cursor.execute("INSERT INTO enemys (name , isFriend) VALUES(? , ?)", (enemyName , friend))
    connection.commit()

#remove enemy from db
def remove_enemy(enemy):
    #Connect To DB
    connection = sqlite3.connect('enemys.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM enemys WHERE Name=?", (enemy,))
    connection.commit()


#return a list of watched enemys
def enemy_list():
   
    #Connect To DB
    connection = sqlite3.connect('enemys.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT name FROM enemys')
    enemylist = cursor.fetchall()
    return enemylist


    

