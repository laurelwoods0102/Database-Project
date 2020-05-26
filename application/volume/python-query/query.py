import cx_Oracle as oracle
import pandas as pd

con1 = oracle.connect("sys", "oracle", "localhost:1522", oracle.SYSDBA)

#ex = pd.read_sql("select * from LOCAL_PEOPLE_DONG_201701_1", con=con1)
man_by_region = pd.read_sql(
    'select CODE, sum(MAN_0_TO_9) + sum(MAN_10_TO_14) + sum(MAN_15_TO_19) as "00~19",' +
    'sum(MAN_20_TO_24) + sum(MAN_25_TO_29) + sum(MAN_30_TO_34) + sum(MAN_35_TO_39) as "20~39",' +
    'sum(MAN_40_TO_44) + sum(MAN_45_TO_49) + sum(MAN_50_TO_54) + sum(MAN_55_TO_59) as "40~59",' +
    'sum(MAN_60_TO_64) + sum(MAN_65_TO_69) + sum(MAN_70_TO_74) as "60~99"'
    'from LOCAL_PEOPLE_DONG_201701_1 group by CODE', con=con1)
    
woman_by_region = pd.read_sql(
    'select CODE, sum(WOMAN_0_TO_9) + sum(WOMAN_10_TO_14) + sum(WOMAN_15_TO_19) as "00~19",' +
    'sum(WOMAN_20_TO_24) + sum(WOMAN_25_TO_29) + sum(WOMAN_30_TO_34) + sum(WOMAN_35_TO_39) as "20~39",' +
    'sum(WOMAN_40_TO_44) + sum(WOMAN_45_TO_49) + sum(WOMAN_50_TO_54) + sum(WOMAN_55_TO_59) as "40~59",' +
    'sum(WOMAN_60_TO_64) + sum(WOMAN_65_TO_69) + sum(WOMAN_70_TO_74) as "60~99"'
    'from LOCAL_PEOPLE_DONG_201701_1 group by CODE', con=con1)

print(woman_by_region)