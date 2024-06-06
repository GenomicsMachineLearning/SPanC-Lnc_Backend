import sqlite3
import csv
import zipfile

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Open the zipped file and read the CSV file inside it
with zipfile.ZipFile('assets/annotation_table.zip') as zip_file:
    with zip_file.open('annotation_table.csv') as csv_file:
        csv_reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
        header = next(csv_reader)
        rows = []
        for row in csv_reader:
            row_dict = {header[i]: row[i] for i in range(len(header))}
            rows.append(row_dict)
            cursor.execute('INSERT INTO genes VALUES (' +
                           '?, ?, ?, ?, ?, ' +
                           '?, ?, ?, ?, ?, ' +
                           '?, ?, ?, ?, ?,' +
                           '?, ?, ?, ?, ?,' +
                           '?, ?)',
                           [row_dict[col] for col in header[:22]])

# Commit the changes and close the connection
conn.commit()
conn.close()
