import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# House tips (can be displayed randomly later if needed)
house_tips = [
    "Make sure you research the neighborhood before buying a house.",
    "Check for any hidden maintenance costs before making your purchase.",
    "Consider future developments in the area that may affect property value.",
    "Factor in property taxes when budgeting for your new home.",
    "Don't rush into a decision—take your time to find the perfect home."
]

# Streamlit UI Configuration
st.set_page_config(page_title="House Price Prediction", layout="wide")
st.title('🏡 House Price Prediction')

# Sidebar for navigation
st.sidebar.header("Navigation")
sidebar_selection = st.sidebar.radio("Go to", ("Home", "House Price Predictor", "Reports"))

# HTML, CSS for custom UI
html_code = """
<style>
    body {
        background-color: #f4f7f6;
        font-family: 'Arial', sans-serif;
        color: #333;
    }
    .header {
        text-align: center;
        margin-top: 50px;
        font-size: 2em;
        color: #2c3e50;
    }
    .section-title {
        font-size: 1.5em;
        margin-bottom: 10px;
        color: #00CFFF;
    }
    .house-form input, .house-form select {
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 1em;
    }
    .house-form button {
        width: 100%;
        padding: 12px;
        background-color: #00CFFF;
        border: none;
        color: white;
        font-size: 1.2em;
        border-radius: 5px;
        cursor: pointer;
    }
    .house-form button:hover {
        background-color: #008C9E;
    }
    .spinner {
        width: 50px;
        height: 50px;
        border: 5px solid #f3f3f3;
        border-top: 5px solid #00CFFF;
        border-radius: 50%;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
"""

# Home page
if sidebar_selection == "Home":
    st.markdown(html_code, unsafe_allow_html=True)  # Inject custom HTML and CSS
    st.image("D:/meme morse/Secret-Meme/eclectic_and_immersive_cyberpunk_living_space.jpg", use_container_width=True)
    st.markdown("### Welcome to the House Price Prediction App!")
    st.markdown("""
    This app helps you predict the price of a house based on various features such as size, number of rooms, and more.
    You can input your house features and get an estimated price, along with helpful tips for buying a house.
    """)
    st.write("### Navigate through the sidebar to get started!")

# House Price Predictor page
def predict_house_price(features):
    # Placeholder for actual prediction logic
    base_price = 50000
    price = base_price + (features['size'] * 100) + (features['rooms'] * 5000) - (features['age'] * 300)
    
    if features['location'] == 'Urban':
        price += 50000
    elif features['location'] == 'Suburban':
        price += 20000
    
    return max(price, 0)  # Ensure the price is not negative

if sidebar_selection == "House Price Predictor":
    st.markdown(html_code, unsafe_allow_html=True)  # Inject custom HTML and CSS
    with st.form(key='house_form', clear_on_submit=True):
        st.markdown("### Enter Your House Features")
        house_size = st.number_input("House Size (in square feet)", min_value=100, max_value=10000, step=10)
        num_rooms = st.number_input("Number of Rooms", min_value=1, max_value=10, step=1)
        house_age = st.number_input("House Age (in years)", min_value=1, max_value=100, step=1)
        house_location = st.selectbox("Location", ['Urban', 'Suburban', 'Rural'])
        submit_button = st.form_submit_button(label="Predict House Price")

        if submit_button:
            features = {
                'size': house_size,
                'rooms': num_rooms,
                'age': house_age,
                'location': house_location
            }
            predicted_price = predict_house_price(features)
            st.success(f"Estimated House Price: ${predicted_price:,.2f}")
    
    st.markdown("<div class='spinner'></div>", unsafe_allow_html=True)  # Spinner animation

# Reports page (Price Summary using user data)
elif sidebar_selection == "Reports":
    st.markdown(html_code, unsafe_allow_html=True)  # Inject custom HTML and CSS
    st.markdown("### House Price Summary Report")
    
    # Upload CSV file with house data
    uploaded_file = st.file_uploader("Upload Your House Data (CSV)", type="csv")
    
    if uploaded_file is not None:
        # Load the data into a pandas dataframe
        df = pd.read_csv(uploaded_file)

        # Check for necessary columns: Size, Rooms, Age, Location
        required_columns = ['size', 'rooms', 'age', 'location']
        if all(col in df.columns for col in required_columns):
            # Generate predictions for each house
            df['predicted_price'] = df.apply(lambda row: predict_house_price(row), axis=1)
            st.write(df)
            st.write("### Summary Statistics")
            st.write(df.describe())
            
            # Visualization
            st.write("### Price Distribution")
            fig, ax = plt.subplots()
            ax.hist(df['predicted_price'], bins=10, color='cyan', edgecolor='black')
            st.pyplot(fig)
        else:
            st.warning("The CSV file must contain the following columns: 'size', 'rooms', 'age', and 'location'.")
