import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

# -----------------------------
# Load Artifacts
# -----------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("../models/model.pkl")
    scaler = joblib.load("../models/scaler.pkl")
    columns = joblib.load("../models/columns.pkl")
    num_cols = joblib.load("../models/num_cols.pkl")
    return model, scaler, columns, num_cols


model, scaler, columns, num_cols = load_artifacts()

# -----------------------------
# UI
# -----------------------------
st.title("🏠 House Price Prediction")
st.markdown("Enter house details to predict price")

col1, col2 = st.columns(2)

with col1:
    GrLivArea = st.number_input("Living Area (sq ft)", 300, 5000, 1500)
    OverallQual = st.slider("Overall Quality (1-10)", 1, 10, 5)
    GarageCars = st.selectbox("Garage Capacity", [0, 1, 2, 3, 4])

with col2:
    TotalBsmtSF = st.number_input("Basement Area", 0, 3000, 800)
    FullBath = st.selectbox("Full Bathrooms", [0, 1, 2, 3])
    YearBuilt = st.number_input("Year Built", 1900, 2025, 2000)

# -----------------------------
# Create Input Data
# -----------------------------
def create_input_df():
    data = {
        "GrLivArea": GrLivArea,
        "OverallQual": OverallQual,
        "GarageCars": GarageCars,
        "TotalBsmtSF": TotalBsmtSF,
        "FullBath": FullBath,
        "YearBuilt": YearBuilt
    }

    df = pd.DataFrame([data])

    # 🔥 Align with training columns
    df = df.reindex(columns=columns, fill_value=0)

    return df


# -----------------------------
# Prediction Function
# -----------------------------
def predict(df):
    # 🔥 Scale ONLY numerical columns
    df[num_cols] = scaler.transform(df[num_cols])

    # Predict (log scale)
    pred_log = model.predict(df)

    # Convert back to actual price
    pred_price = np.expm1(pred_log)

    return pred_price[0]


# -----------------------------
# Button Action
# -----------------------------
if st.button("🔍 Predict Price"):
    try:
        input_df = create_input_df()
        prediction = predict(input_df)

        st.success(f"💰 Estimated Price: ${prediction:,.2f}")

    except Exception as e:
        st.error(f"❌ Error: {e}")


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("House Price Prediction | ML Project")
