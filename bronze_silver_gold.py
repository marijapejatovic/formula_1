import pandas as pd
from sqlalchemy import create_engine
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
            self.df[col]=pd.to_datetime(self.df[col], format="%I:%M:%S %p", errors="coerce")
        return self
    def fix_numerical(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=pd.to_numeric(self.df[col], errors="coerce")
        return self
    def standardize_intervals(self, columns:list)->"DataCleaner":
        for col in columns:
            self.df[col]=pd.to_timedelta(self.df[col], errors="coerce")
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
    silver_row=(silver.standardize_text_columns(["positionText", "name_x", "name_y", "location", "country", "forename", "surname", "nationality", "nationality_constructors", "positionText_constructorstandings", "status"])
                                  .fix_dates_columns(["date", "quali_date", "dob", "sprint_date"])
                                  .fix_time(["time", "fastestLapTime","time_races","quali_time", "sprint_time", "time_laptimes", "time_pitstops"])
                                  .fix_numerical(["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "positionOrder", "points", "laps", "milliseconds","fastestLap", "rank", "fastestLapSpeed", "statusId", "year", "round","lat", "lng", "alt", "number_drivers", "lap", "position_laptimes", "milliseconds_laptimes", "lap_pitstops", "milliseconds_pitstops", "stop","driverStandingsId", "points_driverstandings", "position_driverstandings", "wins", "constructorStandingsId", "points_constructorstandings", "position_constructorstandings", "wins_constructorstandings"])
                                  .standardize_intervals(["duration"])
                                  .standardize_url(["url_x", "url_y", "url", "url_constructors"])
                                  .standardize_lowercase(["circuitRef", "driverRef", "constructorRef"])
                                  .standardize_uppercase(["code"])
    )
    silver_row.df.to_csv("silver.csv", index=False)
    

   
    
    
                            


    
    


