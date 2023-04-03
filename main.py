import time
import datetime
import os
import json
import csv

from seleniumwire import webdriver
from seleniumwire.utils import decode

def main():
    #list of api path
    api_path = ["/api/set/index/AGRO/composition", 
                "/api/set/index/CONSUMP/composition", 
                "/api/set/index/FINCIAL/composition", 
                "/api/set/index/INDUS/composition", 
                "/api/set/index/PROPCON/composition",
                "/api/set/index/RESOURC/composition",
                "/api/set/index/SERVICE/composition",
                "/api/set/index/TECH/composition"]
    
    #add chrome command line options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    seleniumwire_options = {"disable_encoding": "True", "request_storage_base_dir": r"C:\Users\iJoe\Desktop\Programs\iJoe\SET_market_data_selenium"}

    #setting up the driver
    exe_path = "C:\\Users\\iJoe\\Downloads\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=exe_path, options=options, seleniumwire_options=seleniumwire_options)

    #send request
    driver.get("https://www.settrade.com/th/equities/market-data/overview?category=Index&index=SET")
    time.sleep(10)
  

    #get current date
    now = datetime.datetime.now()
    year = now.year
    monthNumber = twoDigitsDate(now.month)
    monthName = monthNumToName(now.month)
    day = twoDigitsDate(now.day)

    #create folder if not already existed
    folderPath = f"csv/{year}/{monthNumber}-{monthName}"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    #create csv file
    filePath = f"csv/{year}/{monthNumber}-{monthName}/{year}-{monthNumber}-{day}.csv"

    with open(filePath, "w", newline="") as fp:
        field_names = ["symbol", "sign", "prior", "open", "high", "low", "last", "change", "percentChange", "totalVolume", "marketCap", "industryName", "sectorName"]
        writer = csv.DictWriter(fp, fieldnames=field_names)
        writer.writeheader()

        #loop through requests to find desired response(s)
        for request in driver.requests:
            if request.response:
                if request.path in api_path:
                    response = request.response
                    body = decode(response.body, response.headers.get("content-encoding", "identity"))
                    body_str = body.decode()
                    data_dict = json.loads(body_str)
                    subIndices_list = data_dict["composition"]["subIndices"]

                    for sector in subIndices_list:
                        for stock in sector["stockInfos"]:
                            writer.writerow({"symbol": stock["symbol"], "sign": stock["sign"], "prior": stock["prior"], 
                            "open": stock["open"], "high": stock["high"], "low": stock["low"], "last": stock["last"], 
                            "change": stock["change"], "percentChange": stock["percentChange"], "totalVolume": stock["totalVolume"],
                            "marketCap": stock["marketCap"], "industryName": stock["industryName"], "sectorName": stock["sectorName"]} )

    driver.quit()

########## END OF main() ##########

def monthNumToName(monthInt):
    return { 1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"}[monthInt]

#turns "day" and "month" number of value < 10 to two-digits
def twoDigitsDate(number):
    if number < 10:
        number = f"0{number}"

    return number

###################################

if __name__ == "__main__":
    main()