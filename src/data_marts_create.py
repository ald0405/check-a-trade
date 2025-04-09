from pathlib import Path
import sqlite3
from utils.data_processors import load_and_clean

root = Path.cwd()
phone_path = root / "data" / "phone.csv"
case_path = root / "data" / "cases.csv"
omni_path = root / "data" / "salesforce_omni_channel.csv"
whatsapp_path = root / "data" / "whatsapp.csv"


# Some pre-processing of data
phone = load_and_clean(phone_path)
cases = load_and_clean(case_path)
omni = load_and_clean(omni_path)
whatsapp = load_and_clean(whatsapp_path)


# Create Check a trade 'marts'
db_path = root / "db" / "check_marts.db"

conn = sqlite3.connect(db_path)

# Write each cleaned DataFrame to the database
phone.to_sql("phone", conn, if_exists="replace", index=False)
cases.to_sql("cases", conn, if_exists="replace", index=False)
omni.to_sql("salesforce_omni_channel", conn, if_exists="replace", index=False)
whatsapp.to_sql("whatsapp", conn, if_exists="replace", index=False)

# Commit and close
conn.commit()
conn.close()

print(f"✅ Written to {db_path}")
