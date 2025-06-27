import streamlit as st
import pandas as pd
from utils import my_functions
from utils.utils import display_menu_buttons

obj = my_functions.MyClass()

def todays_recommendation():
    conn = obj.get_db_connection()
    sql_query = "SELECT * FROM TODAYS_RECOMMENDATION WHERE RECOMMENDATION_DATE = ?"
    result_recommendation = pd.read_sql_query(sql_query, conn, params=(st.session_state.current_day,))
    
    # Query all previous recommendations
    sql_prev_recommendations = "SELECT DISTINCT IMDB_TT FROM TODAYS_RECOMMENDATION"
    previous_recommendations = pd.read_sql_query(sql_prev_recommendations, conn)
    
    conn.close()

    # Picking a random record for recommendation (This is out of if block because it is also used by result_recommendation)
    random_pick_df = st.session_state.all_data_df.copy()

    if len(result_recommendation) == 0:
        st.write("No data found")
        
        # Filter for movies and TV shows, excluding "unknown" type
        random_pick_df = random_pick_df[random_pick_df["TYPE"].isin(["Movie", "TV Series"])]

        # Apply the given conditions
        filtered_df = random_pick_df[
            (random_pick_df["RATING"] >= 6) &  # Rating should be >= 6
            (random_pick_df["RATING_COUNT"] > 6000) &  # Rating count should be > 5000
            (~random_pick_df["STATUS"].isin(["TO BE WATCHED", "N2WATCH", "IN PROGRESS", "DROPPED"])) & # Status should not be in excluded statuses
            (random_pick_df["ORIGINAL_TITLE"].notna() | random_pick_df["PRIMARY_TITLE"].notna())  # At least one of ORIGINAL_TITLE or PRIMARY_TITLE should not be null
        ]

        # **Exclude previously recommended titles**
        if not previous_recommendations.empty:
            filtered_df = filtered_df[
                ~filtered_df["IMDB_TT"].isin(previous_recommendations["IMDB_TT"]) 
            ]


        # Check if there are any records that match the criteria
        if not filtered_df.empty:
            # Randomly select one record from the filtered data
            random_record = filtered_df.sample(n=1).iloc[0]

            # Write back into the database
            conn = obj.get_db_connection()
            cursor = conn.cursor()
            sql_query = "INSERT INTO TODAYS_RECOMMENDATION (RELATED_ID, IMDB_TT) VALUES(?, ?)"
            
            # Execute the insert query
            cursor.execute(sql_query, (int(random_record["ID"]), random_record['IMDB_TT']))
            conn.commit()
            conn.close()


            # Determine the title to display
            if pd.isna(random_record["PRIMARY_TITLE"]):
                display_title = random_record["ORIGINAL_TITLE"]
            else:
                display_title = f"{random_record['ORIGINAL_TITLE']} - {random_record['PRIMARY_TITLE']}"

            # Convert RATING_COUNT to integer (remove decimal point)
            if random_record["RATING_COUNT"]:
                rating_count_int = int(random_record["RATING_COUNT"])

            # Convert RELEASE_YEAR to integer (remove decimal point)
            if random_record["RELEASE_YEAR"]:
                release_year_int = int(random_record["RELEASE_YEAR"])

            imdb_link_formatted = "https://www.imdb.com/title/" + str(random_record['IMDB_TT'])
            
            
            # Display the random record's information
            st.subheader(f"Today's Recommendation: {display_title}")
            st.write(f"**ID**: {random_record['ID']}")
            st.write(f"**IMDb Link**: {imdb_link_formatted}")
            st.write(f"**Type**: {random_record['TYPE']}")
            st.write(f"**Release Year**: {release_year_int}")
            st.write(f"**Rating**: {random_record['RATING']}")
            st.write(f"**Rating Count**: {rating_count_int}")
            st.write(f"**Status**: {random_record['STATUS']}")
            st.write(f"**Genres**: {random_record['GENRES']}")
    
    else:
        if not result_recommendation.empty:
            imdb_tt_value = result_recommendation.iloc[0]["IMDB_TT"]  # Safely extract IMDB_TT
            result_recommendation_df = random_pick_df[random_pick_df["IMDB_TT"] == imdb_tt_value]

            #st.dataframe(result_recommendation_df, hide_index=True)

            selected_record = result_recommendation_df.iloc[0]  # Extract first row safely


            # Determine the title to display
            primary_title = selected_record["PRIMARY_TITLE"]
            original_title = selected_record["ORIGINAL_TITLE"]

            if pd.isna(primary_title):
                display_title = original_title
            else:
                display_title = f"{original_title} - {primary_title}"

            # Convert RATING_COUNT and RELEASE_YEAR to integer safely
            rating_count_int = int(selected_record["RATING_COUNT"]) if not pd.isna(selected_record["RATING_COUNT"]) else None
            release_year_int = int(selected_record["RELEASE_YEAR"]) if not pd.isna(selected_record["RELEASE_YEAR"]) else None

            # Format IMDb link
            imdb_link_formatted = f"https://www.imdb.com/title/{selected_record['IMDB_TT']}"

            # Display the selected record's information
            st.subheader(f"Today's Recommendation: {display_title}")
            st.write(f"**ID**: {selected_record['ID']}")
            st.write(f"**IMDb Link**: {imdb_link_formatted}")
            st.write(f"**Type**: {selected_record['TYPE']}")
            st.write(f"**Release Year**: {release_year_int if release_year_int else 'Unknown'}")
            st.write(f"**Rating**: {selected_record['RATING']}")
            st.write(f"**Rating Count**: {rating_count_int if rating_count_int else 'Unknown'}")
            st.write(f"**Status**: {selected_record['STATUS']}")
            st.write(f"**Genres**: {selected_record['GENRES']}")            
        else:
            st.write("No recommendation")








def show(navigate_to):
    st.title("Home Page")

    st.markdown("#### Keep track of your favorite movies and shows!")

    display_menu_buttons(navigate_to)

    todays_recommendation()

