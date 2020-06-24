import pandas as pd
import cx_Oracle as oracle

from pprint import pprint

class QueryProcess:
    def __init__(self):
        self.con = oracle.connect("sys", "oracle", "172.17.0.3:1521", oracle.SYSDBA)   # Container
        #self.con = oracle.connect("sys", "oracle", "localhost:1522", oracle.SYSDBA)     # Local 
        
    def status(self):
        return pd.read_sql('select status from v$instance', con=self.con)

    # For Argument
    def city_name(self):
        return pd.read_sql('select distinct CT_NM from dong_code', con=self.con)

    # For Argument
    def GS_category(self):
        return pd.read_sql('select distinct "korea_cvs.category" from GS_2016', con=self.con)

    def local_by_city(self, city, sex, year, month):
        # STANDARD_ID for Date
        return pd.read_sql('select sum({0}_0_TO_9) + sum({0}_10_TO_14) + sum({0}_15_TO_19) as "{0}_00~19", sum({0}_20_TO_24) + sum({0}_25_TO_29) + sum({0}_30_TO_34) + sum({0}_35_TO_39) as "{0}_20~39", sum({0}_40_TO_44) + sum({0}_45_TO_49) + sum({0}_50_TO_54) + sum({0}_55_TO_59) as "{0}_40~59", sum({0}_60_TO_64) + sum({0}_65_TO_69) + sum({0}_70_TO_74) as "{0}_60~99" from LOCAL_PEOPLE_DONG_{1}{2} where CODE in (select H_DNG_CD from DONG_CODE where CT_NM = {3}) group by STANDARD_ID order by STANDARD_ID'.format(sex, year, month, "'" + city + "'"), con=self.con)

    def subway(self, year, city):
        # "Date" for Date
        return pd.read_sql('select sum("TIME_05_06" + "TIME_06_07" + "TIME_07_08" + "TIME_08_09" + "TIME_09_10" + "TIME_10_11" + "TIME_11_12" + "TIME_12_13" + "TIME_13_14" + "TIME_14_15" + "TIME_15_16" + "TIME_16_17" + "TIME_17_18" + "TIME_18_19" + "TIME_19_20" + "TIME_20_21" + "TIME_21_22" + "TIME_22_23" + "TIME_23_24" + "TIME_24_")  as TOTAL_PASSENGER from SUBWAY_{0} where "Station_ID" in (select "Subway_Station_Code" from STATION_INFORMATION where "District_Code_of_Station" = (select RESD_CD from DISTRICT_CODE where RESC_CT_NM = {1})) group by "Date" order by "Date"'.format(year, "'" + city + "'"), con=self.con)
    
    def weather(self, year):
        # "Date" for Date
        return pd.read_sql('select sum("Temperature") as "Temperature", sum("Precipitation") as "Precipitation", sum("Wind_Velocity") as "Wind_Velocity", sum("Humidity") as "Humidity", sum("Snowfall") as "Snowfall", sum("Cloud") as "Cloud" from WEATHER_{0} group by "Date" order by "Date"'.format(year), con=self.con)

    def GS_by_city(self, year, category, city):
        return pd.read_sql('select "korea_cvs.sale_dt" as "Date", sum("korea_cvs.adj_qty") as "GS" from GS_{0} where "korea_cvs.category" = {1} and "korea_cvs.bor_nm" = (select RESD_CD from DISTRICT_CODE where RESC_CT_NM = {2}) group by "korea_cvs.sale_dt" order by "korea_cvs.sale_dt"'.format(year, "'" + category + "'", "'" + city + "'"), con=self.con)

    # Query Dataset per Year
    ## Dataset Structure : 'Date', 'man_00~19', 'man_20~39', 'man_40~59', 'man_60~99', 'woman_00~19', 'woman_20~39', 'woman_40~59', 'woman_60~99', 'TOTAL_PASSENGER', 'Temperature', 'Precipitation', 'Wind_Velocity', 'Humidity', 'Snowfall', 'Cloud', 'GS'
    def query_dataset(self, year, city, category):
        year = str(year)

        # Concatenate LOCAL_PEOPLE_DONG for Year
        ## Man
        local_man = self.local_by_city(city, "man", year, "01")
        for i in range(2, 13):
            local_man = pd.concat([local_man, self.local_by_city(city, "man", year, str(i).zfill(2))], axis=0, ignore_index=True) 

        ## Woman
        local_woman = self.local_by_city(city, "woman", year, "01")
        for i in range(2, 13):
            local_woman = pd.concat([local_woman, self.local_by_city(city, "woman", year, str(i).zfill(2))], axis=0, ignore_index=True)    

        Subway = self.subway(year, city)
        weather = self.weather(year)
        GS = self.GS_by_city(year, category, city)
        
        #return pd.concat([GS["Date"], local_man, local_woman, Subway, weather, GS["GS"]], axis=1)

        data = pd.concat([local_man, local_woman, Subway, weather, GS["GS"]], axis=1)
        data.index = GS["Date"]
        return data        


if __name__ == "__main__":
    query_processor = QueryProcess()
    '''
    pprint(processor.local_by_city("Songpa-gu", "man", "2017", "01"))
    print("\n******************************************************\n")
    pprint(processor.GS_by_city("2017", "Beer", "Songpa-gu")["GS"])
    print("\n******************************************************\n")
    pprint(processor.subway("2017", "Songpa-gu")["TOTAL_PASSENGER"])
    '''

    pprint(query_processor.query_dataset(2017, "Gangnam-gu", "Beer").values[:, :15])
