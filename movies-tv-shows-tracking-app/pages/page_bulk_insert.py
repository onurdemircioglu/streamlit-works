import streamlit as st
from utils.utils import display_menu_buttons
from utils import my_functions

obj = my_functions.MyClass()

def show(navigate_to):
    st.title("Bulk Insert")

    display_menu_buttons(navigate_to)

    manual_rows = []

    input_text_area = st.text_area("Paste tabular data (e.g., from Excel or TSV) Format: IMDB_TT, Status, Watch Grading, Watch Link (without the headers)")

    parse_button = st.button("Parse the text")


    # Status Map - StatusMap.csv
    status_action_map = {
                ("DROPPED", "DROPPED"): "skip", # Both DROPEED
                ("DROPPED", "IN PROGRESS"): "skip", #Existing IN PROGRESS
                ("DROPPED", "MAYBE"): "skip", # Existing MAYBE
                ("DROPPED", "N2WATCH"): "skip", # Existing N2WATCH
                ("DROPPED", "POTENTIAL"): "skip", #Existing POTENTIAL
                ("DROPPED", "TO BE WATCHED"): "skip", #Existing TO BE WATCHED
                ("DROPPED", "WATCHED"): "skip", # Existing WATCHED
                ("IN PROGRESS", "DROPPED"): "manual_review",
                ("IN PROGRESS", "IN PROGRESS"): "skip",
                ("IN PROGRESS", "MAYBE"): "manual_review",
                ("IN PROGRESS", "N2WATCH"): "manual_review",
                ("IN PROGRESS", "POTENTIAL"): "update",
                ("IN PROGRESS", "TO BE WATCHED"): "update",
                ("IN PROGRESS", "WATCHED"): "skip",
                ("MAYBE", "DROPPED"): "update",
                ("MAYBE", "IN PROGRESS"): "skip",
                ("MAYBE", "MAYBE"): "check watch grade",
                ("MAYBE", "N2WATCH"): "update",
                ("MAYBE", "POTENTIAL"): "update",
                ("MAYBE", "TO BE WATCHED"): "manual_review",
                ("MAYBE", "WATCHED"): "skip",
                ("N2WATCH", "DROPPED"): "skip",
                ("N2WATCH", "IN PROGRESS"): "skip",
                ("N2WATCH", "MAYBE"): "manual_review",
                ("N2WATCH", "N2WATCH"): "skip",
                ("N2WATCH", "POTENTIAL"): "update",
                ("N2WATCH", "TO BE WATCHED"): "manual_review",
                ("N2WATCH", "WATCHED"): "skip",
                ("POTENTIAL", "DROPPED"): "skip",
                ("POTENTIAL", "IN PROGRESS"): "skip",
                ("POTENTIAL", "MAYBE"): "skip",
                ("POTENTIAL", "N2WATCH"): "skip",
                ("POTENTIAL", "POTENTIAL"): "skip",
                ("POTENTIAL", "TO BE WATCHED"): "skip",
                ("POTENTIAL", "WATCHED"): "skip",
                ("TO BE WATCHED", "DROPPED"): "manual_review",
                ("TO BE WATCHED", "IN PROGRESS"): "skip",
                ("TO BE WATCHED", "MAYBE"): "update",
                ("TO BE WATCHED", "N2WATCH"): "update",
                ("TO BE WATCHED", "POTENTIAL"): "update",
                ("TO BE WATCHED", "TO BE WATCHED"): "check watch grade",
                ("TO BE WATCHED", "WATCHED"): "skip",
                ("WATCHED", "DROPPED"): "skip",
                ("WATCHED", "IN PROGRESS"): "skip",
                ("WATCHED", "MAYBE"): "skip",
                ("WATCHED", "N2WATCH"): "skip",
                ("WATCHED", "POTENTIAL"): "skip",
                ("WATCHED", "TO BE WATCHED"): "skip",
                ("WATCHED", "WATCHED"): "skip",
    }

    if parse_button and input_text_area:
        parsed_rows = input_text_area.strip().split("\n")  # Split text by rows


        for row_index, row in enumerate(parsed_rows):
            cols = row.split("\t") # Split columns by tab
            ##st.write(f"Row {row_index + 1}:")

            bulk_imdb_tt     = cols[0] if len(cols) > 0 else ""
            bulk_status      = cols[1] if len(cols) > 1 else ""
            bulk_watch_grade = cols[2] if len(cols) > 2 else ""
            bulk_watch_grade = int(bulk_watch_grade) if bulk_watch_grade not in (None, "", "NULL") else 0
            bulk_watch_link  = cols[3] if len(cols) > 3 else ""
            
            if obj.check_imdb_title(bulk_imdb_tt) == 1: # "/title/tt" format ok
                imdb_in = obj.imdb_converter(bulk_imdb_tt, "in") # Convert IMDb link

                if obj.check_existing_record(imdb_in) == 1: # Existing Record
                    fetched_records = obj.fetch_record(imdb_in)
                    fetched_status = fetched_records["STATUS"][0]
                    fetched_watch_grade = fetched_records["WATCH_GRADE"][0]
                    fetched_id = fetched_records["ID"][0] # ya da sonrasında fetched_id[0] olarak kullanmak gerekiyor. Yoksa Series[Unknown]" is not assignable to "int" uyarısı/hatası veriyor

                    # Inserting watch link
                    if bulk_watch_link != None: # Status bilgisinden bağımsız olarak kayıt içeride var ise ve link var ise her durumda bu linki insert etsin
                        st.write(fetched_id)
                        
                        is_duplicate = obj.check_existing_record_other_links(int(fetched_id), bulk_watch_link)
                        if is_duplicate == 0: # No duplication
                            obj.insert_other_links(int(fetched_id), "Watch link", bulk_watch_link) # fetched_id alanı int olarak conversion oluyor çünkü normalde np.int64(2606) olarak geliyor. Bu durumda da tabloya insert etmiyor.
                    
                    action = status_action_map.get((bulk_status, fetched_status), "manual_review")  # Default fallback
                    st.write(action)

                    if action in ("skip", "manual_review - skip", "manual_review"):
                        reason = action
                        cols.append(reason)
                        #manual_rows.append(row)
                        manual_rows.append("\t".join(cols))
                    
                    elif action in  ("update", "check watch grade"): # Manual mapleme içinde check watch grade aynı statüde olanlar (MAYBE, TO BE WATCHED) olduğu için update akışı ile aynı akış içinde olabiliyor.
                        if bulk_status in ("MAYBE", "TO BE WATCHED", "N2WATCH"):

                            max_watch_grade = max(
                                bulk_watch_grade,
                                int(fetched_watch_grade) if fetched_watch_grade not in (None, "", "NULL") else 0
                            )

                            # Update
                            conn = obj.get_db_connection()
                            cursor = conn.cursor()

                            update_syntax = "UPDATE MAIN_DATA SET STATUS = ?, WATCH_GRADE = ? WHERE 1=1 AND ID = ?"  

                            #st.write(f"update_syntax: {update_syntax}")

                            try:
                                st.write(f"Trying to update record with ID = {int(fetched_id)}")

                                # Check if any rows were actually modified:
                                result = cursor.execute(update_syntax, (bulk_status, max_watch_grade, int(fetched_id)))
                                
                                if cursor.rowcount == 0:
                                    st.warning("⚠️ No rows were updated. Check if the ID exists.")
                                else:
                                    st.success("✅ Database updated successfully!")

                                conn.commit()
                            except Exception as e:
                                st.error(f"Database update error")
                            finally:
                                cursor.close()
                                conn.close()
                    else:
                        reason = "else case"
                        cols.append(reason)
                        #manual_rows.append(row)
                        manual_rows.append("\t".join(cols))
                        
                else: # New Record
                    # Inserting new record
                    new_record_result = obj.insert_new_record( imdb_tt=imdb_in, record_status=bulk_status, watch_grade=bulk_watch_grade )

                    # When it is a new record, it doesn't insert new record and watch link at the same time. insert_new_record returns new_record_id and we use it to insert into OTHER_LINKS table
                    if bulk_watch_link != None:
                        obj.insert_other_links(int(new_record_result), "Watch link", bulk_watch_link)

                    
            else: # "/title/tt" format not ok
                reason = "imdb title format problem"
                cols.append(reason)
                #manual_rows.append(row)
                manual_rows.append("\t".join(cols))
        
        st.write("Process Completed")
        
        
        if manual_rows:
            st.subheader("#🛠️ Rows Needing Manual Review")
            st.text_area("Unprocessed or manual records will be here", value="\n".join(manual_rows),  # This line keeps tabs, separates rows
        height=300)
            
        
    

        








