import pandas as pd
from zeno_etl_libs.db.db import Athena

Athena = Athena()
conn = Athena.connection(schema_name='mis-datalake-2022-03-31')
df_data = pd.read_sql_query("select * from bills_1 limit 10", conn)
print(df_data.to_string())
