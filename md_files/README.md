# 📊 Stock Analysis Dashboard - AI Trading Signals

A Python-based stock analysis system using machine learning to predict stock prices.  
**Accuracy: 96.97% | Predictions: 5 levels | Data: 1.1M+ historical records**

---

## ⚡ Quick Start (5 Minutes)

### First Time Setup (One-time, ~20 minutes)

```bash
# 1. Open PowerShell in project folder and activate environment
cd C:\Users\SABIN\Desktop\Python-Project
.\pythonproject\Scripts\Activate.ps1

# 2. Initialize database (downloads 10 years of stock data)
python database.py              # Create database
python data/company_names.py      # Get list of 500 companies
python data/download_data.py      # Download historical prices (takes ~20 min)

# 3. Train AI model (takes ~3 minutes)
python models/model.py
```

✅ Done! Your system is ready.

### Daily Usage (Every Trading Day)

```bash
# 1. Activate environment
.\pythonproject\Scripts\Activate.ps1

# 2. Update latest prices
python data/daily_data.py

# 3. Start dashboard
streamlit run dashboard.py
```

Then open: **http://localhost:8501**

---

## 🎯 What This Does

**The AI Analyzes**:
- Price movements (current vs moving averages: 20, 50, 100, 200 days)
- Momentum (RSI indicator)  
- Trend direction
- Trading volume

**The AI Predicts** (One of 5 signals):

| Signal | Emoji | Meaning | Color |
|--------|-------|---------|-------|
| Strong Sell | 🔴 | Best time to SELL | Red |
| Weak Sell | 🔶 | Caution, maybe sell | Orange |
| Hold | 🟡 | No clear signal | Yellow |
| Weak Buy | 🟢 | Light buy signal | Light Green |
| Strong Buy | 🟢 | Best time to BUY | Green |

Each prediction includes **confidence percentage** (0-100%)

---

## 📁 Project Structure

```
Python-Project/
│
├── 🎨 dashboard.py                 ← START HERE (the web app)
├── 📋 README.md                    ← This file
├── 📚 WORKFLOW.md                  ← How it works (technical)
├── 💾 stock_data.db                ← Database (auto-created)
├── 📦 requirements.txt             ← Dependencies
│
├── 📁 data/                        ← Data processing
│   ├── __init__.py                 ← (required for Python)
│   ├── database.py                 ← Database operations
│   ├── indicators.py               ← Calculate indicators
│   ├── daily_data.py              ← Daily updates
│   ├── download_data.py           ← Download data (first time)
│   └── company_names.py           ← Company list (first time)
│
├── 📁 models/                      ← Machine learning
│   ├── model.py                    ← Training code
│   └── stock_model.pkl             ← Trained AI (auto-created)
│
└── 📁 log_files/                   ← Application logs
    ├── daily_sync.log
    └── download.log
```

---

## 🔧 Troubleshooting

### "Model not found" error

**Cause**: AI model hasn't been trained yet

**Fix**:
```bash
.\pythonproject\Scripts\Activate.ps1
python models/model.py
```

Wait 3 minutes for training to complete.

---

### No data appears in dashboard

**Cause**: Database is empty or outdated

**Fix**:
```bash
.\pythonproject\Scripts\Activate.ps1
python data/daily_data.py          # Updates with latest prices
```

---

### "Module not found" or import errors

**Cause**: Missing Python package marker

**Fix**: Ensure this file exists: `data/__init__.py`  
If missing, create empty file with that name in the `data` folder.

---

### Dashboard won't start / Port 8501 already in use

**Cause**: Another instance running

**Fix**:
```bash
streamlit run dashboard.py --logger.level=debug --server.port 8502
```

---

## 📊 Key Commands Reference

| Command | Purpose | Time |
|---------|---------|------|
| `python migrate_db.py` | Create database | < 1 min |
| `python data/company_names.py` | Get 500 companies | 2 min |
| `python data/download_data.py` | Download price history | 20 min |
| `python models/model.py` | Train AI model | 3 min |
| `python data/daily_data.py` | Update latest prices | 1 min |
| `streamlit run dashboard.py` | Start the app | instant |

---

## 📈 Model Performance

- **Accuracy**: 96.97% on 222,918 test samples
- **Training Data**: 1.1M+ historical trading days
- **Stocks Tracked**: 500 (S&P 500)
- **Prediction Classes**: 5 levels (Strong Sell → Strong Buy)

**Feature Importance** (What the AI trusts most):
1. MA200 distance (26.5%)
2. RSI14 momentum (21.6%)
3. MA20 distance (15.4%)
4. MA50 distance (13.8%)
5. MA100 distance (13.4%)
6. Trend direction (9.2%)
7. Trading volume (0.2%)

---

## 💡 Trading Tips

✅ **DO**:
- Use signals as a guide, not gospel
- Combine with your own analysis
- Check market news before trading
- Track accuracy over time
- Let the model learn (improve monthly)

❌ **DON'T**:
- Trade on ONLY AI signal
- Trade against major trends
- Ignore risk management
- Use single stock predictions
- Expect 100% accuracy always

---

## 📚 For Detailed Information

See **WORKFLOW.md** for:
- Complete system architecture
- How the AI model is trained
- Data pipeline explanation
- Performance metrics breakdown
- Next steps for improvement

---

## ✨ Features

✅ Real-time stock data (Yahoo Finance)  
✅ Technical indicators (MA20, MA50, MA100, MA200, RSI14)  
✅ AI predictions (96.97% accuracy)  
✅ Beautiful dark-themed dashboard  
✅ 5-level prediction system  
✅ Automatic daily updates  
✅ 1.1M+ training records  
✅ Easy to understand signals  

---

