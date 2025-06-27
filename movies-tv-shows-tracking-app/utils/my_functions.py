import sqlite3
import pandas as pd
import re
from datetime import datetime
import streamlit as st
import os

# Database Path
# Get the path of the current directory (utils folder)
current_directory = os.path.dirname(__file__)
# Go one directory up to the root folder
DB_PATH = os.path.join(current_directory, "..", "movies_tv_shows.db")

class MyClass:  # ✅ Make sure this class is at the top level

    @staticmethod
    def check_imdb_title(imdb_url: str) -> str:
        if "/title/tt" in imdb_url:
            return 1
        else:
            return 0

    @staticmethod # Due to @staticmethod addition there is no need for 'self' declaration
    def imdb_converter(imdb_url: str, in_out: str) -> str:
        if in_out == "in":
            match = re.search(r'tt\d+', imdb_url)
            return match.group() if match else None
        elif in_out == "out":
            return "https://www.imdb.com/title/" + imdb_url + "/"
        else:
            return "Error"
    

    @staticmethod
    def beyazperde_converter(beyazperde_url: str, in_out: str) -> str:
        if in_out == "in":
            beyazperde_result = beyazperde_url.replace("https://www.beyazperde.com/","")
        elif in_out == "out":
            beyazperde_result = "https://www.beyazperde.com/" + beyazperde_url
        else:
            beyazperde_result = "Error"
        
        return beyazperde_result
    

    @staticmethod # Due to @staticmethod addition there is no need for 'self' declaration
    def get_db_connection():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
            return conn
        except sqlite3.Error as e:
            print(f"Error while connecting to database: {e}")
            return None
    

    def load_initial_data(self):
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
        
        return all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df, tv_shows_last_watched_df
    

    def check_existing_record(self, imdb_tt: str):  # ✅ Added 'self'
        conn = self.get_db_connection()
        cursor = conn.cursor()
        #cursor.execute("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", (imdb_tt,))
        data_exist = pd.read_sql_query("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", conn, params=(imdb_tt,))

        if not data_exist.empty:  # ✅ Corrected check
            #return data_exist.iloc[0, 0]  # ✅ Use iloc[0, 0] instead of data_exist[0]
            return 1

        conn.close()
        #return None
        return 0
   
    
    def insert_new_record(self
                          ,imdb_tt: str, record_type: str, record_title_type: str
                          ,original_title: str = None, primary_title: str = None
                          ,record_status: str = None, release_year: int = None
                          ,record_score: int = None, score_date: str = None
                          ,imdb_rating: float = None
                          ,imdb_rating_count: int = None
                          # : int = Nones
                          ,imdb_genres: str = None
                          ,watch_grade: int = None
                          ):
        conn = self.get_db_connection()
        cursor = conn.cursor()


        # Convert imdb_rating safely
        if imdb_rating in [None, '']:  
            imdb_rating = 0.0
        
        # Convert imdb_rating_count safely
        if imdb_rating_count in [None, '']:  # Check if it's None or an empty string
            imdb_rating_count = 0  # Set a default value

        # Convert release_year safely
        if release_year in [None, '']:  # Check if it's None or an empty string
            release_year = 0  # Set a default value



        # Build the insert query dynamically based on non-empty values
        columns = ["IMDB_TT"]
        values = [imdb_tt]
        
        if original_title:
            columns.append("ORIGINAL_TITLE")
            values.append(original_title)
        if primary_title:
            columns.append("PRIMARY_TITLE")
            values.append(primary_title)
        if record_type:
            columns.append("TYPE")
            values.append(record_type)
        if record_title_type:
            columns.append("TITLE_TYPE")
            values.append(record_title_type)
        if record_status:
            #TODO: buraya >0 kriteri koymak lazım ama nasıl etkileyecek emin olamadığım için şu an dokunmadım ya da min value = 5 kriteri de ekleyebiliriz.
            columns.append("STATUS")
            values.append(record_status)
        if release_year:
            columns.append("RELEASE_YEAR")
            values.append(release_year)
        if record_status == "WATCHED" and record_score > 0:
            columns.append("SCORE")
            values.append(record_score)
        if record_status == "WATCHED" and score_date:
            columns.append("SCORE_DATE")
            values.append(score_date)
        if float(imdb_rating) > 0.0:
            columns.append("RATING")
            values.append(imdb_rating)
        if float(imdb_rating) > 0.0:
            columns.append("RATING_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if imdb_rating_count > 0:
            columns.append("RATING_COUNT")
            values.append(imdb_rating_count)
        if imdb_genres:
            columns.append("GENRES")
            values.append(imdb_genres)
        if imdb_genres:
            columns.append("GENRES_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if (record_status == "TO BE WATCHED" or record_status == "MAYBE") and watch_grade > 0:
            columns.append("WATCH_GRADE") # TODO:Watched olarak işaretlediklerimizde bu alanı sıfırlamalıyız bence
            values.append(watch_grade)
        if imdb_tt:
            columns.append("INSERT_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if imdb_tt:
            columns.append("MANUAL_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        


        placeholders = ", ".join(["?"] * len(values))  # Generates ?, ?, ?, ?
        #print(placeholders)
        #print(values)
        query = f"INSERT INTO MAIN_DATA ({', '.join(columns)}) VALUES ({placeholders})"

        # Execute the insert query
        cursor.execute(query, values)
        conn.commit()

        #st.success("✅ New record inserted successfully!")


        # Insert new record (assuming other required fields have default values)
        #cursor.execute("INSERT INTO MAIN_DATA (IMDB_TT) VALUES (?)", (imdb_tt,))
        #conn.commit()

        # Check if the record inserted and exists in the database now.
        cursor.execute("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", (imdb_tt,))
        new_record_id = cursor.fetchone()[0]
        #print("new_record_id", new_record_id)

        cursor.close()
        conn.close()

        return new_record_id
    

    # Fetch In-Progress TV Shows from Database View
    def fetch_tv_shows(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID, TITLE FROM TV_SHOWS_TRACKING") # 
        shows = {row["ID"]: {"title": row["TITLE"]} for row in cursor.fetchall()}
        conn.close()
        return shows
    

    # Fetch In-Progress TV Shows from Database View
    def fetch_tv_shows_episode_numbers(self, show_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ID, TITLE, MIN_EPISODE_NO, MAX_EPISODE_NO, LAST_WATCHED_EPISODE_NO FROM TV_SHOWS_TRACKING WHERE 1=1 AND ID = ?",(show_id,))  
        #shows = {row["ID"]: {"Title": row["TITLE"], "Min Episode no": row["MIN_EPISODE_NO"], "Max Episode no": row["MAX_EPISODE_NO"]}  for row in cursor.fetchall()}
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "ID": row["ID"],
                "Title": row["TITLE"],
                "Min Episode No": row["MIN_EPISODE_NO"],
                "Max Episode No": row["MAX_EPISODE_NO"],
                "Last Watched Episode No": row["LAST_WATCHED_EPISODE_NO"]
                }
        return None
    

    def insert_new_episodes(self, show_id, start_episode_no, end_episode_no):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Fetch existing episodes for the show
        cursor.execute("SELECT EPISODE_NO FROM EPISODES WHERE RELATED_ID = ?", (show_id,))
        existing_episodes = {row[0] for row in cursor.fetchall()}  # Convert to a set for fast lookup

        new_episodes = []  # Store new episodes to be inserted
        for episode_no in range(start_episode_no, end_episode_no + 1):
            if episode_no not in existing_episodes:  # Only insert if not already in DB
                new_episodes.append((show_id, episode_no))

        # Batch insert new episodes if there are any
        if new_episodes:
            cursor.executemany("INSERT INTO EPISODES (RELATED_ID, EPISODE_NO) VALUES (?, ?)", new_episodes)
            conn.commit()
            st.success(f"✅ {len(new_episodes)} new episodes inserted!")
        else:
            st.warning("⚠️ All selected episodes already exist in the database.")

        conn.close()


    def mark_episode_as_watched(self, show_id, start_episode_no, end_episode_no):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Fetch unwatched episodes for the show
        cursor.execute("SELECT EPISODE_NO FROM EPISODES WHERE 1=1 AND WATCHED_DATE IS NULL AND RELATED_ID = ?", (show_id,))
        existing_episodes = {row[0] for row in cursor.fetchall()}  # Convert to a set for fast lookup

        new_episodes = []  # Store existing episodes to be updated
        for episode_no in range(start_episode_no, end_episode_no + 1):
            if episode_no in existing_episodes:  # Only update if not already watched
                new_episodes.append((st.session_state.current_day, show_id, episode_no))

        # Batch update new episodes if there are any
        if new_episodes:
            cursor.executemany("UPDATE EPISODES SET WATCHED_DATE = ? WHERE 1=1 AND RELATED_ID = ? AND EPISODE_NO = ?", new_episodes)
            conn.commit()
            st.success(f"✅ {len(new_episodes)} episodes are marked as watched!")
        else:
            st.warning("⚠️ All selected episodes already marked as watched in the database.")

        conn.close()


    # Fetch In-Progress TV Shows from Database View
    def fetch_tv_shows_detail(self, show_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Fetch details for the selected show
        cursor.execute("SELECT * FROM TV_SHOWS_TRACKING WHERE ID = ? ORDER BY EPISODE_NO DESC", (show_id,))
        rows = cursor.fetchall()

        # Get column names from the cursor
        columns = [desc[0] for desc in cursor.description]

        # Convert to a DataFrame
        df = pd.DataFrame(rows, columns=columns)

        conn.close()
        return df
    

    # Function to fetch data
    def fetch_record(self, imdb_tt):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        original_df = pd.read_sql_query(
            """SELECT ID, IMDB_TT, TYPE,
            ORIGINAL_TITLE, PRIMARY_TITLE,
            RELEASE_YEAR, 
            STATUS, SCORE, SCORE_DATE,
            DURATION, RATING, RATING_COUNT, GENRES,
            WATCH_GRADE, BEYAZPERDE_LINK
            FROM MAIN_DATA WHERE IMDB_TT = ?""", conn, params=(imdb_tt,))
        conn.close()

        return original_df
    
