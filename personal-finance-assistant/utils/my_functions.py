import sqlite3
import pandas as pd
#import re
from datetime import datetime
import streamlit as st
import os


# Get the folder where the current script is (for example: utils/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up to reach the app folder (if script is in utils/)
app_dir = os.path.dirname(script_dir)

# Build path to the DB file inside the app folder
DB_PATH = os.path.join(app_dir, "database", "budget_management.db")  # This line has been added or changed


class MyClass:  # ✅ Make sure this class is at the top level
    
    

    @staticmethod # Due to @staticmethod addition there is no need for 'self' declaration
    def get_db_connection():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
            return conn
        except sqlite3.Error as e:
            print(f"Error while connecting to database: {e}")
            return None
    

    """def load_initial_data(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        all_data_df = pd.read_sql_query("SELECT * FROM MAIN_DATA", conn)
        all_episodes_df = pd.read_sql("SELECT * FROM EPISODES", conn)
        tv_shows_last_watched_df = pd.read_sql("SELECT * FROM TV_SHOWS_LAST_WATCHED", conn)
        

        # Create filtered DataFrames
        all_movies_df = all_data_df[all_data_df["TYPE"] == "Movie"]
        all_tv_shows_df = all_data_df[all_data_df["TYPE"] == "TV Series"]
        movies_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "Movie") ]
        tv_shows_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "TV Series") ]
        tv_shows_active_df = all_data_df[ (all_data_df["STATUS"] == "IN PROGRESS") & (all_data_df["TYPE"] == "TV Series") ]
        
        conn.close()
        
        return all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df, tv_shows_last_watched_df"""
   
    
    def insert_new_record(self
                          ,expense_date: str,
                          expense_type: str,
                          expense_group: str, expense_subgroup: str,
                          expense_place: str = "",
                          expense_detail: str = "",
                          expense_amount: float = 0.0,
                          installment_status: str = "No",
                          installment_count: int = 0,
                          expense_note: str = ""
                          ):
        conn = self.get_db_connection()
        cursor = conn.cursor()


        # Convert expense_amount safely
        if expense_amount in [None, '']:  
            expense_amount = 0.0

        if installment_count in [None, '']:  
            installment_count = 0
        

        # Build the insert query dynamically based on non-empty values
        columns = ["EXPENSE_DATE"]
        values = [expense_date]
        
        if expense_date:
            columns.append("EXPENSE_DATE")
            values.append(expense_date)
        if expense_type:
            columns.append("EXPENSE_TYPE")
            values.append(expense_type)
        if expense_group:
            columns.append("EXPENSE_GROUP")
            values.append(expense_group)
        if expense_subgroup:
            columns.append("EXPENSE_SUBGROUP")
            values.append(expense_subgroup)
        if expense_place:
            columns.append("EXPENSE_PLACE")
            values.append(expense_subgroup)
        if expense_detail:
            columns.append("EXPENSE_DETAIL")
            values.append(expense_detail)
        if expense_note:
            columns.append("EXPENSE_NOTE")
            values.append(expense_note)
        if installment_status:
            columns.append("INSTALLMENT_STATUS")
            values.append(installment_status)
        if installment_count > 0 and installment_status == "Yes":
            columns.append("INSTALLMENT_COUNT")
            values.append(installment_count) #type: ignore
        if float(expense_amount) > 0.0:
            columns.append("EXPENSE_AMOUNT")
            values.append(float(expense_amount)) #type: ignore
        if expense_date:
            columns.append("INSERT_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if expense_date:
            columns.append("MANUAL_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        


        placeholders = ", ".join(["?"] * len(values))  # Generates ?, ?, ?, ?
        #print(placeholders)
        #print(values)
        query = f"INSERT INTO TBL_EXPENSES ({', '.join(columns)}) VALUES ({placeholders})"

        # Execute the insert query
        cursor.execute(query, values)
        conn.commit()

        #st.success("✅ New record inserted successfully!")


        # Insert new record (assuming other required fields have default values)
        #cursor.execute("INSERT INTO MAIN_DATA (IMDB_TT) VALUES (?)", (imdb_tt,))
        #conn.commit()

        # Check if the record inserted and exists in the database now.
        cursor.execute("SELECT MAX(ID) FROM TBL_EXPENSES WHERE 1=1")
        new_record_id = cursor.fetchone()[0]
        #print("new_record_id", new_record_id)

        cursor.close()
        conn.close()

        return new_record_id
    

    # TODO: fetch_lookup_table fonksiyonu herhangi bir yerde kullanılıyor mu?
    def fetch_lookup_table(self, table_name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT ID, NAME FROM {table_name}")
        data = result.fetchall()
        conn.close()
        return data
    
    
    # TODO: insert_into_table fonksiyonu herhangi bir yerde kullanılıyor mu?
    def insert_into_table(self, table_name, name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} (NAME) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    # TODO: update_table_name fonksiyonu herhangi bir yerde kullanılıyor mu?
    def update_table_name(self, table_name, row_id, new_name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET NAME = ? WHERE ID = ?", (new_name, row_id))
        conn.commit()
        conn.close()

    # **************************************************************** MANAGE GROUPS START **************************************************************** #
    def get_expense_groups(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ID, EXPENSE_GROUP FROM TBL_EXPENSE_GROUPS_LKP WHERE IS_ACTIVE = 1")
        data = cur.fetchall()
        conn.close()
        return data

    
    def get_subgroups_by_group_id(self, group_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, EXPENSE_SUBGROUP FROM TBL_EXPENSE_SUBGROUPS_LKP
            WHERE EXPENSE_GROUP_ID = ? AND IS_ACTIVE = 1
        """, (group_id,))
        data = cur.fetchall()
        conn.close()
        return data

    
    def insert_subgroup(self, group_id, name):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO TBL_EXPENSE_SUBGROUPS_LKP (EXPENSE_GROUP_ID, EXPENSE_SUBGROUP)
            VALUES (?, ?)
        """, (group_id, name))
        conn.commit()
        conn.close()

    
    def update_subgroup(self, subgroup_id, new_name):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE TBL_EXPENSE_SUBGROUPS_LKP
            SET EXPENSE_SUBGROUP = ?
            WHERE ID = ?
        """, (new_name, subgroup_id))
        conn.commit()
        conn.close()

    
    def update_group_name(self, group_id, new_name):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE TBL_EXPENSE_GROUPS_LKP
                SET EXPENSE_GROUP = ?
                WHERE ID = ?
            """, (new_name, group_id))
            conn.commit()
            conn.close()
            return True, None  # success
        except sqlite3.IntegrityError:
            return False, "Group name already exists."
        except Exception as e:
            return False, str(e)
        
    
    def soft_delete_group(self, group_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        # Soft delete the group
        cur.execute("UPDATE TBL_EXPENSE_GROUPS_LKP SET IS_ACTIVE = 0 WHERE ID = ?", (group_id,))
        # Optionally also soft delete its subgroups
        cur.execute("UPDATE TBL_EXPENSE_SUBGROUPS_LKP SET IS_ACTIVE = 0 WHERE EXPENSE_GROUP_ID = ?", (group_id,))
        conn.commit()
        conn.close()


    def restore_group(self, group_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE TBL_EXPENSE_GROUPS_LKP SET IS_ACTIVE = 1 WHERE ID = ?", (group_id,))
        # Optionally: restore its subgroups too
        cur.execute("UPDATE TBL_EXPENSE_SUBGROUPS_LKP SET IS_ACTIVE = 1 WHERE EXPENSE_GROUP_ID = ?", (group_id,))
        conn.commit()
        conn.close()


    def get_deleted_groups(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, EXPENSE_GROUP FROM TBL_EXPENSE_GROUPS_LKP
            WHERE IS_ACTIVE = 0
            ORDER BY EXPENSE_GROUP
        """)
        data = cur.fetchall()
        conn.close()
        return data
    
    # **************************************************************** MANAGE GROUPS END **************************************************************** #



    # **************************************************************** MANAGE TYPES START **************************************************************** #


    def get_expense_types(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ID, TYPE_DESC FROM TBL_EXPENSE_TYPES_LKP WHERE IS_ACTIVE = 1")
        data = cur.fetchall()
        conn.close()
        return data
    
    def update_type_name(self, type_id, new_name):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE TBL_EXPENSE_TYPES_LKP
                SET TYPE_DESC = ?
                WHERE ID = ?
            """, (new_name, type_id))
            conn.commit()
            conn.close()
            return True, None  # success
        except sqlite3.IntegrityError:
            return False, "Type name already exists."
        except Exception as e:
            return False, str(e)
        

    def soft_delete_type(self, type_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        # Soft delete the group
        cur.execute("UPDATE TBL_EXPENSE_TYPES_LKP SET IS_ACTIVE = 0 WHERE ID = ?", (type_id,))
        conn.commit()
        conn.close()
    
    def get_deleted_types(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, TYPE_DESC FROM TBL_EXPENSE_TYPES_LKP
            WHERE IS_ACTIVE = 0
            ORDER BY TYPE_DESC
        """)
        data = cur.fetchall()
        conn.close()
        return data


    def restore_type(self, type_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE TBL_EXPENSE_TYPES_LKP SET IS_ACTIVE = 1 WHERE ID = ?", (type_id,))
        conn.commit()
        conn.close()

    
    # **************************************************************** MANAGE TYPES END **************************************************************** #


    # **************************************************************** MANAGE BANKS START **************************************************************** #


    """def get_banks(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ID, BANK_NAME FROM TBL_BANKS_LKP WHERE IS_ACTIVE = 1")
        data = cur.fetchall()
        conn.close()
        return data"""
    

    def get_banks(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        result = cursor.execute("SELECT ID, BANK_NAME, DETAIL_NAME, BANK_TYPE FROM TBL_BANKS_LKP WHERE IS_ACTIVE = 1")
        banks = result.fetchall()
        conn.close()
        return banks  # list of tuples

    
    def update_bank_name(self, bank_id, new_name):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE TBL_BANKS_LKP
                SET BANK_NAME = ?
                WHERE ID = ?
            """, (new_name, bank_id))
            conn.commit()
            conn.close()
            return True, None  # success
        except sqlite3.IntegrityError:
            return False, "Bank name already exists."
        except Exception as e:
            return False, str(e)
        

    def soft_delete_bank(self, bank_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE TBL_BANKS_LKP SET IS_ACTIVE = 0 WHERE ID = ?", (bank_id,))
        conn.commit()
        conn.close()
    
    def get_deleted_banks(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, BANK_NAME FROM TBL_BANKS_LKP
            WHERE IS_ACTIVE = 0
            ORDER BY BANK_NAME
        """)
        data = cur.fetchall()
        conn.close()
        return data


    def restore_bank(self, bank_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE TBL_BANKS_LKP SET IS_ACTIVE = 1 WHERE ID = ?", (bank_id,))
        conn.commit()
        conn.close()


    def get_bank_detail_by_id(self, bank_id):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT BANK_NAME, DETAIL_NAME, BANK_TYPE
            FROM TBL_BANKS_LKP
            WHERE ID = ?
        """, (bank_id,))
        row = cur.fetchone()
        conn.close()
        return {
            "BANK_NAME": row[0],
            "DETAIL_NAME": row[1],
            "BANK_TYPE": row[2]
        } if row else {}
    

    def update_bank_full(self, bank_id, new_name, new_detail, new_type):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE TBL_BANKS_LKP
                SET BANK_NAME = ?, DETAIL_NAME = ?, BANK_TYPE = ?
                WHERE ID = ?
            """, (new_name, new_detail, new_type, bank_id))
            conn.commit()
            conn.close()
            return True, None
        except sqlite3.IntegrityError:
            return False, "Bank name already exists."
        except Exception as e:
            return False, str(e)
    

    def get_bank_details_by_type(self, bank_type):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, BANK_NAME, DETAIL_NAME
            FROM TBL_BANKS_LKP
            WHERE IS_ACTIVE = 1 AND BANK_TYPE = ?
            ORDER BY BANK_NAME, DETAIL_NAME
        """, (bank_type,))
        results = cur.fetchall()
        conn.close()
        return results




    # **************************************************************** MANAGE BANKS END **************************************************************** #



    def insert_expense(self, expense_date, expense_type, expense_group, expense_subgroup,
                    expense_place, expense_detail, expense_amount,
                    installment_status, installment_count, no_of_installment,
                    bank_id, expense_note):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO TBL_EXPENSES (
                    EXPENSE_DATE, EXPENSE_TYPE, EXPENSE_GROUP, EXPENSE_SUBGROUP,
                    EXPENSE_PLACE, EXPENSE_DETAIL, EXPENSE_AMOUNT,
                    INSTALLMENT_STATUS, INSTALLMENT_COUNT, NO_OF_INSTALLMENT,
                    BANK_ID, EXPENSE_NOTE
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                expense_date, expense_type, expense_group, expense_subgroup,
                expense_place, expense_detail, expense_amount,
                installment_status, installment_count, no_of_installment,
                bank_id, expense_note
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Insert error:", e)
            return False
