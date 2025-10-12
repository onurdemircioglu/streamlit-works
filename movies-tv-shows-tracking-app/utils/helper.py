import streamlit as st

# Set page config
#st.set_page_config(page_title="Movies & TV Series Tracker", page_icon="🎥")

# ":smiley:"
# "🎥"
#icon="🎦",
#icon="📺",
st.subheader("🎬 Add a Movie")


# Example: Display a sample movie list
movies = ["Inception", "Interstellar", "The Dark Knight"]
for movie in movies:
    st.markdown(f"- 🎬 {movie}")
    


Retrieve & Convert Back to List
# Fetch data from the database
cursor.execute("SELECT genres FROM movies WHERE title = ?", (title,))
row = cursor.fetchone()

if row:
    stored_genres = row[0]  # Stored as a comma-separated string
    imdb_genres_list = stored_genres.split(", ") if stored_genres else []  # Convert back to list
    st.write("Selected Genres:", imdb_genres_list)



streamlit cache clear





pip install streamlit
pip install streamlit-elements==0.1










# template ya da blog. chat yapılabilri bununla farklı userlar ile https://www.restack.io/docs/streamlit-knowledge-streamlit-chat-feedback-insights#clvottssx0d2d11mob1ljbmhn
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
prompt = st.chat_input("Say something")
if prompt:
    # Echo the input back to the chat
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()



left, middle, right = st.columns(3)

left.button("Insert Record", use_container_width=True, on_click=insert_new_record_process)
    #pass  # No need for extra logic here
#if left.button("Insert Record", use_container_width=True, on_click=insert_new_record):


if middle.button("Clear Form", use_container_width=True):
    clear_form()
    st.rerun()  # Refresh the page to apply changes
if right.button("Unknown Button", use_container_width=True):
    right.markdown("You clicked the Unknown button.")






blog ya da template. st.form içinde çalışmıyor bu
import streamlit as st

# Define category-wise options
category_options = {
    "Fruits": ["Apple", "Banana", "Orange", "Mango"],
    "Vegetables": ["Carrot", "Broccoli", "Spinach", "Potato"],
    "Dairy": ["Milk", "Cheese", "Yogurt"]
}

# First selection with radio buttons
selected_category = st.radio("Select Category", list(category_options.keys()), index=None)

# Second selectbox updates based on first selection
if selected_category:
    selected_item = st.selectbox("Select Item", category_options[selected_category], key="items")
    st.write("**Selected Category:**", selected_category)
    st.write("**Selected Item:**", selected_item)
else:
    st.warning("Please select a category to see items.")






https://www.sqlite.org/lang_corefunc.html#ifnull



  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.77:8501




  You can find our privacy policy at https://streamlit.io/privacy-policy

  Summary:
  - This open source library collects usage statistics.
  - We cannot see and do not store information contained inside Streamlit apps,
    such as text, charts, images, etc.
  - Telemetry data is stored in servers in the United States.
  - If you'd like to opt out, add the following to %userprofile%/.streamlit/config.toml,
    creating that file if necessary:

    [browser]
    gatherUsageStats = false










import streamlit as st
from utils.utils import display_menu_buttons
from utils import my_functions

obj = my_functions.MyClass()

def show(navigate_to):
    st.title("Bulk Insert")

    display_menu_buttons(navigate_to)

    manual_rows = []

    input_text_area = st.text_area("Paste tabular data (e.g., from Excel or TSV) Format: IMDB_TT, Status, Watch Grading, Watch Link")

    parse_button = st.button("Parse the text")

    if parse_button and input_text_area:
        rows = input_text_area.strip().split("\n")  # Split text by rows

        for i, row in enumerate(rows):
            cols = row.split("\t")  # Split each row into columns
            st.write(f"🔹 Row {i + 1}:")
            for j, col in enumerate(cols):
                st.write(f"  - Column {j + 1}: `{col}`")  # Or process it here
                if obj.check_imdb_title(col) == 1: # "/title/tt" format ok
                    imdb_in = obj.imdb_converter(col, "in") # Convert IMDb link
                    st.write(imdb_in) # TODO: Sonra silinecek
                    if obj.check_existing_record(imdb_in) == 1:
                        fetched_records = obj.fetch_record(imdb_in)

                        st.write("Record already exists in the database")
                        st.write(fetched_records)
                        st.write(fetched_records["STATUS"] == "WATCHED")
                    else:
                        st.write("New record")
    

                    

"""    if parse_button and my_text_area:
        rows = my_text_area.strip().split("\n")  # Split by rows
        parsed_data = [row.split("\t") for row in rows]  # Split by columns

        st.write("Parsed Data:")
        st.write(parsed_data)

        # Optional: Display as table
        st.table(parsed_data)"""

#imdb_title_format_check = obj.check_imdb_title(imdb_link)

#imdb_converter(imdb_url: str, in_out: str) -> str:



"""for i in range(1, len(cols)):
                previous = cols[i - 1]
                current = cols[i]
                # You can implement any logic here using both values
                st.write(f"  Col {i}: `{current}` (depends on `{previous}`)")"""








                    if fetched_status == "WATCHED":
                        reason = "Existing status WATCHED (watch link inserted)"
                        cols.append(reason)
                        manual_rows.append("\t".join(cols))
                    elif fetched_status == "IN PROGRESS":
                        reason = "Existing Status Overpredence - In Progress (watch link inserted)"
                        cols.append(reason)
                        manual_rows.append("\t".join(cols))
                    elif fetched_status == "DROPPED" and bulk_status != "POTENTIAL":
                        reason = "Manual Check DROPPED (watch link inserted)"
                        cols.append(reason)
                        manual_rows.append("\t".join(cols))
                    elif fetched_status == "POTENTIAL" and bulk_status == "POTENTIAL":
                        reason = "Duplicate Record - POTENTIAL + POTENTIAL (watch link inserted)"
                        cols.append(reason)
                        manual_rows.append("\t".join(cols))