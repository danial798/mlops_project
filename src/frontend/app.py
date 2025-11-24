import streamlit as st
import requests
import os

# API endpoint configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Wine Quality Predictor",
    page_icon="🍷",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #8B0000;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #A52A2A;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍷 Wine Quality Prediction System")
st.markdown("### Predict wine quality based on physicochemical properties")

# Check API health
try:
    health_response = requests.get(f"{API_URL}/health", timeout=5)
    if health_response.status_code == 200:
        health_data = health_response.json()
        if health_data.get("model_loaded"):
            st.success("✅ API is healthy and model is loaded")
        else:
            st.warning("⚠️ API is running but model is not loaded")
    else:
        st.error("❌ API health check failed")
except Exception as e:
    st.error(f"❌ Cannot connect to API: {str(e)}")
    st.info(f"Make sure the API is running at {API_URL}")

st.markdown("---")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Acidity & Chemical Properties")
    fixed_acidity = st.number_input("Fixed Acidity", min_value=0.0, max_value=20.0, value=7.4, step=0.1)
    volatile_acidity = st.number_input("Volatile Acidity", min_value=0.0, max_value=2.0, value=0.7, step=0.01)
    citric_acid = st.number_input("Citric Acid", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
    residual_sugar = st.number_input("Residual Sugar", min_value=0.0, max_value=20.0, value=1.9, step=0.1)
    chlorides = st.number_input("Chlorides", min_value=0.0, max_value=1.0, value=0.076, step=0.001)
    pH = st.number_input("pH", min_value=0.0, max_value=14.0, value=3.51, step=0.01)

with col2:
    st.subheader("Sulfur Dioxide & Other Properties")
    free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", min_value=0.0, max_value=100.0, value=11.0, step=1.0)
    total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", min_value=0.0, max_value=300.0, value=34.0, step=1.0)
    density = st.number_input("Density", min_value=0.0, max_value=2.0, value=0.9978, step=0.0001, format="%.4f")
    sulphates = st.number_input("Sulphates", min_value=0.0, max_value=2.0, value=0.56, step=0.01)
    alcohol = st.number_input("Alcohol (%)", min_value=0.0, max_value=20.0, value=9.4, step=0.1)

st.markdown("---")

# Predict button
if st.button("🔮 Predict Wine Quality"):
    # Prepare input data
    input_data = {
        "fixed_acidity": fixed_acidity,
        "volatile_acidity": volatile_acidity,
        "citric_acid": citric_acid,
        "residual_sugar": residual_sugar,
        "chlorides": chlorides,
        "free_sulfur_dioxide": free_sulfur_dioxide,
        "total_sulfur_dioxide": total_sulfur_dioxide,
        "density": density,
        "pH": pH,
        "sulphates": sulphates,
        "alcohol": alcohol
    }
    
    try:
        with st.spinner("Making prediction..."):
            response = requests.post(f"{API_URL}/predict", json=input_data, timeout=10)
        
        if response.status_code == 200:
            prediction = response.json()["quality_prediction"]
            
            # Display prediction with styling
            st.markdown(f"""
                <div class="prediction-box">
                    <h2>Predicted Wine Quality</h2>
                    <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction:.2f}</h1>
                    <p style="font-size: 1.2rem;">Quality Score (0-10 scale)</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Quality interpretation
            if prediction >= 7:
                st.success("🌟 Excellent quality wine!")
            elif prediction >= 6:
                st.info("👍 Good quality wine")
            elif prediction >= 5:
                st.warning("😐 Average quality wine")
            else:
                st.error("👎 Below average quality wine")
        else:
            st.error(f"Prediction failed: {response.text}")
    
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Built with FastAPI + Streamlit | MLOps Pipeline Demo</p>
    </div>
""", unsafe_allow_html=True)
