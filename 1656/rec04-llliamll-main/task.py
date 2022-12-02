import json
from datetime import datetime, timedelta, date
import requests
import pandas as pd

class Task(object):
    def __init__(self, start_date, end_date):
        self.wprdc_api_endpoint = "https://data.wprdc.org/api/3/action/datastore_search_sql"
        self.resource_id = "1a1329e2-418c-4bd3-af2c-cc334e7559af"
        self.start_str = start_date.strftime("%Y-%m-%d")
        self.end_str = end_date.strftime("%Y-%m-%d")        

    def t1(self):
        query = """
            SELECT "facility_name" as facility, COUNT("description_new") as count
            FROM "{}"
            WHERE "inspect_dt" BETWEEN '{}' and '{}' AND "city" = '{}' AND "rating" = '{}'
            GROUP BY "facility_name"
            ORDER BY count DESC
            LIMIT 30 """.format(self.resource_id, self.start_str, self.end_str, "Pittsburgh", "V")
        response = requests.get(self.wprdc_api_endpoint, {'sql': query}, verify=False)
        df = pd.DataFrame.from_dict(json.loads(response.text)['result']['records'])
        return df

    def t2(self):
        #pd.set_option('display.max_columns', None)
        query = """
            SELECT "facility_name" as facility, "description_new" as violation, "rating" as rating , "high" as high, "medium" as medium, "low" as low
            FROM "{}"
            WHERE "facility_name" LIKE 'Pitt%' AND "inspect_dt" BETWEEN '{}' and '{}' AND "city" = '{}'
            
        """.format(self.resource_id, self.start_str, self.end_str, "Pittsburgh")
        response = requests.get(self.wprdc_api_endpoint, {'sql': query}, verify=False)
        df = pd.DataFrame.from_dict(json.loads(response.text)['result']['records'])
        return df

    def t3(self):
        #pd.set_option('display.max_columns', None)
        query = """
            SELECT "facility_name" as facility, "description_new" as violation, "rating" as rating , "high" as high, "medium" as medium, "low" as low
            FROM "{}"
            WHERE ("facility_name" LIKE '% Pitt %'
             OR "facility_name" LIKE 'Pitt %'
             OR "facility_name" LIKE '% Pitt'
             OR "facility_name" LIKE 'Pitt')
             AND "inspect_dt" BETWEEN '{}' and '{}' AND "city" = '{}'
        """.format(self.resource_id, self.start_str, self.end_str, "Pittsburgh")
        response = requests.get(self.wprdc_api_endpoint, {'sql': query}, verify=False)
        df = pd.DataFrame.from_dict(json.loads(response.text)['result']['records'])
        return df

    def t4(self):
        query = """
            SELECT "facility_name" as facility, COUNT("description_new") as count
            FROM "{}"
            WHERE "inspect_dt" BETWEEN '{}' and '{}' AND "city" = '{}' AND "rating" = '{}' AND 
            ("facility_name" LIKE '% Pitt %'
             OR "facility_name" LIKE 'Pitt %'
             OR "facility_name" LIKE '% Pitt'
             OR "facility_name" LIKE 'Pitt')
            GROUP BY "facility_name"
            ORDER BY count DESC
            LIMIT 20 """.format(self.resource_id, self.start_str, self.end_str, "Pittsburgh","V")
        response = requests.get(self.wprdc_api_endpoint, {'sql': query}, verify=False)
        df = pd.DataFrame.from_dict(json.loads(response.text)['result']['records'])
        return df

if __name__ == "__main__":
    t = Task(date(2018, 9, 1), date(2019, 6, 1))
    print("----T1----" + "\n")
    print(str(t.t1()) + "\n")
    print("----T2----" + "\n")
    print(str(t.t2()) + "\n")
    print("----T3----" + "\n")
    print(str(t.t3()) + "\n")
    print("----T4----" + "\n")
    print(str(t.t4()) + "\n")
