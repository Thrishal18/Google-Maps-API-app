import streamlit as st
import os
import googlemaps
from dotenv import load_dotenv
from bs4 import BeautifulSoup


# Load environment variables from .envile
load_dotenv()
from bs4 import BeautifulSoup
# --- FUNCTIONS ---
def get_directions(api_key, origin, destination):
    """Fetches directions from Google Maps API and returns results."""
    try:
        gmaps = googlemaps.Client(key=api_key)
        directions_result = gmaps.directions(origin,destination,mode="driving" )
        
        if directions_result:
            return directions_result
        else:
            return None
    except Exception as e:
        # Handle potential API errors, like invalid key or request issues
        st.error(f"An error occurred with the Google Maps API: {e}")
        return None

# --- STREAMLIT APP ---

# Set the title of the web app
st.title("📍 Google Maps Route Planner")

# Load the API key from environment variables
api_key = os.getenv("GOOGLE_MAPS_API")
password = os.getenv("password")

# Check if the API key is available
if not api_key:
    st.error("🔴 Error: GOOGLE_MAPS_API key not found.")
    st.info("Please make sure you have a .env file with your API key defined.")
else:
    # Create text input fields for the user
    login_password = st.text_input("Enter password to run")
    origin = st.text_input("Enter Origin Address:", "Guntur, Andhra Pradesh")
    destination = st.text_input("Enter Destination Address:")

    # Create a button to trigger the directions search
    if st.button("Get Directions"):
        # Validate that both fields have input
        if origin and destination and login_password==password:
            with st.spinner("Finding the best route..."):
                directions = get_directions(api_key, origin, destination)

            if directions:
                st.success("✅ Route found!")
                
                # Extract the first leg of the journey
                leg = directions[0]['legs'][0]
                
                # Display high-level results in columns
                col1, col2 = st.columns(2)
                col1.metric("Total Distance", leg['distance']['text'])
                col2.metric("Estimated Duration", leg['duration']['text'])

                st.info("Directions :")
                # Display the steps of the journey
                for i, step in enumerate(leg['steps'][:]):
                    html_instruction = step['html_instructions']
                    soup = BeautifulSoup(html_instruction, "html.parser")
                    plain_text_instruction = soup.get_text(separator=' ', strip=True)
                    # --- MODIFICATION END ---
                    
                    # Display the cleaned, plain text instruction
                    st.markdown(f"**{i+1}.** {plain_text_instruction} `({step['distance']['text']})`")
            else:
                st.error("Could not find a route. Please check your addresses.")
        else:

            st.warning("Please enter correct password and include origin and a destination.")
