from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

base_url = 'http://localhost:8000'

driver = webdriver.Firefox()
driver.set_page_load_timeout(3600)

driver.get(base_url)

select_all_dropdown = driver.find_element(
    By.CSS_SELECTOR, 'button.ms-choice'
)
select_all_dropdown.click()

dropdown = driver.find_element(By.CSS_SELECTOR, '.ms-drop.bottom')
lis = dropdown.find_elements(By.CSS_SELECTOR, 'li')

for li in lis:
    try:
        select_batch_checkbox = li.find_element(By.CSS_SELECTOR, 'input[data-name="selectItem"]')
    except NoSuchElementException:
        continue
    if select_batch_checkbox.get_attribute('data-name') == 'selectItem':
        select_batch_checkbox.click()

