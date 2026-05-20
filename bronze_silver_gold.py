import pandas as pd
from sqlalchemy import create_engine,text 
from dotenv import load_dotenv
import os
class DataCleaner:
    def __init__(self, df: pd.DataFrame, name: str):
        self.df=df.copy()
        self.name=name
    def standardize_text_columns(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=self.df[col].astype(str)
            self.df[col]=self.df[col].str.strip().str.title()
        return self
    def fix_dates_columns(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=pd.to_datetime(self.df[col],format="mixed", errors="coerce") 
        return self
    def fix_time(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=pd.to_datetime(self.df[col], format="%I:%M:%S %p", errors="coerce").dt.strftime("%H:%M:%S")
        return self
    def fix_numerical(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=pd.to_numeric(self.df[col], errors="coerce")
        return self
    def standardize_lowercase(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=self.df[col].str.strip().str.lower()
        return self
    def standardize_uppercase(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=self.df[col].str.strip().str.upper()
        return self
    def standardize_url(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=self.df[col].where(self.df[col].str.match(r"https?://\S+"), other=pd.NA)
        return self
    
if __name__=="__main__":
    load_dotenv()
    engine=create_engine(os.getenv("DATABASE_URL"))
    bronze_row=pd.read_csv("dataEngineeringDataset.csv", low_memory=False)
    bronze_row.to_sql("bronze_row", engine, if_exists="replace", index=False)
    bronze_from_db = pd.read_sql("SELECT * FROM bronze_row", engine)
    silver = DataCleaner(bronze_from_db, "silver_row")
    silver_row=(silver.standardize_text_columns(["positionText", "name_x", "name_y", "location", "country", "forename", "surname", "nationality", "nationality_constructors", "positionText_constructorstandings", "status", "duration"])
                                  .fix_dates_columns(["date", "quali_date", "dob", "sprint_date"])
                                  .fix_time(["time", "fastestLapTime","time_races","quali_time", "sprint_time", "time_laptimes", "time_pitstops"])
                                  .fix_numerical(["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "positionOrder", "points", "laps", "milliseconds","fastestLap", "rank", "fastestLapSpeed", "statusId", "year", "round","lat", "lng", "alt", "number_drivers", "lap", "position_laptimes", "milliseconds_laptimes", "lap_pitstops", "milliseconds_pitstops", "stop","driverStandingsId", "points_driverstandings", "position_driverstandings", "wins", "constructorStandingsId", "points_constructorstandings", "position_constructorstandings", "wins_constructorstandings"])
                                  .standardize_url(["url_x", "url_y", "url", "url_constructors"])
                                  .standardize_lowercase(["circuitRef", "driverRef", "constructorRef"])
                                  .standardize_uppercase(["code"])
    )
    silver_row.df.to_csv("silver.csv", index=False)
    silver_row.df.to_sql("silver_row", engine, if_exists="replace", index=False)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    print(f"Bronze redovi {len(bronze_row)}")
    print(f"Silver redovi {len(silver_row.df)}")
    print(f"izgubljeni redovi {len(bronze_row)-len(silver_row.df)}")
    print("Null vrijednosti po kolonama:")
    print(silver_row.df.isnull().sum())
    print("tipovi podataka po kolonama:")
    print(silver_row.df.dtypes)
   #with engine.connect() as conn:
        #ith open("tabela.sql", "r") as f:
           #conn.execute(text(f.read()))
       #conn.commit() 
   #dim_status=pd.read_sql("select distinct statusId, status from silver_row", engine)
   #dim_status.to_sql("dim_status", engine, if_exists="append", index=False)
   #dim_constructors=pd.read_sql("select distinct constructorId, constructorRef, name, nationality_constructor, url_constructors from silver_row", engine)
   #dim_constructors.to_sql("dim_constructors", engine, if_exists="append", index=False)
   #dim_driver=pd.read_sql("select distinct driverId, number, driverRef, number_drivers, code, forename, surname, dob, nationality, url from silver_row", engine)
   #dim_driver.to_sql("dim_driver", engine, if_exists="append", index=False)
   #dim_race=pd.read_sql("select distinct raceId, year, round, name_x, url_x, quali_date, quali_time, date, time_races, sprint_date, sprint_time from silver_row", engine)
   #dim_race.to_sql("dim_race", engine, if_exists="append", index="False")



    
                           




    

   
    
    
                            


    
    


