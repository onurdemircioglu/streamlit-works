import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import my_functions

obj = my_functions.MyClass()

def create_database_objects():
    conn = obj.get_db_connection()
    cursor = conn.cursor()

    # Create TBL_EXPENSES table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_EXPENSES (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EXPENSE_DATE TEXT,
            EXPENSE_TYPE INTEGER,
            EXPENSE_GROUP INTEGER,
            EXPENSE_SUBGROUP INTEGER,
            EXPENSE_PLACE TEXT,
            EXPENSE_DETAIL TEXT,
            EXPENSE_AMOUNT REAL,
            INSTALLMENT_STATUS TEXT,
            INSTALLMENT_COUNT INTEGER,
            NO_OF_INSTALLMENT TEXT,
            BANK_ID INTEGER,
            EXPENSE_NOTE TEXT,
            INSERT_DATE TEXT DEFAULT (DATE('now')),
            MANUAL_UPDATE_DATE TEXT DEFAULT (DATE('now')),
            IS_ACTIVE INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    # --CARD_NUMBER TEXT,


    # Create TBL_INCOMES_TYPES_LKP table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_INCOME_TYPES_LKP (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TYPE_NAME TEXT UNIQUE NOT NULL,
            IS_ACTIVE INTEGER DEFAULT 1
        )
    """)
    conn.commit()


    # Create TBL_INCOMES table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_INCOMES (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            INCOME_DATE TEXT NOT NULL,
            INCOME_TYPE_ID INTEGER NOT NULL,
            INCOME_AMOUNT REAL NOT NULL,
            INCOME_SOURCE TEXT,
            NOTE TEXT,
            IS_ACTIVE INTEGER DEFAULT 1,
            INSERT_DATE TEXT DEFAULT (DATE('now')),
            UPDATE_DATE TEXT DEFAULT (DATE('now')),
            FOREIGN KEY (INCOME_TYPE_ID) REFERENCES TBL_INCOME_TYPES_LKP(ID)
        )
    """)
    conn.commit()


    # Create TBL_EXPENSE_GROUPS_LKP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_EXPENSE_GROUPS_LKP (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EXPENSE_GROUP TEXT UNIQUE NOT NULL,
            IS_ACTIVE INTEGER DEFAULT 1
        )
    """)


    # Create TBL_EXPENSE_GROUPS_LKP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_EXPENSE_SUBGROUPS_LKP (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EXPENSE_GROUP_ID INTEGER,
            EXPENSE_SUBGROUP TEXT,
            IS_ACTIVE INTEGER DEFAULT 1,
            UNIQUE(EXPENSE_GROUP_ID, EXPENSE_SUBGROUP)
        )
    """)


    # Create TBL_EXPENSE_TYPES_LKP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_EXPENSE_TYPES_LKP (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TYPE_DESC TEXT UNIQUE NOT NULL,
            IS_ACTIVE INTEGER DEFAULT 1
        )
    """)


    # Create TBL_BANKS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_BANKS_LKP (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BANK_NAME TEXT,
            DETAIL_NAME TEXT,             -- e.g., "Ziraat Visa Card" or "Salary Account"
            BANK_TYPE TEXT,               -- This is your "associated expense type"
            IS_ACTIVE INTEGER DEFAULT 1,
            UNIQUE(BANK_NAME, DETAIL_NAME)
                   
        )
    """)


    # Create TBL_REMINDERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_REMINDERS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            REMINDER_DATE TEXT,
            REMINDER_NAME TEXT,
            REMINDER_DETAIL TEXT,
            REMINDER_CATEGORY TEXT,  -- e.g., "Utility", "Loan", "Subscription"
            RECURRENCE_TYPE TEXT,       -- 'none', 'monthly', 'yearly', 'weekly'
            RECURRENCE_INTERVAL INTEGER, -- e.g., every 1 month, every 2 weeks
            IS_ACTIVE INTEGER DEFAULT 1,
            IS_DONE INTEGER DEFAULT 0,
            DONE_DATE TEXT,
            CREATED_AT TEXT DEFAULT (DATE('now')),
            UPDATED_AT TEXT
        )
    """)


    # Create REPORTABLE_EXPSENSES VIEW
    cursor.execute("DROP VIEW IF EXISTS REPORTABLE_EXPENSES")


    # Create TBL_BANKS
    cursor.execute("""
        CREATE VIEW REPORTABLE_EXPENSES AS
        SELECT A.ID,
                A.EXPENSE_DATE, SUBSTR(A.EXPENSE_DATE, 1, 4) AS EXPENSE_YEAR, SUBSTR(A.EXPENSE_DATE, 1, 7) AS EXPENSE_PERIOD, SUBSTR(A.EXPENSE_DATE, 6, 2) AS EXPENSE_MONTH,
                B.EXPENSE_GROUP, C.EXPENSE_SUBGROUP, EXPENSE_PLACE, EXPENSE_DETAIL, EXPENSE_AMOUNT,
        INSTALLMENT_STATUS, INSTALLMENT_COUNT, NO_OF_INSTALLMENT, D.BANK_NAME, D.DETAIL_NAME, EXPENSE_NOTE,
        CASE WHEN A.EXPENSE_DATE > DATE() THEN 1 ELSE 0 END AS FUTURE_EXPENSE
        FROM TBL_EXPENSES A 

        LEFT JOIN TBL_EXPENSE_GROUPS_LKP B
        ON A.EXPENSE_GROUP = B.ID

        LEFT JOIN TBL_EXPENSE_SUBGROUPS_LKP C
        ON A.EXPENSE_SUBGROUP = C.ID

        LEFT JOIN TBL_BANKS_LKP D
        ON A.BANK_ID = D.ID
                   
    """)
    

    # Close connection on exit
    conn.close()


create_database_objects()