import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import selenium.webdriver

chrome_options = Options()

options = [
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features",
    "--disable-blink-features=AutomationControlled",
    "--disable-3d-apis"
]
for option in options:
    chrome_options.add_argument(option)

# Create the directory if it doesn't exist
CSV_DIR = "flight_datasets"
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

CSV_PATH = os.path.join(CSV_DIR, "flight_data_CASA_Rome.csv")

driver = selenium.webdriver.Chrome(options=chrome_options)

driver.get("https://www.makemytrip.com/flight/search?itinerary=CAS-ROM-30/11/2023&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng")
time.sleep(25)

COUNT = 50

for i in range(1, COUNT + 1):
    fname, fcode, depcity, deptime, arrcity, arrtime, duration, price = "", "", "", "", "", "", "", ""
    try:
        block = driver.find_element(By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']')
    except:
        driver.close()  # page closes when scraping is over
    try:
        # scrapecode
        driver.find_element(By.XPATH,
                             '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[3]/span').click()
        time.sleep(1)
        fname = block.find_element(
            By.XPATH, '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[1]/div/p[1]').text
        print(fname)
        fcode = block.find_element(By.CLASS_NAME, 'fliCode').text
        print("flightcode: " + fcode)

        # DEPARTURE
        deptime = block.find_element(
            By.XPATH,
            '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[1]').text
        print("deptime: " + deptime)
        depcity = block.find_element(
            By.XPATH,
            '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[2]').text
        print("depcity: " + depcity)

        # ARRIVAL
        arrtime = block.find_element(
            By.XPATH,
            '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[1]').text
        print("arrtime: " + arrtime)
        arrcity = block.find_element(
            By.XPATH,
            '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[2]').text
        print("arrcity:" + arrcity)
        duration = block.find_element(
            By.XPATH,
            '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[2]/p').text
        print("duration: " + duration)

        price = driver.find_element(
            By.XPATH,
            '//*[@id="listing-id"]/div/div[2]/div/div[' + str(i) + ']/div[1]/div[2]/div[2]/div/div/div').text
        price = price.split('\n')
        price = price[0][2:]
        print("price: " + price)

    except:
        pass
    data = [[fname, fcode, depcity, deptime, arrcity, arrtime, duration, price]]
    with open(CSV_PATH, 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    time.sleep(2)

driver.close()
