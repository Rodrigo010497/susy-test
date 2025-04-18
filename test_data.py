import pymysql
import random
from datetime import date, timedelta

# --- Connect to the database ---
def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123',
        database='db',
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Generate a row of data based on a scenario ---
def generate_row(base_date):
    scenario = random.choice([1, 2, 3])

    if scenario == 1:
        # Scenario 1: Usage > Potential > Production
        A = random.uniform(800, 1000)
        B = random.uniform(500, 700)
        D = random.uniform(400, B)
        H = round(random.uniform(2.0, 3.0), 2)
    elif scenario == 2:
        # Scenario 2: Potential > Usage > Production
        B = random.uniform(900, 1100)
        A = random.uniform(700, 850)
        D = random.uniform(600, A)
        H = round(random.uniform(1.0, 2.0), 2)
    else:
        # Scenario 3: Potential > Production > Usage
        A = random.uniform(400, 600)
        B = random.uniform(1000, 1200)
        D = random.uniform(A + 50, B)
        H = round(random.uniform(-1.0, 0.0), 2)

    C = round(B - A, 2)
    E = round(B - D, 2)
    F = round(random.uniform(100, 300), 2)
    G = round(random.uniform(80, F), 2)

    return (base_date.isoformat(), A, B, C, D, E, F, G, H)

# --- Insert data into the database ---
def insert_generated_data():
    conn = connect_to_db()
    cursor = conn.cursor()

    start_date = date(2024, 1, 1)
    for i in range(100):
        current_date = start_date + timedelta(days=i)
        row = generate_row(current_date)

        insert_query = """
            INSERT INTO houses (date, A, B, C, D, E, F, G, H)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, row)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 100 rows inserted.")

# --- Run it ---
insert_generated_data()
