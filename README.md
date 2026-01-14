# CGPA Calculator

A Streamlit web application to calculate GPA and CGPA for students.

## Features

- Add multiple subjects with grade points and credits
- Dynamic subject management (add/remove subjects)
- Calculate current semester GPA
- Calculate overall CGPA using previous academic record
- Grade classification system
- Responsive design

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your repository
5. Set the main file path as `app.py`

## Usage

1. Enter your previous CGPA and total credits in the sidebar
2. Add current semester subjects with grades and credits
3. View calculated GPA and CGPA in real-time

## Grade Point Scale

- A+ = 10.0
- A = 9.0
- B+ = 8.0
- B = 7.0
- C+ = 6.0
- C = 5.0
- D = 4.0
- F = 0.0
