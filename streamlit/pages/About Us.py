import streamlit as st

st.set_page_config(
    page_title = 'About Us',
    page_icon = '👤',
    layout = 'wide',                   # Use full-width layout
    initial_sidebar_state = 'expanded' # Sidebar state: "expanded", "collapsed", "auto"
)

# Set the title of the page
st.title("About Us")

# Display the "About Us" information
st.write("""
This project is developed by three students from **Tunku Abdul Rahman University of Management and Technology (TAR UMT)**:

- **Yeap Jie Shen**
- **Gan Yee Jing**
- **Jerome Subash A/L Joseph**

We are currently pursuing a Bachelor's Degree in Computer Science (Honours) with a focus on Data Science, and currently in Year 2, Semester 3.

### Project Information

This project is part of the subject **BMCS 2114 Machine Learning**, which provides us with the opportunity to apply machine learning techniques and explore data science methodologies.

### Acknowledgements

We would like to extend our heartfelt appreciation to our lecturer and practical tutor, **Dr. Lim Siew Mooi**, for her invaluable guidance and support throughout this project️.

Thank you for your encouragement and for helping us grow as data scientists!

We hope you find this project insightful and useful in your data science journey.
""")
