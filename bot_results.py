import contextlib
import json
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@contextlib.contextmanager
def driver_setup(headless=True):
    options = Options()
    options.headless = headless

    service = Service('./drivers/chromedriver')
    service.start()
    driver = webdriver.Remote(service.service_url, options=options)

    try:
        yield driver
    except TimeoutException:
        return 'Service overloaded, please try later.'
    finally:
        driver.close()


def cookie_down(driver_):
    try:
        btn_cookies = driver_.find_element(By.CSS_SELECTOR, 'div[class$="summary-buttons"] button[size="large"]:last-child')
        btn_cookies.click()
    except NoSuchElementException:
        return 'Service not available, please try again.'


def get_flight_data(result, flight, name):
    result[f'{name}_airline'] = flight.find_element(By.CSS_SELECTOR, 'img.ng-star-inserted').get_attribute("alt")
    result[f'{name}_time'] = {
        'start_time': flight.find_element(By.CSS_SELECTOR, 'span.hour.departure').text,
        'arrival_time': flight.find_element(By.CSS_SELECTOR, 'span.hour.arrival').text
    }
    result[f'{name}_change'] = {
        'quantity': flight.find_element(By.CSS_SELECTOR, 'span.ng-star-inserted').text[0],
        'location': ', '.join(
            [code.get_property('textContent') for code in flight.find_elements(By.CSS_SELECTOR, 'div.code>span')])
    }


def get_results(departure, arrival, departure_date, return_date, trip_type='roundtrip', departure_type='ap',
                arrival_type='ap', flight_standard='economy', pa='1', py='0', pc='0', pi='0'):
    url = f'https://www.esky.pl/flights/select/{trip_type}/{departure_type}/{departure}/{arrival_type}/{arrival}' \
          f'?departureDate={departure_date}&returnDate={return_date}&pa={pa}&py={py}&pc={pc}&pi={pi}&sc={flight_standard}'

    with driver_setup(headless=False) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        time.sleep(3)
        cookie_down(driver)

        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.badge .content')))
        time.sleep(3)

        results = []
        flights = driver.find_elements(By.CLASS_NAME, 'flight-content')
        for flight in flights:
            result = {'departure': departure, 'arrival': arrival, 'departure_date': departure_date, 'return_date': return_date}
            result['amount'] = flight.find_element(By.CLASS_NAME, 'amount').text

            dep, arr = flight.find_elements(By.CLASS_NAME, 'leg-group-container')
            get_flight_data(result, dep, 'departure')
            get_flight_data(result, arr, 'return')

            results.append(result)

        return results


data = get_results('krk', 'agp', '2022-02-26', '2022-03-06')
json_data = json.dumps(data)
print(json_data)
