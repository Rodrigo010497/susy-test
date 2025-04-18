import pymysql
import os
from datetime import datetime
#house class
class House:
    #Attributes
    def __init__(self,A,B,C,D,E,F,G,H):
        self.energy_usage = A
        self.months = list(A.keys())
        self.potential_energy_generation = B
        self.potential_energy_usage = C
        self.effective_energy_generation = D
        self.energy_generation_prediction_error = E
        self.potential_savings_on_improvements = F
        self.effective_savings_on_improvements = G
        self.co2_saved = H
        self.savings_on_project_improvements_prediction_error = { date: (F[date] - G[date]) for date in self.months }
        self.potential_scores_per_month = {date: self.calculate_potential_score(date) for date in self.months}
        self.effective_scores_per_month = {date: self.calculate_effective_score(date) for date in self.months}

    #calculate potential score
    def calculate_potential_score(self, date):
        score = ( (self.potential_energy_generation[date] + self.potential_savings_on_improvements[date]) - self.energy_usage[date] )
        print(date,"potential score",score)
        return score
    
    #calculate effective score
    def calculate_effective_score(self, date):
        score = ( (self.effective_energy_generation[date] + self.effective_energy_generation[date]) - self.energy_usage[date])
        print(date,"effective score",score)
        return score

    #save potential score to database
    def save_potential_score(self, conn, cursor, date):
        cursor.execute(f"UPDATE houses SET potential_score = {self.potential_scores_per_month[date]} WHERE date = '{date}';")
        conn.commit()

    #save effective score to database
    def save_effective_score(self, conn, cursor, date):
        cursor.execute(f"UPDATE houses SET effective_score = {self.effective_scores_per_month[date]} WHERE date = '{date}';")
        conn.commit()

    #save all potential scores for dates
    def save_all_potential_scores(self, conn, cursor):
        for date in list(self.potential_scores_per_month.keys()):
            self.save_potential_score(conn, cursor, date)

    #save all effective scores for dates
    def save_all_effective_scores(self, conn, cursor):
        for date in list(self.effective_scores_per_month.keys()):
            self.save_effective_score(conn, cursor, date)

#Connect to database 
def conenct_to_db():
    # Connection to MySQL database
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),        
        user=os.getenv("DB_USER"),        
        password=os.getenv("DB_PASSWORD"), 
        database=os.getenv("DB_NAME"),      
        port=int(os.getenv("DB_PORT"))
    )

    # Cursor object to interact with the db
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cursor 

#close db connection
def close_db_connection(conn, cursor):
        cursor.close()
        conn.close()

#I could have done this inside the class but I didn't to ensure loose coupling     
# Get house data per month from db
def get_houses_data_from_db(cursor, first_month_date, last_month_date):
    cursor.execute(f"SELECT * FROM houses WHERE date BETWEEN '{first_month_date}' AND '{last_month_date}'")  #Adjust table name as needed
    rows = cursor.fetchall()
    variables_names = ["A","B","C","D","E","F","G","H"]
    #organize data by variable per date
    data_per_month = { name: { str(row["date"]) : row[name] for row in rows } for name in variables_names }

    return data_per_month 

os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_USER"] = "root"
os.environ["DB_PASSWORD"] = "123"
os.environ["DB_NAME"] = "db"
os.environ["DB_PORT"] = "3306"
conn, cursor = conenct_to_db()
data = get_houses_data_from_db(cursor, "2023-04-01", "2023-06-30")
house = House(**data)
house.save_potential_score(conn, cursor, "2023-04-01")
house.save_effective_score(conn, cursor, "2023-04-01")
house.save_all_potential_scores(conn, cursor)
house.save_all_effective_scores(conn, cursor)
close_db_connection(conn, cursor)




