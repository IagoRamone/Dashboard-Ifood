import os
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'), 
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_user(nome, email, telefone, usuario, senha):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO dashcad (nome, email, telefone, usuario, senha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nome, email, telefone, usuario, senha))
            connection.commit()
            cursor.close()
            print("User registered successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()
    else:
        print("Failed to create connection to the database.")
