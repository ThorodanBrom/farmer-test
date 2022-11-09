from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import os
import json

options = webdriver.ChromeOptions()

if len(sys.argv) == 1:
    raise Exception("Set a download directory in argument")

download_path = sys.argv[1]
print("Setting download directory as", download_path)
prefs = {"download.default_directory": download_path}
options.add_experimental_option("prefs", prefs)

service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://soilhealth.dac.gov.in/PublicReports/NutrientStatusFarmerWise")

state_code = driver.find_element(By.ID, "State_Code")
all_states = state_code.find_elements(By.TAG_NAME, "option")

for state in all_states:
    if state.get_attribute("value") == "":
        continue
    state_name = state.get_attribute("text")
    state.click()
    time.sleep(1)

    district_code = driver.find_element(By.ID, "District_Code")
    all_districts_in_state = district_code.find_elements(By.TAG_NAME, "option")
    for district in all_districts_in_state:
        if district.get_attribute("value") == "":
            continue
        district_name = district.get_attribute("text")
        district.click()
        time.sleep(1)

        sub_district_code = driver.find_element(By.ID, "sub_district_code")
        all_sub_districts = sub_district_code.find_elements(By.TAG_NAME, "option")
        for sub_district in all_sub_districts:
            if sub_district.get_attribute("value") == "":
                continue
            sub_district_name = sub_district.get_attribute("text")
            sub_district.click()
            time.sleep(1)

            cycle_id = driver.find_element(By.ID, "CycleId")
            all_cycles = cycle_id.find_elements(By.TAG_NAME, "option")
            for cycle in all_cycles:
                if cycle.get_attribute("value") == "":
                    continue
                cycle_name = cycle.get_attribute("text")
                cycle.click()
                time.sleep(1)

                driver.find_element(By.ID, "confirmLink").click()
                try:
                    time.sleep(5)
                    WebDriverWait(driver, 30).until(
                        EC.frame_to_be_available_and_switch_to_it(
                            driver.find_element(
                                By.XPATH,
                                "/html/body/div[2]/div/div[2]/div/div/form/fieldset/div[2]/table[2]/tbody/tr/td/div/iframe",
                            )
                        )
                    )
                    time.sleep(10)
                    driver.execute_script(
                        "$find('ReportViewer1').exportReport('EXCELOPENXML');"
                    )
                    driver.switch_to.default_content()
                except:
                    print("Encountered error!!!")
                    print("Check progress.json for last processed file")
                else:
                    downloaded_file = (
                        download_path + "/" + "NutrientStatusFarmerWise.xlsx"
                    )
                    new_file_name = "_".join(
                        [state_name, district_name, sub_district_name, cycle_name]
                    ).replace(" ", "-")

                    while not os.path.exists(downloaded_file):
                        time.sleep(0.5)

                    os.rename(
                        downloaded_file, download_path + "/" + new_file_name + ".xlsx"
                    )
                    print(
                        "Downloaded {} {} {} {}".format(
                            state_name, district_name, sub_district_name, cycle_name
                        )
                    )
