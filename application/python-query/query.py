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

    '''
    def dongs_in_city(self):
        result = dict()           

        for city in self.city_name().T.values.tolist()[0]:
            result[city] = pd.read_sql("select H_DNG_CD from dong_code where CT_NM = '{}'".format(str(city)), con=self.con).T.values.tolist()[0]
        return result

    def by_region(self, sex, year, month):
        return pd.read_sql('select STANDARD_ID, CODE, sum({0}_0_TO_9) + sum({0}_10_TO_14) + sum({0}_15_TO_19) as "00~19", sum({0}_20_TO_24) + sum({0}_25_TO_29) + sum({0}_30_TO_34) + sum({0}_35_TO_39) as "20~39", sum({0}_40_TO_44) + sum({0}_45_TO_49) + sum({0}_50_TO_54) + sum({0}_55_TO_59) as "40~59", sum({0}_60_TO_64) + sum({0}_65_TO_69) + sum({0}_70_TO_74) as "60~99" from LOCAL_PEOPLE_DONG_{1}{2} group by STANDARD_ID, CODE order by CODE'.format(sex, year, month), con=self.con)
    '''

    def local_by_city(self, city, sex, year, month):
        return pd.read_sql('select STANDARD_ID, sum({0}_0_TO_9) + sum({0}_10_TO_14) + sum({0}_15_TO_19) as "00~19", sum({0}_20_TO_24) + sum({0}_25_TO_29) + sum({0}_30_TO_34) + sum({0}_35_TO_39) as "20~39", sum({0}_40_TO_44) + sum({0}_45_TO_49) + sum({0}_50_TO_54) + sum({0}_55_TO_59) as "40~59", sum({0}_60_TO_64) + sum({0}_65_TO_69) + sum({0}_70_TO_74) as "60~99" from LOCAL_PEOPLE_DONG_{1}{2} where CODE in (select H_DNG_CD from DONG_CODE where CT_NM = {3}) group by STANDARD_ID order by STANDARD_ID'.format(sex, year, month, "'" + city + "'"), con=self.con)
        #return pd.read_sql('select l.STANDARD_ID, sum(l.{0}_0_TO_9) + sum(l.{0}_10_TO_14) + sum(l.{0}_15_TO_19) as "00~19", sum(l.{0}_20_TO_24) + sum(l.{0}_25_TO_29) + sum(l.{0}_30_TO_34) + sum(l.{0}_35_TO_39) as "20~39", sum(l.{0}_40_TO_44) + sum(l.{0}_45_TO_49) + sum(l.{0}_50_TO_54) + sum(l.{0}_55_TO_59) as "40~59", sum(l.{0}_60_TO_64) + sum(l.{0}_65_TO_69) + sum(l.{0}_70_TO_74) as "60~99" from LOCAL_PEOPLE_DONG_{1}{2} l, DONG_CODE d where l.CODE = d.H_DNG_CD group by l.STANDARD_ID order by l.STANDARD_ID'.format(sex, year, month), con=self.con)


    def GS_by_city(self):
        return pd.read_sql('', con=self.con)

if __name__ == "__main__":
    processor = QueryProcess()
    #print(processor.by_region("man", "2017", "01"))
    pprint(processor.local_by_city("Songpa-gu", "man", "2017", "01"))