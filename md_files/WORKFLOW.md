# 🔄 System Workflow - Technical Deep Dive

Complete explanation of how the stock analysis system works.

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        👤 USER                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
           ┌─────────────────────────────────┐
           │   📱 STREAMLIT DASHBOARD        │
           │  (dashboard.py)                 │
           │                                 │
           │  ▪ Stock selector               │
           │  ▪ Price charts                 │
           │  ▪ AI predictions               │
           │  ▪ Technical indicators         │
           └────────────┬────────────────────┘
                        │ Requests prediction
                        ▼
           ┌─────────────────────────────────┐
           │   🤖 AI MODEL (Prediction)      │
           │  (models/stock_model.pkl)       │
           │                                 │
           │  Random Forest Classifier       │
           │  - 200 decision trees           │
           │  - 96.97% accuracy              │
           │  - Outputs: 5 signals           │
           └────────────┬────────────────────┘
                        │ Asks for features
                        ▼
           ┌─────────────────────────────────┐
           │  📊 INDICATORS CALCULATOR       │
           │  (indicators.py)                │
           │                                 │
           │  Calculates 7 features:         │
           │  ▪ Distance to MA20             │
           │  ▪ Distance to MA50             │
           │  ▪ Distance to MA100            │
           │  ▪ Distance to MA200            │
           │  ▪ RSI14 momentum               │
           │  ▪ MA trend direction           │
           │  ▪ Normalized volume            │
           └────────────┬────────────────────┘
                        │ Requests data
                        ▼
           ┌─────────────────────────────────┐
           │    💾 SQLITE DATABASE           │
           │  (stock_data.db)                │
           │                                 │
           │  3 tables:                      │
           │  ▪ companies (name, sector)     │
           │  ▪ daily_prices (OHLCV)         │
           │  ▪ technical_indicators (MA+RSI)│
           └────────────┬──────┬──────────────┘
                        │      │
          ┌─────────────┤      ├──────────────┐
          │             │      │              │
          ▼             ▼      ▼              ▼
    📥 YAHOO         📅 DAILY    📚 HISTORICAL 📋 COMPANY
    FINANCE         UPDATE      DOWNLOAD      LIST
    API             (daily_     (download_    (company_
                    data.py)    data.py)      names.py)
```

---

## 🔄 Daily Workflow

### Morning (Before Market Opens)

```
9:00 AM - User runs:
│
│ python data/daily_data.py
│
├─→ Connects to Yahoo Finance API
│   └─→ Downloads yesterday's closing price
│
├─→ Cleans invalid data
│   └─→ Removes errors, fills gaps
│
├─→ Calculates indicators
│   ├─→ Moving averages (MA20, 50, 100, 200)
│   ├─→ RSI14 momentum
│   └─→ Volume normalized
│
└─→ Stores in database
    └─→ stock_data.db updated
    
⏰ Takes: 1-2 minutes
```

### During Market Hours

```
9:30 AM - User runs:
│
│ streamlit run dashboard.py
│
├─→ Dashboard loads
│   ├─→ Reads from database
│   ├─→ Displays price chart
│   └─→ Shows indicators
│
├─→ User selects stock
│   ├─→ Queries database
│   ├─→ Gets latest data
│   └─→ Calls AI model
│
├─→ AI Model Predicts:
│   ├─→ Gets 7 features from calculator
│   ├─→ Processes through 200 decision trees
│   ├─→ Produces 5 predictions (probabilities)
│   ├─→ Outputs strongest signal + confidence
│   └─→ Returns result to dashboard
│
└─→ Dashboard displays:
    ├─→ Signal color (🔴 🔶 🟡 🟢)
    ├─→ Confidence (0-100%)
    └─→ Charts updated

⏰ Response time: < 2 seconds
```

---

## 🧠 AI Model Training Process

### Training Workflow

```
Step 1: Data Preparation
│
├─→ Query database (1.1M+ records)
│
├─→ Create features (engineers 7 indicators):
│   ├─→ Distance to MA20 = (Price - MA20) / MA20
│   ├─→ Distance to MA50 = (Price - MA50) / MA50
│   ├─→ Distance to MA100 = (Price - MA100) / MA100
│   ├─→ Distance to MA200 = (Price - MA200) / MA200
│   ├─→ RSI14 momentum (0-100)
│   ├─→ MA Trend = (MA20 - MA100) / MA100
│   └─→ Volume normalized = Volume / MA(Volume)
│
└─→ Create target labels (5 classes):
    ├─→ Strong Sell (-2): RSI < 30 AND price below all MAs
    ├─→ Weak Sell (-1): RSI 30-50 OR price below MA50
    ├─→ Hold (0): Mixed signals
    ├─→ Weak Buy (1): RSI 50-70 OR price above MA50
    └─→ Strong Buy (2): RSI > 70 AND price above all MAs

Step 2: Model Training
│
├─→ Split data: 80% training, 20% testing
│   └─→ 884,734 training samples
│   └─→ 221,183 test samples
│
├─→ Train Random Forest:
│   ├─→ Trees: 200
│   ├─→ Max depth: 15
│   ├─→ Class weights: balanced (handles imbalance)
│   └─→ Process time: ~3 minutes
│
└─→ Save model: models/stock_model.pkl (~2MB)

Step 3: Model Validation
│
├─→ Test on 221,183 unseen samples
│
├─→ Accuracy: 96.97% ✅
│
├─→ Per-class performance:
│   ├─→ Strong Sell: Recall 99%, Precision 72%
│   ├─→ Weak Sell: Recall 95%, Precision 99%
│   ├─→ Hold: Recall 99%, Precision 98%
│   ├─→ Weak Buy: Recall 97%, Precision 100%
│   └─→ Strong Buy: Recall 100%, Precision 85%
│
└─→ Feature importance:
    ├─→ MA200 distance: 26.5% (most important)
    ├─→ RSI14: 21.6%
    ├─→ MA20 distance: 15.4%
    ├─→ MA50 distance: 13.8%
    ├─→ MA100 distance: 13.4%
    ├─→ MA Trend: 9.2%
    └─→ Volume: 0.2%

When to retrain?
├─→ After 30 days of new data
├─→ When accuracy drops below 95%
├─→ When market conditions change significantly
└─→ Command: python models/model.py
```

---

## 🎯 Prediction Process (Real-time)

### What Happens When User Selects a Stock

```
User selects: Apple (AAPL)
│
├─→ Dashboard queries database:
│   │
│   └─→ Gets latest record:
│        ├─→ Date: 2026-03-28
│        ├─→ Price: $185.50
│        ├─→ MA20: $183.20
│        ├─→ MA50: $181.40
│        ├─→ MA100: $179.50
│        ├─→ MA200: $178.30
│        ├─→ RSI14: 72
│        ├─→ Volume: 52M
│        └─→ Volume_MA: 45M
│
├─→ Feature Engineer (in code):
│   │
│   ├─→ dist_ma20 = (185.50 - 183.20) / 183.20 = 0.0125
│   ├─→ dist_ma50 = (185.50 - 181.40) / 181.40 = 0.0226
│   ├─→ dist_ma100 = (185.50 - 179.50) / 179.50 = 0.0334
│   ├─→ dist_ma200 = (185.50 - 178.30) / 178.30 = 0.0402
│   ├─→ rsi14 = 72
│   ├─→ ma_trend = (183.20 - 179.50) / 179.50 = 0.0206
│   └─→ vol_normalized = 52M / 45M = 1.156
│
├─→ Load AI model:
│   │
│   └─→ models/stock_model.pkl loaded into memory
│
├─→ Make prediction:
│   │
│   ├─→ Features array: [0.0125, 0.0226, 0.0334, 0.0402, 72, 0.0206, 1.156]
│   │
│   ├─→ 200 Decision Trees vote:
│   │   ├─→ Tree 1: "Strong Buy" ✓
│   │   ├─→ Tree 2: "Strong Buy" ✓
│   │   ├─→ Tree 3: "Weak Buy" (majority: Strong Buy wins)
│   │   ├─→ ... (all 200 trees vote)
│   │   └─→ Majority consensus: STRONG BUY
│   │
│   ├─→ Calculate confidence:
│   │   └─→ Probs: [1%, 2%, 5%, 15%, 77%]
│   │   └─→ Max prob: 77% ← This is confidence
│   │
│   └─→ Map to signal:
│       ├─→ Prediction: 2 (Strong Buy)
│       ├─→ Emoji: 🟢
│       ├─→ Color: Green
│       ├─→ Label: "Strong Buy"
│       └─→ Confidence: 77%
│
├─→ Dashboard Renders:
│   │
│   ├─→ Display price chart (with MAs)
│   ├─→ Show indicators
│   ├─→ Highlight prediction:
│   │   │
│   │   └─→ 🟢 STRONG BUY
│   │       Confidence: 77%
│   │
│   ├─→ Show metrics:
│   │   ├─→ Price: $185.50
│   │   ├─→ MA200: $178.30 (+4.0%)
│   │   └─→ RSI: 72 (strong momentum)
│   │
│   └─→ Recommendation:
│       └─→ "Consider buying"
│
└─→ Total time: ~1.5 seconds

User sees the result on screen ✨
```

---

## 📊 Database Schema

### Table 1: companies
```
┌────────────────────────────────┐
│ companies                      │
├────────────────────────────────┤
│ symbol (TEXT, PK)  | "AAPL"   │
│ name (TEXT)        | "Apple"  │
│ sector (TEXT)      | "Tech"   │
└────────────────────────────────┘
```

### Table 2: daily_prices
```
┌─────────────────────────────────────────────┐
│ daily_prices                                │
├─────────────────────────────────────────────┤
│ id (INT, PK)        | 1                    │
│ symbol (TEXT, FK)   | "AAPL"               │
│ date (DATE)         | 2026-03-28           │
│ open (FLOAT)        | 180.50               │
│ high (FLOAT)        | 186.20               │
│ low (FLOAT)         | 180.30               │
│ close (FLOAT)       | 185.50               │
│ volume (INT)        | 52000000             │
└─────────────────────────────────────────────┘
```

### Table 3: technical_indicators
```
┌────────────────────────────────────────────────────────┐
│ technical_indicators                                   │
├────────────────────────────────────────────────────────┤
│ id (INT, PK)        | 1                               │
│ symbol (TEXT, FK)   | "AAPL"                          │
│ date (DATE)         | 2026-03-28                      │
│ ma20 (FLOAT)        | 183.20  (20-day moving avg)    │
│ ma50 (FLOAT)        | 181.40  (50-day moving avg)    │
│ ma100 (FLOAT)       | 179.50  (100-day moving avg)   │
│ ma200 (FLOAT)       | 178.30  (200-day moving avg)   │
│ rsi14 (FLOAT)       | 72.0    (14-day RSI)           │
│ volume_ma (FLOAT)   | 45000000 (volume moving avg)   │
└────────────────────────────────────────────────────────┘
```

---

## 📈 Data Flow - First Time Setup

```
Step 1: Initialize Database
│
└─→ python migrate_db.py
    │
    ├─→ Creates stock_data.db
    ├─→ Creates 3 tables (companies, daily_prices, technical_indicators)
    └─→ Sets up structure

Step 2: Get Company Names
│
└─→ python data/company_names.py
    │
    ├─→ Connects to Wikipedia
    ├─→ Downloads S&P 500 list (~500 companies)
    └─→ Stores in 'companies' table

Step 3: Download Historical Data
│
└─→ python data/download_data.py
    │
    ├─→ For each company:
    │   │
    │   ├─→ Query Yahoo Finance API
    │   ├─→ Download 5 years of daily prices (~1,260 records/company)
    │   ├─→ Store in 'daily_prices' table
    │   └─→ **PROGRESS**: Shows company count
    │
    ├─→ Total records: ~500 companies × 1,260 days = 630,000 initial records
    │
    └─→ Time: ~20 minutes (API rate-limited)

Step 4: Calculate Indicators (Automatic)
│
└─→ python data/indicators.py (runs automatically)
    │
    ├─→ For each price record:
    │   │
    │   ├─→ Calculate MA20 (20-day moving average)
    │   ├─→ Calculate MA50
    │   ├─→ Calculate MA100
    │   ├─→ Calculate MA200
    │   ├─→ Calculate RSI14 (momentum)
    │   └─→ Calculate volume moving average
    │
    └─→ Stores in 'technical_indicators' table

Step 5: Train AI Model
│
└─→ python models/model.py
    │
    ├─→ Queries all 630,000+ records
    ├─→ Engineers 7 features for each record
    ├─→ Creates target labels (5 classes)
    ├─→ Trains Random Forest (200 trees)
    ├─→ Tests on held-out data
    ├─→ Saves as models/stock_model.pkl
    │
    └─→ Result: 96.97% accuracy

Step 6: Ready to Use
│
└─→ python data/daily_data.py (updates latest)
└─→ streamlit run dashboard.py (start app)
```

---

## 🔄 Daily Update Flow

```
Every Evening (After Market Close 4:00 PM):

python data/daily_data.py
│
├─→ Connect to Yahoo Finance
│
├─→ For each company (500):
│   │
│   ├─→ Download today's OHLCV
│   ├─→ Store in daily_prices table
│   └─→ Calculate indicators
│
├─→ Update technical_indicators table
│   └─→ Add MA20, MA50, MA100, MA200, RSI14
│
├─→ Log results
│   ├─→ Companies updated: 500
│   ├─→ New records: 500
│   ├─→ Timestamp: 2026-03-28 16:33:45
│   └─→ Status: SUCCESS
│
└─→ **Next day**: Dashboard shows latest data

Total time: 1-3 minutes
Database size: ~+1MB/month
```

---

## 🎨 Moving Averages Explained

### What is a Moving Average?

Moving averages smooth out price noise to show real trends.

```
Stock prices (noisy):  $180, $185, $178, $182, $190, $188, $192

MA20 (20-day average): Smooth line showing trend
                       ├─→ Averages last 20 days
                       ├─→ Updates daily
                       └─→ Helps identify direction

Visual:
│
│  Actual Price (bouncy)       Chart
│  ●●●●●●●●●●●●●●●●●●●●
│   \    /\    /\    /\
│     \/  \/  \/  \/
│
│  MA20 (smooth)               
│  ──────────────────
│   rises slowly (uptrend)
```

### Why 4 Moving Averages?

Each captures different timeframes:

- **MA20**: Short-term (1 month) - quick reactions
- **MA50**: Medium-term (2.5 months) - intermediate trend
- **MA100**: Long-term (5 months) - major trend
- **MA200**: Very long-term (10 months) - yearly trend

**Rule**: 
- Price above MA200 = **Long-term uptrend** 🟢
- Price below MA200 = **Long-term downtrend** 🔴

---

## 📊 RSI14 Explained

### Relative Strength Index

Measures momentum on scale 0-100.

```
RSI 0-30:   OVERSOLD  (bearish, may bounce up)
RSI 30-70:  NEUTRAL   (normal range)
RSI 70-100: OVERBOUGHT (bullish, may pullback)

Visual Scale:
│
│ 100 ▬▬▬▬▬▬▬▬▬▬ OVERBOUGHT (RUN TOO HARD, MIGHT COLLAPSE)
│     
│ 70  ▬▬▬▬▬▬▬▬▬▬ STRONG UP (GOOD MOMENTUM)
│
│ 50  ▬▬▬▬▬▬▬▬▬▬ NEUTRAL (NO CLEAR DIRECTION)
│
│ 30  ▬▬▬▬▬▬▬▬▬▬ WEAK DOWN (WEAK MOMENTUM)
│
│ 0   ▬▬▬▬▬▬▬▬▬▬ OVERSOLD (OVERSOlD, MIGHT BOUNCE)
│
```

---

## 🤖 Why Random Forest?

### Why Not Other Models?

```
Model Type          Pros                  Cons                  Our Choice
────────────────────────────────────────────────────────────────────────
Neural Network      Very flexible         Black box, slow        ❌
SVM                 Fast                  Hard to tune           ❌
Logistic Reg        Simple                Too simple             ❌
Random Forest       ✅ Good accuracy      Medium complex         ✅ CHOSEN
                    ✅ Fast prediction
                    ✅ Feature importance
                    ✅ Handles non-linear
```

### How Random Forest Works

Instead of ONE decision tree:
- **Use 200 tiny decision trees**
- **Each trained on random subset of data**
- **Each votes on prediction**
- **Majority wins**

Result: More accurate than single tree!

```
Stock: Apple, Price > MA200?

Tree 1:  "YES"  ─┐
Tree 2:  "YES"  ─┼─► 77% say YES
Tree 3:  "NO"   ─┼─► 23% say NO  
...              ─┘
Tree 200: "YES"

CONFIDENCE: 77% (how sure we are)
```

---

## 🚀 Future Improvements

1. **Add more indicators**
   - Bollinger Bands
   - MACD
   - Stochastic
   - Moving average convergence

2. **Ensemble models**
   - Combine Random Forest + Neural Network
   - Could improve accuracy to 98%+

3. **Sector-specific models**
   - Train separate models for Tech, Finance, Healthcare
   - Better for sector-specific patterns

4. **Real-time predictions**
   - Update predictions every minute
   - During trading hours

5. **Risk management**
   - Add stop-loss levels
   - Calculate risk/reward ratio
   - Portfolio optimization

6. **Backtesting framework**
   - Test strategy vs historical data
   - Show returns if followed perfectly

---

## 📝 Key Metrics Summary

```
SYSTEM STATISTICS
─────────────────────────────────────
Model Accuracy:          96.97%
Training Samples:        1.1M+
Test Samples:            221,918
Prediction Classes:      5 levels
Feature Count:           7 indicators
Stocks Tracked:          500
Data Points:             1.1M+ records
Database Size:           100-500 MB
Model File Size:         ~2 MB
Daily Update Time:       1-2 minutes
Prediction Time:         <2 seconds
Dashboard Start Time:    5 seconds

PREDICTION DISTRIBUTION
─────────────────────────────────────
Strong Sell (-2):        2.7%
Weak Sell (-1):          24.3%
Hold (0):                17.8%
Weak Buy (1):            47.4%
Strong Buy (2):          7.8%

MODEL PERFORMANCE (Per Class)
─────────────────────────────────────
Class         Precision  Recall  F1-Score
Strong Sell   72%        99%     83%
Weak Sell     99%        95%     97%
Hold          98%        99%     98%
Weak Buy      100%       97%     98%
Strong Buy    85%        100%    92%

FEATURE IMPORTANCE
─────────────────────────────────────
MA200 Distance:          26.5% ★★★★★
RSI14:                   21.6% ★★★★☆
MA20 Distance:           15.4% ★★★☆☆
MA50 Distance:           13.8% ★★★☆☆
MA100 Distance:          13.4% ★★★☆☆
Trend Direction:         9.2%  ★★☆☆☆
Volume Normalized:       0.2%  ☆☆☆☆☆
```

---

## 🔗 System Dependencies

```
streamlit          → Web dashboard UI
pandas             → Data manipulation
scikit-learn       → Machine learning
joblib             → Model serialization
yfinance           → Stock data API
pandas_ta          → Technical indicators
plotly             → Interactive charts
sqlite3            → Database
numpy              → Numerical computations
```

---

**Last Updated**: March 28, 2026  
**System Version**: 2.1  
**Status**: ✅ Production Ready

For day-to-day usage, see **README.md**
