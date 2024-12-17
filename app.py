import streamlit as st
from recommender import find_similarity, load_features_from_db, feature_extract
from chatbot import Chatbot
import requests
import numpy as np
import cv2

# Initialize chatbot
try:
    chatbot = Chatbot()
except ConnectionError:
    st.error("Ollama server is not running. Please start the server and restart the app.")
    chatbot = None

# Load features and image URLs from the database
image_urls, features_list = load_features_from_db()

# Streamlit app layout
st.title("E-Commerce Assistant")
st.sidebar.title("Options")

# Sidebar navigation
app_mode = st.sidebar.radio(
    "Choose a feature",
    ("Chatbot", "Image Recommender")
)

# Chatbot feature
if app_mode == "Chatbot":
    st.header("Chat with AI")
    st.write("Type a question to get started!")

    user_input = st.text_input("You:", placeholder="Ask me something...")
    if st.button("Send"):
        if not chatbot:
            st.error("Chatbot is unavailable. Please start the Ollama server.")
        elif user_input.strip():
            response = chatbot.send_message(user_input)
            st.text_area("Chatbot:", value=response, height=200)

    if st.button("Reset Conversation"):
        chatbot.reset_conversation()
        st.success("Conversation reset successfully!")

# Image Recommender feature
elif app_mode == "Image Recommender":
    st.header("Find Similar Images")
    st.write("Upload an image to find visually similar images.")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        # Convert uploaded file to OpenCV format
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        input_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Display uploaded image
        st.image(input_image, channels="BGR", caption="Uploaded Image")

        # Find similar images
        with st.spinner("Finding similar images..."):
            similar_images = find_similarity(input_image, features_list, image_urls)

        st.subheader("Top 5 Similar Images:")
        for idx, (url, score) in enumerate(similar_images[:5], start=1):
            st.markdown(f"**{idx}. Similarity Score: {score:.2f}**")
            st.image(url, caption=f"Image {idx}", use_column_width=True)
