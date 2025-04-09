# 🧰 Check-A-Trade AI Toolkit

This project analyses and supports customer service interactions for Checkatrade, 
focusing on automation opportunities, workload reduction, and insight generation.

---


## 🚀 Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up environment variables

Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your-api-key-here
```

This is required for the `summary_client.py` module.

### Create the processed database/marts

```bash
python src/data_to_csvs.py # Write each table to data/
python src/data_marts_create.py # Creates check_marts.db
```

This builds the `check_marts.db` file from CSVs and writes clean tables for downstream analysis


## 📊 Analysis & Reporting

The main exploratory analysis is in:

```
notebooks/exploratory_data_analysis.ipynb
```

This notebook leverages:
- `check_marts.db` as the primary data source
- `utils.inferential_statistics` for bootstrap confidence intervals, effect size, and non-parametric testing


---

## 📊 Streamlit Apps

### 📝 Profile Creation App

```bash
streamlit run profile_creation_app.py
```

Enables tradespeople or internal users to create new profiles with AI support.

### ✏️ Profile Update App

```bash
streamlit run profile_update_app.py
```

Lets users update or revise their existing Checkatrade profiles with AI-generated suggestions and controls.


## 🗂️ Project Structure

```
check-a-trade/
├── data/                  # CSV inputs and outputs
├── db/                    # SQLite databases (e.g. check_marts.db)
├── documents/             # Reference docs (e.g. profile writing guides)
├── logs/                  # Output of logging module
├── notebooks/
│   └── exploratory_data_analysis.ipynb  # Primary analysis notebook
├── reports/               # Optional folder for data profiles
├── src/
│   ├── data_marts_create.py       # Builds the 'check_marts.db'
│   ├── data_to_csvs.py            # Creates csvs from the case.db
│   ├── summary_client.py          # Summary generation or chatbot client
│── utils/
│   ├── inferential_statistics.py  # Statistics wrapper class.
│   └── data_processors.py        # Misc helper functions
├── profile_creation_app.py         # Streamlit app for creating profiles
├── profile_update_app.py           # Streamlit app for updating profiles
├── requirements.txt
├── .env                            # Contains secrets like OPENAI_API_KEY
```

---