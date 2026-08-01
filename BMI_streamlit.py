from google import genai
import streamlit as st

st.title("💪 BMI Calculator with AI Nutritionist")

Client = genai.Client(api_key=st.secrets["api_key"] )

# User Inputs for Weight and Height
wt = st.number_input("Enter your weight in kilograms (kg):", min_value=1.0, value=70.0)
ht = st.number_input("Enter your height in meters (m):", min_value=0.5, value=1.75)

# Calculate BMI button
if st.button("Calculate BMI & Get AI Advice"):
  if not google_api_key:
    st.error("Please enter your Google API Key in the sidebar first!")
  else:
    # Calculate BMI
    bmi = wt / (ht**2)

    # Display results
    st.subheader("Results")
    st.write(f"Your calculated BMI is: **{bmi:.2f}**")

    # Determine BMI category
    if bmi < 18.5:
      category = "Underweight"
    elif 18.5 <= bmi < 25:
      category = "Normal weight"
    elif 25 <= bmi < 30:
      category = "Overweight"
    else:
      category = "Obese"

    st.info(f"Category: **{category}**")

    # Connect to Google GenAI and get AI recommendations
    try:
      client = genai.Client(api_key=google_api_key)

      prompt = (
          f"My weight is {wt} kg and my height is {ht} m, giving a BMI of"
          f" {bmi:.2f} ({category}). Act as an expert nutritionist and give"
          " me 3 short, personalized dietary and health recommendations."
      )

      with st.spinner("Consulting AI Nutritionist..."):
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        st.subheader("🥗 AI Nutritionist Advice")
        st.write(response.text)

    except Exception as e:
      st.error(f"An error occurred with the Google API: {e}")