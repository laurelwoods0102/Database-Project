import cx_Oracle as oracle
import pandas as pd

con1 = oracle.connect("sys", "oracle", "localhost:1522", oracle.SYSDBA)

ex = pd.read_sql("select * from ex", con=con1)

print(ex)