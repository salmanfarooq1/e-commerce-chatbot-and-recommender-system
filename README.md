# **E-Commerce Chatbot and Recommender System**

An integrated platform that combines an image-based recommender system and an intelligent chatbot to enhance the shopping experience for users. The recommender system finds similar images to a user-uploaded product, while the chatbot assists with general inquiries.

---

## **Features**
1. **Image-Based Recommender System**:
   - Users can upload an image of a product.
   - The system finds and displays visually similar products from the database.

2. **Intelligent Chatbot**:
   - A text-based chatbot that answers user queries about products, services, or the platform.

3. **Streamlit Integration**:
   - A user-friendly web interface built using Streamlit to seamlessly integrate both functionalities.

---

## **Technologies Used**
- **Backend**:
  - Python
  - TensorFlow (VGG16 for feature extraction)
  - SQLite for database
  - Scikit-learn for cosine similarity calculations
- **Frontend**:
  - Streamlit
- **Deployment**:
  - GitHub (for hosting the code repository)
  - Local or cloud server for running the app

---

## **Setup Instructions**

### 1. **Clone the Repository**
```bash
git clone https://github.com/salmanfarooq1/e-commerce-chatbot-and-recommender-system.git
cd e-commerce-chatbot-and-recommender-system
```

### 2. **Install Dependencies**
Create a virtual environment and install required packages:
```bash
pip install -r requirements.txt
```

### 3. **Prepare the Database**
- The recommender system uses a database (`features.db`) to store image features and URLs.
- If you don't have a prebuilt database, create one:
  1. Place images in a directory (e.g., `data/images/`).
  2. Run a feature extraction script to populate the database. Example script:
     ```bash
     python feature_extraction.py
     ```
  3. Ensure images are accessible via URLs or file paths for Streamlit.

### 4. **Run the Streamlit App**
Start the app locally:
```bash
streamlit run streamlit_app.py
```
The app will launch in your default browser at `http://localhost:8501`.

---

## **Usage**

### **Recommender System**
1. Navigate to the **"Find Similar Images"** tab.
2. Upload an image (JPG/PNG format).
3. View the top 5 visually similar products with their similarity scores.

### **Chatbot**
1. Navigate to the **"Chat with Assistant"** tab.
2. Type your query in the input box.
3. Get an intelligent response from the chatbot.

---

## **Important Considerations**
1. **Database**:
   - Ensure `features.db` is in the project root directory.
   - Images must be accessible via URLs or local paths.
   
2. **Image Dataset**:
   - If you don’t have an existing dataset, upload a collection of product images into a folder (e.g., `data/images/`).
   - Update the database by running the feature extraction script.

3. **Dependencies**:
   - Ensure all dependencies listed in `requirements.txt` are installed.
   - Use Python 3.8+ for compatibility.

4. **Hardware Requirements**:
   - For feature extraction, a GPU is recommended but not mandatory.
   - The recommender system and chatbot can run on a typical CPU.

5. **Environment Variables**:
   - If external APIs are used (e.g., for chatbot integration), configure API keys in an `.env` file and load them using `python-dotenv`.

---

## **Contributing**
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Contact**
For any queries, feel free to reach out:
- **Author**: Salman Farooq
- **Email**: [Your Email Address]
- **GitHub**: [https://github.com/salmanfarooq1](https://github.com/salmanfarooq1)

