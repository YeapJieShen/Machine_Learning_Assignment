import streamlit as st

st.write('hi world')

option = st.radio(
    "Select an option:",
    ['Option 1', 'Option 2', 'Option 3'],
    horizontal = True
)

# Sidebar content based on the selected radio option
with st.sidebar:
    st.header("Sidebar Content")

    if option == 'Option 1':
        st.write("You selected Option 1.")
        st.slider("Slider for Option 1", 0, 100)

    elif option == 'Option 2':
        st.write("You selected Option 2.")
        st.text_input("Text Input for Option 2")

    elif option == 'Option 3':
        st.write("You selected Option 3.")
        st.button("Button for Option 3")

# Display the selected option in the main area
st.write(f"You have selected: {option}")