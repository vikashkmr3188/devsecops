import json
import psycopg2
from psycopg2 import sql, Error
import logging
from datetime import datetime

# Load JSON data
with open('ransomware_overview.json') as file:
    data = json.load(file)

# Initialize tracking variables
total_records = len(data)
inserted_records = 0
duplicate_records = 0
missed_records = 0
missed_rows = []

# Setup logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"log_{timestamp}.txt"
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Database connection
try:
    conn = psycopg2.connect(
        dbname="devsecops1",
        user="dev_user1",
        password="devsecops123$",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    logging.info("Database connection established successfully.")
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")
    raise

# Create tables
try:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ransomware (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS ransomware_details (
        id SERIAL PRIMARY KEY,
        ransomware_id INTEGER REFERENCES ransomware(id),
        extensions TEXT,
        extension_pattern TEXT,
        ransom_note_filenames TEXT,
        comment TEXT,
        encryption_algorithm TEXT,
        decryptor TEXT,
        resources TEXT[],
        screenshots TEXT,
        microsoft_detection_name TEXT,
        microsoft_info TEXT,
        sandbox TEXT,
        iocs TEXT,
        snort TEXT,
        UNIQUE (ransomware_id, extensions, extension_pattern, ransom_note_filenames,
                comment, encryption_algorithm, decryptor, resources, screenshots,
                microsoft_detection_name, microsoft_info, sandbox, iocs, snort)
    );
    ''')
    conn.commit()
    logging.info("Tables created successfully.")
except Error as e:
    logging.error(f"Error creating tables: {e}")
    conn.rollback()
    raise

# Function to insert data
def insert_data(data):
    global inserted_records, duplicate_records, missed_records
    for entry in data:
        # Insert into ransomware table
        names = entry['name']
        ransomware_id = None
        for name in names:
            try:
                cur.execute(
                    sql.SQL("INSERT INTO ransomware (name) VALUES (%s) RETURNING id;"),
                    [name]
                )
                ransomware_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f"Inserted ransomware name: {name}")
            except psycopg2.IntegrityError:
                conn.rollback()
                cur.execute(
                    sql.SQL("SELECT id FROM ransomware WHERE name = %s;"),
                    [name]
                )
                ransomware_id = cur.fetchone()[0]
                logging.info(f"Ransomware name already exists, using existing ID: {name}")

            # Insert into ransomware_details table
            try:
                cur.execute(
                    sql.SQL('''
                        INSERT INTO ransomware_details (
                            ransomware_id, extensions, extension_pattern, ransom_note_filenames,
                            comment, encryption_algorithm, decryptor, resources, screenshots,
                            microsoft_detection_name, microsoft_info, sandbox, iocs, snort
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (ransomware_id, extensions, extension_pattern, ransom_note_filenames,
                                    comment, encryption_algorithm, decryptor, resources, screenshots,
                                    microsoft_detection_name, microsoft_info, sandbox, iocs, snort)
                        DO NOTHING;
                    '''),
                    [
                        ransomware_id,
                        entry.get('extensions', None),
                        entry.get('extensionPattern', None),
                        entry.get('ransomNoteFilenames', None)[:255] if entry.get('ransomNoteFilenames', None) else None,  # Ensure it fits in VARCHAR(255)
                        entry.get('comment', None),
                        entry.get('encryptionAlgorithm', None),
                        entry.get('decryptor', None),
                        entry.get('resources', []),
                        entry.get('screenshots', None),
                        entry.get('microsoftDetectionName', None),
                        entry.get('microsoftInfo', None),
                        entry.get('sandbox', None),
                        entry.get('iocs', None),
                        entry.get('snort', None)
                    ]
                )
                if cur.rowcount == 0:
                    duplicate_records += 1
                    missed_rows.append({**entry, "missing_reason": "Duplicate"})
                    logging.info(f"Duplicate record detected and skipped: {entry}")
                else:
                    inserted_records += 1
                    logging.info(f"Inserted ransomware details for ransomware_id: {ransomware_id}")
                conn.commit()
            except Error as e:
                conn.rollback()
                missed_records += 1
                missed_rows.append({**entry, "missing_reason": str(e)})
                logging.error(f"Error inserting ransomware_details for ransomware_id {ransomware_id}: {e}")
                logging.error(f"Entry causing the issue: {entry}")

# Insert data
insert_data(data)

# Close connection
cur.close()
conn.close()

# Write missed rows to JSON file
with open('missed_rows.json', 'w') as missed_file:
    json.dump(missed_rows, missed_file, indent=4)

# Output the summary
print(f"Total records in json: {total_records}")
print(f"Inserted records from json: {inserted_records}")
print(f"Duplicate records from json: {duplicate_records}")
print(f"Missed records from json: {missed_records}")
print("Please check missed_rows.json to check missed rows details")
print(f"Please check {log_filename} for more details")
