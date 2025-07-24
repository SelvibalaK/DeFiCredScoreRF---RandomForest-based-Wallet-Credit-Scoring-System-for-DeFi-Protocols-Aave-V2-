# DeFiCredScoreRF---RandomForest-based-Wallet-Credit-Scoring-System-for-DeFi-Protocols-Aave-V2-

This project aims to assign a **credit score (0–1000)** to DeFi wallets based on their historical transaction behavior with the **Aave V2 protocol**. The goal is to identify trustworthy vs risky wallet behavior using both **rule-based logic** and a **machine learning model**.

---

## 🔍 Problem Statement

- Provided with 100K+ raw Aave V2 transactions in JSON format
- Each transaction includes actions like `deposit`, `borrow`, `repay`, `redeemunderlying`, `liquidationcall`
- Objective: Build a robust scoring system that evaluates wallet behavior and assigns a **score between 0 and 1000**

---

## 🚀 Solution Overview

### 1. Data Parsing & Feature Engineering
We extracted wallet-level behavioral metrics from raw JSON:

| Feature | Purpose |
|--------|---------|
| `repay_ratio` | Measures repayment responsibility |
| `total_borrow`, `total_repay` | Tracks credit usage & returns |
| `total_liquidations` | Flags financial risk |
| `days_active` | Wallet activity consistency |
| `deposit_redeem_ratio` | Detects suspicious loops |
| `unique_actions` | Helps identify bots or inactive users |

---

### 2. Rule-Based Scoring Logic

Each wallet starts with a base score of 500. Based on behavior:
- High `repay_ratio` = score boost
- Liquidations or bot-like behavior = score penalty
- Active, diverse, and long-term users are rewarded

> Final rule-based scores are stored in `wallet_scores.csv`

---

### 3. Machine Learning Model (Random Forest)

To strengthen the scoring system:
- We used the rule-based scores as **pseudo-labels**
- Trained a `RandomForestRegressor` on wallet features
- Achieved **R² = 0.9919** proving our scoring logic was learnable

> Feature importances confirmed that **`repay_ratio`, `days_active`, and `liquidation_count`** are most critical

---

## 📂 Project Structure
├── user_transactions.json # (Not uploaded - large file)
├── generate_scores.py # 💡 One-step script: JSON ➝ Features ➝ Scores
├── train_ml_model.py # Train RF model on features + scores
├── wallet_features.csv # Extracted wallet behavior
├── wallet_scores.csv # Final scores per wallet
├── score_distribution.png # Score histogram
├── feature_importance.png # Random Forest feature importance
├── score_band_summary.csv # Analysis of wallet behavior by score band
├── README.md
├── analysis.md
└── requirements.txt

---

## ▶️ How to Run

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the one-step scoring pipeline
```bash
python generate_scores.py
```

This will:
- Load the raw JSON
- Extract wallet behavior features
- Apply rule-based scoring
- Save wallet_scores.csv for submission or modeling

## 🧠 Insights

- High-scoring wallets show consistent, long-term, responsible activity with full loan repayments
- Low-scoring wallets exhibit signs of botting, risky borrowing, or liquidation
- repay_ratio is the most dominant signal of financial health in DeFi

---

## 📊 ML Model Summary
|  Metric  |	Value  |
|--------|---------|
|  Model  |  Random Forest Regressor  |
|  MSE  |  287.12  |
|  R²  |  0.9919  |
|  Top Features  |  `repay_ratio`, `days_active`, `total_liquidations`  |

---

## 📌 Authors
## Selvibala K
