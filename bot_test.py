from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cookie_down(driver_):
    btn_cookies = driver_.find_element(By.CSS_SELECTOR, 'div[class$="summary-buttons"] button[size="large"]:last-child')
    btn_cookies.click()


trip_type = 'roundtrip'
departure_type = 'ap'
departure = 'krk'
arrival_type = 'ap'
arrival = 'agp'
departure_date = '2022-02-26'
arrival_date = '2022-03-06'
flight_standard = 'economy'
pax_adult = '1'
pax_young = '0'
pax_children = '0'
pax_infant = '0'

url = f'https://www.esky.pl/flights/select/{trip_type}/{departure_type}/{departure}/{arrival_type}/{arrival}' \
      f'?departureDate={departure_date}&returnDate={arrival_date}&pa={pax_adult}&py={pax_young}&pc={pax_children}&pi={pax_infant}&sc={flight_standard}'

options = Options()
# options.headless = True

service = Service('./drivers/chromedriver')
service.start()
driver = webdriver.Remote(service.service_url, options=options)

driver.get(url)

wait = WebDriverWait(driver, 20)

cookie_down(driver)


# def select_progress_bar(driver_):
#     progress_bar = driver_.find_element(
#         by=By.CSS_SELECTOR,
#         value="div progress-bar"
#     )
#     value = progress_bar.text
#     return not bool(value)
#
#
# wait.until(select_progress_bar)

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.badge .content')))

amounts = []
flights = driver.find_elements(By.CLASS_NAME, 'flight-content')
for flight in flights:
    amounts.append(flight.find_element(By.CLASS_NAME, 'amount').text)

print(amounts)

driver.close()
