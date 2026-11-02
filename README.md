# ⚡ Energy Consumption Prediction

Machine Learning Based Smart Energy Analytics System

---

## 📌 Project Overview

A web application that predicts energy consumption using a Linear Regression model trained on real-world energy data. Built with Flask and deployed on Vercel.

---

## 🛠️ Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Frontend   | HTML, CSS           |
| Backend    | Python, Flask       |
| ML Model   | scikit-learn (Linear Regression) |
| Deployment | Vercel              |

---

## 📁 Project Structure

```
energy-app/
├── api/
│   └── index.py          # Flask app — Vercel serverless handler
├── templates/
│   └── index.html        # Frontend UI
├── static/               # Static assets
├── model.pkl             # Trained ML model
├── Energy_consumption.csv# Dataset
├── requirements.txt      # Python dependencies
└── vercel.json           # Vercel deployment config
```

---

## 🚀 Deployment (Vercel)

### Step 1 — Push to GitHub
Upload all project files to a new GitHub repository.

### Step 2 — Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click **New Project**
3. Import your GitHub repository
4. Leave all settings as default
5. Click **Deploy**

Your app will be live in ~2 minutes.

---

## 🧠 Model Details

- **Algorithm:** Linear Regression
- **Accuracy:** 98.53% (R² Score)
- **Training Data:** `Energy_consumption.csv`

### Input Features

| Feature          | Type        |
|------------------|-------------|
| Temperature      | Numeric     |
| Humidity         | Numeric     |
| Square Footage   | Numeric     |
| Occupancy        | Numeric     |
| Renewable Energy | Numeric     |
| HVAC Usage       | On / Off    |
| Lighting Usage   | On / Off    |
| Day of Week      | Mon–Sun     |
| Holiday          | Yes / No    |

---

## 💻 Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/your-repo.git
cd energy-app

# Install dependencies
pip install -r requirements.txt

# Run the app
python api/index.py
```

Open `http://localhost:5000` in your browser.

---

## 👥 Team

- N. Vamshi Reddy
- R. Naresh
- S. Srikanth Reddy

---

## 📄 License

This project is for academic purposes.
