import streamlit as st
from utils import my_functions
from utils.utils import display_menu_buttons


obj = my_functions.MyClass()


# Function to update the database
def update_database(): # update_database_record
    update_counter = 0
    update_syntax_middle = ""
    update_syntax_middle_values = []
    

    if (
        st.session_state["imdb_tt_original"] != st.session_state["imdb_tt_new"]
        and st.session_state["imdb_tt_new"] not in ["", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,IMDB_TT = ?"
        update_syntax_middle_values.append(st.session_state["imdb_tt_new"])


    if (
        st.session_state["type_original"] != st.session_state["type_new"]
        and st.session_state["type_new"] not in ["", "Select a value", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,TYPE = ?"
        update_syntax_middle_values.append(st.session_state["type_new"])
    

    if (
        st.session_state["original_title_original"] != st.session_state["original_title_new"]
        and st.session_state["original_title_new"] not in ["", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,ORIGINAL_TITLE = ?"
        update_syntax_middle_values.append(st.session_state["original_title_new"])
    

    if (
        st.session_state["primary_title_original"] != st.session_state["primary_title_new"]
        and st.session_state["primary_title_new"] not in ["", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,PRIMARY_TITLE = ?"
        update_syntax_middle_values.append(st.session_state["primary_title_new"])
    

    if (
        st.session_state["release_year_original"] != st.session_state["release_year_new"]
        and st.session_state["release_year_new"] not in ["", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,RELEASE_YEAR = ?"
        update_syntax_middle_values.append(st.session_state["release_year_new"])


    if (
        st.session_state["status_original"] != st.session_state["status_new"]
        and st.session_state["status_new"] not in ["", "Select a value", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,STATUS = ?"
        update_syntax_middle_values.append(st.session_state["status_new"])
    

    if (
        st.session_state["score_original"] != st.session_state["score_new"]
        and st.session_state["score_new"] not in ["", 0, None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,SCORE = ?"
        update_syntax_middle_values.append(st.session_state["score_new"])


    if (
        st.session_state["score_date_original"] != st.session_state["score_date_new"]
        and st.session_state["score_date_new"] not in ["", None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,SCORE_DATE = ?"
        update_syntax_middle_values.append(st.session_state["score_date_new"])
    

    if (
        st.session_state["duration_original"] != st.session_state["duration_new"]
        and st.session_state["duration_new"] not in ["", 0, None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,DURATION = ?"
        update_syntax_middle_values.append(st.session_state["duration_new"])
    

    if (
        st.session_state["imdb_rating_original"] != st.session_state["imdb_rating_new"]
        and st.session_state["imdb_rating_new"] not in ["", 0, None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,RATING = ?"
        update_syntax_middle_values.append(st.session_state["imdb_rating_new"])

        
        update_syntax_middle = update_syntax_middle + " ,RATING_UPDATE_DATE = ?"
        update_syntax_middle_values.append(st.session_state.current_day)
    

    if (
        st.session_state["imdb_rating_count_original"] != st.session_state["imdb_rating_count_new"]
        and st.session_state["imdb_rating_count_new"] not in ["", 0, None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,RATING_COUNT = ?"
        update_syntax_middle_values.append(st.session_state["imdb_rating_count_new"])
    

    if "Select a value" in st.session_state["genres_new"]:
        st.session_state["genres_new"].remove("Select a value")
    
    if (
        st.session_state["genres_original"] != st.session_state["genres_new"]
        #and st.session_state["genres_new"] not in ["","Select a value", None]
        and st.session_state["genres_new"]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,GENRES = ?"
        update_syntax_middle_values.append(", ".join(st.session_state["genres_new"]))

        update_syntax_middle = update_syntax_middle + " ,GENRES_UPDATE_DATE = ?"
        update_syntax_middle_values.append(st.session_state.current_day)
    

    if (
        st.session_state["watch_grade_original"] != st.session_state["watch_grade_new"]
        and st.session_state["watch_grade_new"] not in ["", 0, None]
    ):
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,WATCH_GRADE = ?"
        update_syntax_middle_values.append(st.session_state["watch_grade_new"])
    

    if (
        st.session_state["beyazperde_link_original"] != st.session_state["beyazperde_link_new"]
        and st.session_state["beyazperde_link_new"] not in ["", None]
    ):
        
        update_counter += 1
        update_syntax_middle = update_syntax_middle + " ,BEYAZPERDE_LINK = ?"
        update_syntax_middle_values.append(obj.beyazperde_converter(st.session_state["beyazperde_link_new"], "in"))

    # Pre-check
    if st.session_state["score_new"] > 0 and not st.session_state["score_date_new"]:
        st.toast("Score and Score Data fields are inconsistent 1")
    elif st.session_state["score_new"] == 0 and st.session_state["score_date_new"]:
        st.toast("Score and Score Data fields are inconsistent 2")
    elif st.session_state["score_new"] % 5 != 0:
        st.toast("Score field is not divisible by 5")
    elif st.session_state["score_new"] > 0 and st.session_state["status_new"] != "WATCHED":
        st.toast("Score and Status fields are inconsistent")
    elif not st.session_state["score_date_new"] and st.session_state["status_new"] == "WATCHED":
        st.toast("Score Date and Status fields are inconsistent 1")
    elif st.session_state["score_date_new"] and st.session_state["status_new"] != "WATCHED":
        st.toast("Score Date and Status fields are inconsistent 2")
    elif st.session_state["watch_grade_new"] > 0 and st.session_state["status_new"] == "WATCHED":
        st.toast("Watch Grade and Status fields are inconsistent")
    else:
        if update_counter > 0:
            st.write(f"Update field count: {update_counter}")

            # Update
            conn = obj.get_db_connection()
            cursor = conn.cursor()

            # Manual Update Date
            update_syntax_middle = update_syntax_middle + " ,MANUAL_UPDATE_DATE = ?"
            update_syntax_middle_values.append(st.session_state.current_day)

            
            update_syntax_start = "UPDATE MAIN_DATA SET ID = ID" 
            update_syntax_end = " WHERE 1=1 AND ID = ?"
            
            update_syntax_final = update_syntax_start + "".join(update_syntax_middle) + update_syntax_end
            update_syntax_middle_values.append(st.session_state["id_new"])  

            st.write(f"update_syntax: {update_syntax_final}")
            st.write(f"update_syntax_middle_values: {update_syntax_middle_values}")

            try:
                cursor.execute(update_syntax_final, update_syntax_middle_values)
                conn.commit()
                st.success("✅ Database updated successfully!")
            except:
                st.error(f"Database update error")
            finally:
                cursor.close()
                conn.close()
        else:
            st.toast("No change to update")




def show(navigate_to):
    st.title("Update Record")
    
    display_menu_buttons(navigate_to)

    
    # UI Components
    imdb_link = st.text_input("IMDb Link", value="https://www.imdb.com/title/", key="imdb_link")
    find_record_button = st.button("Find Record", key="find_record")

    # Pre-check
    if find_record_button:
        


        imdb_title_format_check = obj.check_imdb_title(imdb_link)
        imdb_in = obj.imdb_converter(imdb_link, "in")

        if imdb_title_format_check == 0: # "/title/tt" format check
            st.toast("IMDb Link does not have proper format")
        elif imdb_in == "Error":
            st.toast("IMDb Link has error")
        elif obj.check_existing_record(imdb_in) == 0:
            st.toast("Record doesn't exist")
        else:
            df = obj.fetch_record(imdb_in)
            
            if not df.empty:
                st.session_state.fetched_record = df.iloc[0].to_dict()  # Store fetched record

    if "fetched_record" in st.session_state:
        with st.container():
            title_type_options = {
                "Movie": ["Movie", "Short", "TV Movie", "TV Special", "Video", "Unknown"],
                "TV Series": ["TV Series", "TV Mini Series", "Unknown"],
                "Unknown": ["Unknown"]
                }
            title_type_options_keys = list(title_type_options.keys())
            title_type_options_keys.append("Select a value")
            title_type_options_keys.insert(0,"Select a value")

            status_options = ["Select a value", "POTENTIAL", "TO BE WATCHED", "MAYBE", "N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"]


            col_original, col_new = st.columns(2)

            fetched_record = st.session_state.fetched_record
            
            #id_original = df.iloc[0, 0] if not df.empty else ""
            id_original = fetched_record.get("ID", "")
            col_original.text_input("Original ID", value=id_original, disabled=True, key="id_original")
            col_new.text_input("New ID", value=id_original, disabled=True, key="id_new")

            #imdb_tt_original = df.iloc[0, 1] if not df.empty else ""
            imdb_tt_original = fetched_record.get("IMDB_TT", "")
            col_original.text_input("Original IMDb TT", value=imdb_tt_original, disabled=True, key="imdb_tt_original")
            col_new.text_input("New IMDb TT", key="imdb_tt_new")

            #type_original = df.iloc[0, 2] if not df.empty else ""
            type_original = fetched_record.get("TYPE", "")
            col_original.text_input("Original Type", value=type_original, disabled=True, key="type_original")
            col_new.selectbox(
            "New Type",
            title_type_options_keys,
            #("1","2","3"),
            index=0,  # Default: "Unknown"
            key="type_new"
            )

            #original_title_original = df.iloc[0, 3] if not df.empty else ""
            original_title_original = fetched_record.get("ORIGINAL_TITLE", "")
            col_original.text_input("Original Title", value=original_title_original, disabled=True, key="original_title_original")
            col_new.text_input("New Original Title", value="", key="original_title_new")

            #primary_title_original = df.iloc[0, 4] if not df.empty else ""
            primary_title_original = fetched_record.get("PRIMARY_TITLE", "")
            col_original.text_input("Primary Title", value=primary_title_original, disabled=True, key="primary_title_original")
            col_new.text_input("New Primary Title", value="", key="primary_title_new")

            #release_year_original = df.iloc[0,5] if not df.empty else ""
            release_year_original = fetched_record.get("RELEASE_YEAR", "")
            col_original.text_input("Release Year", value=release_year_original, disabled=True,key="release_year_original")
            col_new.number_input("New Release Year", value=None, min_value=1888, max_value=st.session_state.current_year, key="release_year_new")

            #status_original = df.iloc[0,6] if not df.empty else ""
            status_original = fetched_record.get("STATUS", "")
            col_original.text_input("Status", value=status_original, disabled=True,key="status_original")
            col_new.selectbox(
            "New Status",
            status_options,
            #horizontal=True,  # Makes options appear inline
            index=0,  # Default: "POTENTIAL"
            key="status_new"
            )
            
            #score_original = df.iloc[0,7] if not df.empty else ""
            score_original = fetched_record.get("SCORE", "")
            col_original.text_input("Score", value=score_original, disabled=True,key="score_original")
            col_new.number_input("New Score", min_value=0, max_value=100, step=5, key="score_new") # It is define as text_input because when it is number_input min_valus is automatically 0 or 0.00

            #score_date_original = df.iloc[0,8] if not df.empty else ""
            score_date_original = fetched_record.get("SCORE_DATE", "")
            col_original.text_input("Score Date", value=score_date_original, disabled=True, key="score_date_original")
            col_new.date_input("New Score Date", value=None, key="score_date_new", ) #value=st.session_state.current_day,

            #duration_original = df.iloc[0,9] if not df.empty else ""
            duration_original = fetched_record.get("DURATION", "")
            col_original.text_input("Duration", value=duration_original, disabled=True, key="duration_original")
            col_new.number_input("New Duration", min_value=0, value=0, key="duration_new")

            #imdb_rating_original = df.iloc[0,10] if not df.empty else ""
            imdb_rating_original = fetched_record.get("RATING", "")
            col_original.number_input("IMDb Rating", value=imdb_rating_original, disabled=True, format="%.1f", key="imdb_rating_original")
            col_new.number_input("New IMDb Rating", min_value=0.0, max_value=10.0, step=0.10, format="%.1f", key="imdb_rating_new")

            #imdb_rating_count_original = df.iloc[0,11] if not df.empty else ""
            imdb_rating_count_original = fetched_record.get("RATING_COUNT", "")
            col_original.text_input("IMDb Rating Count", value=imdb_rating_count_original, disabled=True, key="imdb_rating_count_original")
            col_new.number_input("New IMDb Rating Count", min_value=0, value=0, key="imdb_rating_count_new")

            #genres_original = df.iloc[0,12] if not df.empty else ""
            genres_original = fetched_record.get("GENRES", "")
            col_original.text_input("Genres", value=genres_original, disabled=True, key="genres_original")
            col_new.multiselect(
                'New Genres',
                ["Select a value", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show", "History",
                "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"], default="Select a value", key="genres_new")

            #watch_grade_original = df.iloc[0,13] if not df.empty else ""
            watch_grade_original = fetched_record.get("WATCH_GRADE", "")
            col_original.text_input("Watch Grade", value=watch_grade_original, disabled=True, key="watch_grade_original")
            col_new.number_input("New Watch Grade", min_value=0, max_value=10, value=0, key="watch_grade_new")

            #beyazperde_link_original = df.iloc[0, 14] if not df.empty else ""
            beyazperde_link_original = fetched_record.get("BEYAZPERDE_LINK", "")
            col_original.text_input("Beyazperde Link", value=beyazperde_link_original, disabled=True, key="beyazperde_link_original")
            col_new.text_input("New Beyazperde Link", value="", key="beyazperde_link_new")

            


        update_record = st.button("Update Database", key="update_database")

        if update_record:
            #st.write("update_record is clicked")
            update_database()


