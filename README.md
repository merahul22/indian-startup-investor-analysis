﻿# indian-startup-investor-analysis

# 🚀 Startup Funding Analysis Dashboard

A Streamlit-based interactive web application for visualizing and analyzing startup funding data in India. This dashboard enables users to explore investment trends, top investors, startups, sectors, and more.

---

## 📊 Features

### ✅ Overall Analysis
- Total funding, average funding, and number of funded startups
- Month-on-Month (MoM) trend: Total Funding / Funding Count
- Sector-wise and City-wise analysis
- Top funding rounds and types
- Funding Heatmap (Year vs Month)
- Top startups by year
- Top 10 investors overall

### 🧑‍💼 Investor Analysis
- View all investments made by a selected investor
- Breakdown of sectors, cities, and funding stages they invested in
- Year-over-Year investment trends
- Similar investors based on city

### 🏢 Startup Analysis (Company POV)
- Founders, Industry, Subindustry, Location
- Funding rounds, Stages, Total investment
- All investment rounds and dates
- Similar companies in same industry and location

---

## 📁 Folder Structure

```

📦Startup-Funding-Analysis
┣ 📄 startup\_cleaned.csv
┣ 📄 app.py
┗ 📄 README.md

````

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/startup-funding-analysis.git
cd startup-funding-analysis
````

2. **Install dependencies**

Make sure you have Python 3.8+ and install required packages:

```bash
pip install -r requirements.txt
```

> Or manually:

```bash
pip install streamlit pandas matplotlib
```

3. **Run the app**

```bash
streamlit run app.py
```

4. **Open in browser**
   The app will open at `http://localhost:8501`

---

## 📌 Dependencies

* `pandas` – Data cleaning & manipulation
* `matplotlib` – Chart plotting
* `streamlit` – Web UI and interactivity

---

## 📬 Dataset Info

* File: `startup_cleaned.csv`
* Columns expected: `startup`, `date`, `amount`, `round`, `vertical`, `city`, `investors`, `founders`, `subvertical`, `stage` *(optional)*

---

## 🛠 Future Improvements

* Search and filter by funding range or startup category
* Upload your own dataset
* Export charts as images/PDFs
* Add login/dashboard for custom tracking

---

## 🙌 Credits

This project is built using:

* Streamlit for UI
* Matplotlib for plotting
* Pandas for data wrangling
* kaggle for dataset 

---







