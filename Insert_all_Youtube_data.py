import pyodbc
import pandas as pd

print('Insert data from csv files to MSSQL tables')
print()

server = "<SERVER>"
database = "<DATABASE>"
schema = '<SCHEMA>'
username = '<USERNAME>'
password = '<PASSWORD>'

def connect_to_mssql():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'UID=' + username + ';'
        'PWD=' + password + ';'
    )
    print('Connecting to MSSQL...')
    return conn

def insert_csv_data(conn, table, csv_file):
    cursor = conn.cursor()
    df = pd.read_csv(csv_file, sep=',')
    df.fillna(0, inplace=True)
    columns = ', '.join(df.columns)
    placeholders = ', '.join('?' * len(df.columns))
    sql_query = f"INSERT INTO {schema}.{table} ({columns}) VALUES ({placeholders})"
    print(f'Inserting data from {csv_file} into {table}...')
    total_rows = len(df)
    inserted_rows = 0
    for i, row in enumerate(df.itertuples(index=False), 1):
        cursor.execute(sql_query, row)
        inserted_rows += 1
        print(f"{inserted_rows}/{total_rows}")
    print(f"Insertion into {table} complete!")
    cursor.close()

def close_connection(conn):
    conn.commit()
    conn.close()
    print('MSSQL connection closed')

# Connect to MSSQL
conn = connect_to_mssql()

# Insert data from CSV files into tables
table1 = "CHANNEL_INFORMATION"
csv_file1 = r"channel_information.csv"
insert_csv_data(conn, table1, csv_file1)

table2 = "PLAYLISTS_INFORMATION"
csv_file2 = r"playlists_information.csv"
insert_csv_data(conn, table2, csv_file2)

table3 = "VIDEOS_INFORMATION"
csv_file3 = r"videos_information.csv"
insert_csv_data(conn, table3, csv_file3)

# Close the connection
close_connection(conn)