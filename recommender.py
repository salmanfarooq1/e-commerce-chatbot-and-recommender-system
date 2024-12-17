import os
import requests
import sqlite3
import numpy as np
import pandas as pd
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

# Load the VGG16 model
vgg16_model = VGG16(weights="imagenet", include_top=False)

# Initialize SQLite database
def initialize_database():
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT UNIQUE,
            features BLOB
        )
    """)
    conn.commit()
    conn.close()

# Feature extraction function
def feature_extract(img):
    img_resized = cv2.resize(img, (224, 224))
    img_array = img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = vgg16_model.predict(img_array)
    return features.flatten()

# Store features and image URLs in the database
def store_features_to_db(img_url, features):
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO image_features (image_url, features)
            VALUES (?, ?)
        """, (img_url, features.tobytes()))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"URL already exists in the database: {img_url}")
    conn.close()

# Load features and URLs from the database
def load_features_from_db():
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()
    cursor.execute("SELECT image_url, features FROM image_features")
    data = cursor.fetchall()
    conn.close()

    image_urls = [row[0] for row in data]
    features_list = [np.frombuffer(row[1], dtype=np.float32) for row in data]
    return image_urls, features_list

# Process Shopify links and store features in the database
def process_and_store_images(image_source):
    # Read Shopify links from the CSV file
    df = pd.read_csv(image_source)
    image_urls = df["image_link"].tolist()

    for img_url in image_urls:
        try:
            # Download the image
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                # Extract features and store them
                features = feature_extract(img)
                store_features_to_db(img_url, features)
        except Exception as e:
            print(f"Failed to process image {img_url}: {e}")

# Find similar images
def find_similarity(input_image, features_list, image_urls):
    input_features = feature_extract(input_image)
    similarity_scores = []

    for idx, features in enumerate(features_list):
        score = cosine_similarity(input_features.reshape(1, -1), features.reshape(1, -1))[0][0]
        similarity_scores.append((image_urls[idx], score))

    # Sort by similarity score (descending)
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    return similarity_scores

# Main script for testing
if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Process and store image features
    process_and_store_images("image_links.csv")

    # Load features from the database
    image_urls, features_list = load_features_from_db()

    # Test with a new input image URL
    input_image_url = "https://cdn.shopify.com/s/files/1/0464/1731/3955/products/sample_image.jpg"
    response = requests.get(input_image_url, stream=True)
    if response.status_code == 200:
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        input_image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Find similar images
        similar_images = find_similarity(input_image, features_list, image_urls)

        # Print top 5 similar images
        print("Top 5 Similar Images:")
        for img_url, score in similar_images[:5]:
            print(f"{img_url} - Similarity Score: {score}")
