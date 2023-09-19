import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()


db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

try:
    
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    cursor = connection.cursor()

    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS my_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equation VARCHAR(255) NOT NULL,
        result INT NOT NULL
    )
    """
    cursor.execute(create_table_query)

    
    with open("sums.txt", "r") as file:
        lines = file.readlines()

    
    total_sum = 0

    
    for line in lines:
        parts = line.strip().split('=')  
        if len(parts) == 2:
            equation, result = parts[0].strip(), parts[1].strip()
            query = "INSERT INTO my_table (equation, result) VALUES (%s, %s)"
            cursor.execute(query, (equation, result))

            
            total_sum += int(result)

    
    connection.commit()

    
    total_sum_query = "INSERT INTO my_table (equation, result) VALUES (%s, %s)"
    cursor.execute(total_sum_query, ("Total Sum", str(total_sum)))

    
    connection.commit()

    print("Data inserted successfully")
    print(f"Sum of all results: {total_sum}")

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    
    if cursor:
        cursor.close()
    if connection:
        connection.close()
