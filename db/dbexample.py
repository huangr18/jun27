import psycopg2

# Establish connection
connection = psycopg2.connect(
    host="localhost",
    port="9001",
    database="test",
    user="test",
    password="test"
)

# Create a cursor
cursor = connection.cursor()

# Execute CREATE TABLE statement
create_table_query = '''
CREATE TABLE if not exists test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INTEGER
)
'''
cursor.execute(create_table_query)

# Insert data into the table
insert_data_query = '''
INSERT INTO test_table (name, age) VALUES (%s, %s)
'''
data = [('John', 25), ('Alice', 30), ('Bob', 35)]  # Example data
cursor.executemany(insert_data_query, data)

# Commit the changes
connection.commit()


# Execute SQL queries
cursor.execute("SELECT * FROM test_table")
result = cursor.fetchall()

# Print the query result
for row in result:
    print(row)

# Commit and close the connection
connection.commit()
connection.close()