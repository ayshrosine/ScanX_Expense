import sqlite3

DB_NAME = "ocr_master.db"
con = None

try:
    #establishing connection
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    #creating table: 
    #creating table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ocr_line_items ( 
            Invoice_No TEXT NOT NULL,
            line_item_id INTEGER NOT NULL,
            Issue_Date TEXT,
            billed_to TEXT,
            billed_by TEXT,
            Description TEXT,
            Category TEXT,
            Amount REAL,
            Grand_Total REAL,
            source_file TEXT, -- column name case for consistency
            PRIMARY KEY (Invoice_No, line_item_id)
        )
        """ )
    #closing the connection
    con.commit()
    print(f"table succeffully created")

except sqlite3.Error as e:
    print(f"error is {e}")


finally:
    if con:
        con.close()