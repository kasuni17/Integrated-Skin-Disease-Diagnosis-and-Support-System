# Integrated Skin Disease Diagnosis and Support System

A web-based application that uses AI to help users identify skin diseases through image analysis. The system provides instant predictions, educational content, and expert consultation support, making dermatological care more accessible.

## Features

- **AI-Powered Skin Disease Detection**: Upload an image of a skin condition and get an instant prediction using a trained Convolutional Neural Network (CNN) model.
- **Educational Content**: Access detailed information about predicted conditions, including causes, symptoms, prevention, and home remedies.
- **Expert Consultation**: Connect with board-certified dermatologists for professional diagnosis confirmation and treatment recommendations.
- **Interactive Chatbot**: Get real-time answers to general skin-related questions and navigation support.
- **User Account Management**: Maintain a personal history of past diagnoses and track your skin health over time.
- **Cross-Platform Accessibility**: Use the system on any modern web browser, including mobile devices.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI Model**: TensorFlow, Keras, MobileNetV3
- **Chatbot**: DeepSeek API
- **Security**: Hashlib (SHA-256) for password encryption

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kasuni17/Integrated-Skin-Disease-Diagnosis-and-Support-System.git
   cd Integrated-Skin-Disease-Diagnosis-and-Support-System
   ```

2. **Create a Virtual Environment (recommended)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure Environment Variables**
   - Create a `.env` file in the project root or set system environment variables:
     ```bash
     # required if you use the chatbot
     DEEPSEEK_API_KEY=your_api_key_here
     ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**
   Open your web browser and go to `http://localhost:8501`.

## Usage

1. **Register/Login**: Create an account or log in to access all features.
2. **Upload an Image**: Navigate to the **Disease Identification** page and upload an image of the skin condition.
3. **View Prediction**: The AI model will analyze the image and display the predicted disease along with a confidence score.
4. **Explore Educational Content**: Click on **Learn More** to access detailed information and YouTube tutorials about the predicted condition.
5. **Chat with the Bot**: Use the chatbot for general questions and guidance.
6. **Contact an Expert**: Submit a query to a dermatologist for professional advice.
7. **View History**: Check your past predictions and expert responses in the **Records** section.

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── database.py            # Database initialization and operations
├── auth.py                # User authentication functions
├── model_loader.py        # AI model loading and prediction
├── chatbot.py             # Chatbot integration with DeepSeek API
├── expert.py              # Expert query handling
├── records.py             # User diagnosis history management
├── test/                  # Unit tests
├── static/                # Static files (images, etc.)
└── README.md              # Project documentation (this file)
```

## Testing

To run the unit tests:

```bash
pytest test/
```


## Contact

For questions or support, please contact:
- Email: kasuniik417@gmail.com
- GitHub: [kasuni17](https://github.com/kasuni17)

