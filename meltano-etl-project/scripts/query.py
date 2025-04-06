import psycopg2
import csv

connection = psycopg2.connect(host='localhost', database='processed_data', user='user', password='password', port='5433')
cursor = connection.cursor()

cursor.execute("SELECT * FROM order_details od JOIN orders o ON o.order_id = od.order_id;")
results = cursor.fetchall()

column_names = [desc[0] for desc in cursor.description]

with open('query/final_orders.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(column_names)
    csv_writer.writerows(results)

cursor.close()
connection.close()