# ml-venv\Scripts\activate
# cd streamlit
# streamlit run "Welcome.py"
# deactivate

import streamlit as st

st.set_page_config(
    page_title = 'Welcome',
    page_icon = '👋',
    layout = 'wide',                   # Use full-width layout
    initial_sidebar_state = 'expanded' # Sidebar state: "expanded", "collapsed", "auto"
)

# Set the title of the app
st.title("Welcome to Our App!")

# Display a welcome message
st.write("""
Welcome to our Data Science application! This app is designed to explore and analyze
the [**Credit Card Dataset for Clustering**](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) contributed by **Arjun Bhasin** on **Kaggle**
using various unsupervised machine learning techniques.

### Features of the App:
- **Clustering Analysis**: Perform clustering with different algorithms and visualize results.
- **Model Evaluation**: Compare models using various metrics and visualizations.
- **Interactive Plots**: Explore data through interactive charts and plots.

### Unsupervised Machine Learning Techniques Used:
1) **Agglomerative Clustering**: Hierarchical clustering algorithm that builds a tree of clusters.
2) **Mean Shift Clustering**: Non-parametric clustering algorithm that assigns data points to the nearest mode.
3) **BIRCH**: Hierarchical clustering algorithm that uses a tree data structure to store the clustering information.
4) **HDBSCAN**: Density-based clustering algorithm that finds clusters of varying densities in data.
5) **OPTICS**: Density-based clustering algorithm that orders data points based on their density.

### Getting Started:
- Use the sidebar to navigate through the different sections of the app.
- Follow the instructions provided in each section for detailed analysis and visualizations.

If you have any questions or need assistance, feel free to check out our documentation.

Thank you for using our Data Science App. We hope you find it useful and insightful!

Enjoy exploring the data!

[**Link to GitHub Repository**](https://github.com/YeapJieShen/Machine_Learning_Assignment)
""")

st.divider()
st.write("Created with ❤️ by Yeap Jie Shen, Gan Yee Jing & Jerome Subash A/L Joseph")
