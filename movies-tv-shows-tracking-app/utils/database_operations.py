import my_functions

obj = my_functions.MyClass()

def create_database_objects():
    conn = obj.get_db_connection()
    cursor = conn.cursor()

    # Create MAIN_DATA table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MAIN_DATA (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TYPE TEXT,
            TITLE_TYPE TEXT,
            IMDB_TT TEXT,
            BEYAZPERDE_LINK TEXT,
            ORIGINAL_TITLE TEXT,
            PRIMARY_TITLE TEXT,
            RELEASE_YEAR,
            STATUS TEXT,
            SCORE INTEGER,
            SCORE_DATE TEXT,
            DURATION INTEGER,
            RATING REAL,
            RATING_COUNT INTEGER,
            RATING_UPDATE_DATE,
            GENRES TEXT,
            GENRES_UPDATE_DATE TEXT,
            WATCH_GRADE INTEGER,
            INSERT_DATE TEXT DEFAULT (DATE('now')),
            MANUAL_UPDATE_DATE TEXT DEFAULT (DATE('now')),
            AUTOMATIC_UPDATE_DATE TEXT
        )
    """)
    conn.commit()


    # Create EPISODES table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EPISODES (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            RELATED_ID INTEGER,
            EPISODE_NO INTEGER,
            EPISODE_NAME TEXT,
            INSERT_DATE TEXT DEFAULT (DATE('now')),
            UPDATE_DATE TEXT DEFAULT (DATE('now')),
            WATCHED_DATE TEXT DEFAULT '1900-01-01'
        )
    """)
    conn.commit()


    # Create WATCH_LINKS table (if not exists) (Type can be trailer or watch link => TRAILER, WATCH_LINK, OTHER)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS WATCH_LINKS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            RELATED_ID INTEGER,
            TYPE TEXT,
            LINK TEXT
        )
    """)
    conn.commit()


    # Create recommendation table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TODAYS_RECOMMENDATION (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            RELATED_ID INTEGER,
            IMDB_TT TEXT,
            RECOMMENDATION_DATE TEXT DEFAULT (DATE('now'))
        )
    """)


    cursor.execute("""
    DROP VIEW IF EXISTS "main"."TV_SHOWS_LAST_WATCHED"
    """)
    cursor.execute("""
    CREATE VIEW TV_SHOWS_LAST_WATCHED AS
    SELECT B.ID,
        B.TYPE,
        B.TITLE_TYPE,
        B.IMDB_TT,
        CASE 
            WHEN B.PRIMARY_TITLE IS NULL THEN B.ORIGINAL_TITLE 
            ELSE B.ORIGINAL_TITLE || ' - ' || B.PRIMARY_TITLE 
        END AS TITLE,
        B.RELEASE_YEAR,
        B.DURATION,
        B.RATING,
        B.RATING_COUNT,
        B.GENRES,
        A.MAX_WATCHED_DATE,
        A.MAX_EPISODE_NO AS LATEST_EPISODE
    FROM
        (
        SELECT A.RELATED_ID,
            A.MAX_WATCHED_DATE,
            B.MAX_EPISODE_NO
        FROM
            (
            SELECT RELATED_ID, MAX(WATCHED_DATE) AS MAX_WATCHED_DATE
            FROM EPISODES
            GROUP BY RELATED_ID
            ) A
        INNER JOIN
            (
            SELECT RELATED_ID, MAX(EPISODE_NO) AS MAX_EPISODE_NO
            FROM EPISODES
            WHERE WATCHED_DATE IS NOT NULL
            GROUP BY RELATED_ID
            ) B
        ON A.RELATED_ID = B.RELATED_ID
        ) A
    INNER JOIN
        (
        SELECT *
        FROM MAIN_DATA
        WHERE STATUS = 'IN PROGRESS'
        ) B
    ON A.RELATED_ID = B.ID
    """)


    cursor.execute("""
    DROP VIEW IF EXISTS "main"."TV_SHOWS_TRACKING"
    """)
    cursor.execute("""
    CREATE VIEW TV_SHOWS_TRACKING AS
    SELECT A.*,
        B.EPISODE_NO,
        B.MIN_EPISODE_NO,
        B.MAX_EPISODE_NO,
        B.EPISODE_NAME,
        B.UPDATE_DATE,
        B.WATCHED_DATE,
        B.LAST_WATCHED_EPISODE_NO
    FROM    
        (
        SELECT ID, 
            TYPE, 
            IMDB_TT, 
            CASE 
                WHEN PRIMARY_TITLE IS NOT NULL THEN ORIGINAL_TITLE || '-' || PRIMARY_TITLE 
                ELSE ORIGINAL_TITLE 
            END AS TITLE,
            MANUAL_UPDATE_DATE
        FROM MAIN_DATA
        WHERE STATUS = 'IN PROGRESS'
        ) A
    LEFT JOIN
        (
        SELECT RELATED_ID, 
            EPISODE_NO, 
            EPISODE_NAME, 
            UPDATE_DATE, 
            WATCHED_DATE,
            MIN(EPISODE_NO) OVER (PARTITION BY RELATED_ID) AS MIN_EPISODE_NO,
            MAX(EPISODE_NO) OVER (PARTITION BY RELATED_ID) AS MAX_EPISODE_NO,
            MAX(WATCHED_DATE) OVER (PARTITION BY RELATED_ID) AS MAX_WATCHED_DATE,
            MAX(CASE WHEN WATCHED_DATE IS NOT NULL THEN EPISODE_NO ELSE 0 END) OVER (PARTITION BY RELATED_ID) AS LAST_WATCHED_EPISODE_NO
        FROM EPISODES
        ) B
    ON A.ID = B.RELATED_ID
    ORDER BY IFNULL(A.MANUAL_UPDATE_DATE, '2999-01-01') DESC,
            IFNULL(B.MAX_WATCHED_DATE, '2999-01-01') DESC
    """)

    # Close connection on exit
    conn.close()


create_database_objects()