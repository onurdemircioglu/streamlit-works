import streamlit as st


col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    My Works
    - [Movies TV Shows Tracking](https://app-works-jzt8gzeunzdfjsszheejit.streamlit.app/)
    
    - [Personal Finance Assistant](https://www.themoviedb.org)    
    
    - [Wheel of Fortune](https://www.rottentomatoes.com)
    """)

with col2:
    st.markdown("""
        Links
        - [My Blog (Substack)](https://computerdiaries.substack.com/)
        
        - [GitHub](https://github.com/onurdemircioglu)
        """)
