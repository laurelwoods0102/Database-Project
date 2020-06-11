import pandas as pd
import cx_Oracle as oracle
import json

from pprint import pprint

class QueryProcess:
    def __init__(self):
        self.con = oracle.connect("sys", "oracle", "172.17.0.3:1521", oracle.SYSDBA)

    def status(self):
        return pd.read_sql('select status from v$instance', con=self.con)

    def city_name(self):
        return pd.read_sql('select distinct CT_NM from dong_code', con=self.con)

    def local_by_city(self, city, sex, year, month):
        return pd.read_sql('select STANDARD_ID, sum({0}_0_TO_9) + sum({0}_10_TO_14) + sum({0}_15_TO_19) as "00~19", sum({0}_20_TO_24) + sum({0}_25_TO_29) + sum({0}_30_TO_34) + sum({0}_35_TO_39) as "20~39", sum({0}_40_TO_44) + sum({0}_45_TO_49) + sum({0}_50_TO_54) + sum({0}_55_TO_59) as "40~59", sum({0}_60_TO_64) + sum({0}_65_TO_69) + sum({0}_70_TO_74) as "60~99" from LOCAL_PEOPLE_DONG_{1}{2} where CODE in (select H_DNG_CD from DONG_CODE where CT_NM = {3}) group by STANDARD_ID order by STANDARD_ID'.format(sex, year, month, "'" + city + "'"), con=self.con)

    def GS_category(self):
        return pd.read_sql('select distinct "korea_cvs.category" from GS_2016', con=self.con)

    def GS_by_city(self, year, category, city):
        return pd.read_sql('select "korea_cvs.sale_dt", sum("korea_cvs.adj_qty") from GS_{0} where "korea_cvs.category" = {1} and "korea_cvs.bor_nm" = (select RESD_CD from DISTRICT_CODE where RESC_CT_NM = {2}) group by "korea_cvs.sale_dt" order by "korea_cvs.sale_dt"'.format(year, "'" + category + "'", "'" + city + "'"), con=self.con)


if __name__ == "__main__":
    processor = QueryProcess()
    ##pprint(processor.local_by_city("Songpa-gu", "man", "2017", "01"))
    pprint(processor.GS_by_city("2016", "Beer", "Songpa-gu"))