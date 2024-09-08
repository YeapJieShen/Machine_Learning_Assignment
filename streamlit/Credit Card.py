# ml-venv\Scripts\activate
# cd streamlit
# streamlit run "Credit Card.py"
# deactivate

import streamlit as st

# Title for the app
st.title("Radio Button Example")

# Create radio buttons
option = st.radio(
    "Select an option:",
    ['Option 1', 'Option 2', 'Option 3'],
    horizontal = True
)

# Display corresponding messages based on the selection
if option == 'Option 1':
    st.write("Hi1")
    st.radio('IM hidden 1', ['1', '2', '3'], horizontal=True)
elif option == 'Option 2':
    st.write("Hi2")
elif option == 'Option 3':
    st.write("Hi3")