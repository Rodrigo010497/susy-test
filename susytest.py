import pymysql
import os
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
        self.savings_on_project_improvements_prediction_error = { month: (F[month] - G[month]) for month in months }
        self.potential_score = self.__calculate_potential_score()
        self.effective_score = self.__calculate_effective_score()


    #calculate potential score
    def __calculate_potential_score(self):
        return ( (self.potential_energy_generation + self.potential_savings_on_improvements) - self.energy_usage)
    
    #calculate effective score
    def __calculate_effective_score(self):
        return ( (self.effective_energy_generation + self.effective_energy_generation) - self.energy_usage)
    @property
    #get potential score
    def potential_score(self):
        self.potential_score = 0
        return self.potential_score
    @property
    #get effective score
    def effective_score(self): 
        return self.effective_score
    

    #save potential score to database
    def save_potential_score(self, cursor, conn):
        cursor.execute(f"INSERT INTO houses (potential_score) VALUES {self.potential_score}")
        conn.commit()  # Commit the transaction

    #save effective score to database
    def save_effective_score(self): 
        return 0 

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
    variables_names = ["A","B","C","D","E","F","G"]
    data_per_month = { name: { str(row["date"]) : row[name] for row in rows } for name in variables_names }

    # Print the data from the table
    for row in rows:
        print(row)

    return data_per_month 


    # Step 2: Writing (Inserting) Data into an Existing Table
    cursor.execute('''
        INSERT INTO users (name, age) 
        VALUES (%s, %s)
    ''', ('John Doe', 35))  # The %s are placeholders for the actual values
    conn.commit()  # Commit the transaction

    # print("Data inserted successfully!")

    




os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_USER"] = "root"
os.environ["DB_PASSWORD"] = "123"
os.environ["DB_NAME"] = "db"
os.environ["DB_PORT"] = "3306"
conn, cursor = conenct_to_db()
data = get_houses_data_from_db(cursor, "2023-04-01", "2023-06-30")
house = House(**data)




