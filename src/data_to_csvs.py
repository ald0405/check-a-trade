import sqlite3
import pandas as pd 
DATA_DIR  = 'data'
conn = sqlite3.connect("db/case.db")


cursor = conn.cursor()


tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables:", tables)


cases = pd.read_sql_query("""SELECT * FROM cases """,con=conn)
cases.to_csv(DATA_DIR+"/cases.csv")
cases.info()

cases['Callback Reason'].value_counts()


phone = pd.read_sql_query("""SELECT * FROM phone ORDER BY 1 DESC""",con=conn)
phone.to_csv(DATA_DIR+"/phone.csv")
phone.info()



wa = pd.read_sql_query("""SELECT * FROM whatsapp """,con=conn,coerce_float=True)


ewa = pd.read_sql_query("""SELECT * FROM email_web_whatsapp_community """,con=conn,coerce_float=True)

ewa.info()

wa['Status']

ewa.to_csv(DATA_DIR+"/salesforce_omni_channel.csv")
wa.to_csv(DATA_DIR+"/whatsapp.csv")

REPORTS_DIR = "reports"

from ydata_profiling import ProfileReport

profile = ProfileReport(wa, title="Whatsapp Table Report", explorative=True)
profile.to_file(REPORTS_DIR+"/whatsapp.html")




profile = ProfileReport(
    phone, 
    title="Phone Table Report", 
    explorative=True,
    interactions={"continuous": False},    # turn off pairwise interactions
    )
profile.to_file(REPORTS_DIR+"/phone.html")




profile = ProfileReport(cases, 
                        title="Case Table Report", 
                        explorative=True,
                        interactions={"continuous": False},    # turn off pairwise interactions
)

profile.to_file(REPORTS_DIR+"/case.html")

