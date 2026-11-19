# 💳 Credit Card Expiry Checker

A computer vision application that uses **OpenCV, Tesseract OCR, Regex, and Streamlit** to detect card expiry dates from uploaded images and determine whether a card is expired or still valid.

## 🚀 Project Overview

The application processes card images, extracts text using Optical Character Recognition (OCR), identifies expiry dates using Regular Expressions, and compares the detected date with the current date to determine the expiry status.

## ✨ Features

- Upload card images in JPG, JPEG, PNG, and WebP formats
- OCR-based text extraction using Tesseract
- Image preprocessing to improve text recognition
- Expiry date detection using Regex
- Expiry status classification
- Bounding-box annotation around detected expiry dates
- Manual expiry-date correction
- Interactive Streamlit interface
- Multiple image processing techniques for OCR improvement

## 🛠️ Technologies Used

- Python
- OpenCV
- Tesseract OCR
- Pytesseract
- NumPy
- Regular Expressions
- Streamlit

## ⚙️ Workflow

1. Upload a card image.
2. Process the image using OpenCV.
3. Apply multiple preprocessing techniques.
4. Extract text using Tesseract OCR.
5. Detect expiry-date patterns using Regex.
6. Compare the expiry date with the current date.
7. Display the expiry status and annotated image.

## 📂 Project Structure

```text
Credit-Card-Expiry-Checker/
├── app.py
├── detect.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Credit-Card-Expiry-Checker.git
cd Credit-Card-Expiry-Checker
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

Tesseract OCR must be installed separately on your system.

On Windows, configure the Tesseract executable path in `app.py` if necessary.

### 4. Run the application

```bash
streamlit run app.py
```

## 🔍 How It Works

The application uses OCR to extract text from card images and Regex to identify expiry-date patterns such as MM/YY and MM/YYYY. The extracted month and year are then compared with the current date to determine whether the expiry month has passed.

## ⚠️ Disclaimer

This project is intended for educational and demonstration purposes only. Use synthetic or test card images. Do not upload, store, or process real payment-card information or sensitive financial data.

## 👨‍💻 Author

Mohanakrishnan M.

GitHub: [mhn-alt](https://github.com/mhn-alt)
