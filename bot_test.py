from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def cookie_down(driver):
    btn_cookies = driver.find_element(By.CSS_SELECTOR, 'div[class$="summary-buttons"] button[size="large"]:last-child')
    btn_cookies.click()


trip_type = 'roundtrip'
departure_type = 'ap'
departure = 'krk'
arrival_type = 'ap'
arrival = 'agp'
departure_date = '2022-02-17'
arrival_date = '2022-02-20'
flight_standard = 'economy'
pax_adult = '1'
pax_young = '0'
pax_children = '0'
pax_infant = '0'

url = f'https://www.esky.pl/flights/select/{trip_type}/{departure_type}/{departure}/{arrival_type}/{arrival}' \
      f'?departureDate={departure_date}&returnDate={arrival_date}&pa={pax_adult}&py={pax_young}&pc={pax_children}&pi={pax_infant}&sc={flight_standard}'

driver = webdriver.Chrome('./drivers/chromedriver')
driver.get(url)

cookie_down(driver)

# driver.close()
