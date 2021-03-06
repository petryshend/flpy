import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from credentials import Credentials
from women_done import WomenDone


class Mailer:

    base_url = 'http://www.foreignladies.com'

    def __init__(self, only_with_photos):
        self.only_with_photos = only_with_photos
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(3600)
        self.women_send_intro_links = []
        self.men = self.load_men_array_from_json()
        self.men_countries = list(self.men.keys())
        self.username = Credentials.get()['username']
        self.password = Credentials.get()['password']

    @staticmethod
    def load_men_array_from_json():
        with open('men.json') as data_file:
            data = json.load(data_file)
        return data

    def start(self):
        wd = WomenDone()
        self.open_home_page()
        self.go_to_login_page()
        self.submit_login_form()
        time.sleep(2)
        self.submit_agree_with_rules_form()
        self.go_to_women_list()
        self.collect_women_search_profile_links()
        for woman_link in self.women_send_intro_links:
            if woman_link not in wd.get().keys():
                self.send_letters_for_woman(woman_link)
                woman_name = self.extract_woman_name()
                wd.add(woman_link, woman_name)

    def close_mailer(self):
        self.driver.close()

    def open_home_page(self):
        self.driver.get(self.base_url)

    def go_to_login_page(self):
        login_link_text = 'Affiliate Login'
        login_link = self.driver.find_element(By.LINK_TEXT, login_link_text)
        login_link.click()

    def submit_login_form(self):
        time.sleep(1)
        username_input = self.driver.find_element(By.ID, 'logins_ident')
        username_input.send_keys(self.username)

        password_input = self.driver.find_element(By.ID, 'logins_password')
        password_input.send_keys(self.password)

        submit_button = self.driver.find_element(By.NAME, 'btn_submit')
        submit_button.click()

    def submit_agree_with_rules_form(self):
        time.sleep(2)
        understand_radio = self.driver.find_element(By.CSS_SELECTOR, 'input[value=\"yes\"]')
        understand_radio.click()

        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type=\"submit\"]')
        submit_button.click()

    def go_to_women_list(self):
        woman_list_url = 'http://www.foreignladies.com/aff-assign_women~_step-500.html'
        self.driver.get(woman_list_url)

    def collect_women_search_profile_links(self):
        link_selector = 'a[title=\"Send Intro\"]'
        links = self.driver.find_elements(By.CSS_SELECTOR, link_selector)
        for link in links:
            self.women_send_intro_links.append(link.get_attribute('href'))

    def send_letters_for_woman(self, woman_link):
        self.driver.get(woman_link)
        for country in self.men_countries:
            country_age_ranges = self.men[country]['ranges']
            for age_range in country_age_ranges:
                print 'Setting range for ' + country + ': ' + str(age_range)
                country_select = self.driver.find_element(By.ID, 'fk_countries')
                country_select.send_keys(country)
                self.set_age_range(age_range)
                time.sleep(1)
                expand_button = self.driver.find_element(By.CSS_SELECTOR, 'a.btn_expand')
                expand_button.click()
                self.check_other_search_criteria()
                self.click_submit_search_button()
                time.sleep(5)
                self.check_all_and_click_green_big_send_button()
                self.driver.get(woman_link)


    def set_age_range(self, age_range):
        from_select = self.driver.find_element(
            By.CSS_SELECTOR, 'select[name=profile_age__GREATER_EQUAL]')
        from_select.send_keys(age_range[0])

        to_select = self.driver.find_element(
            By.CSS_SELECTOR, 'select[name=profile_age__SMALLER_EQUAL]')
        to_select.send_keys(age_range[1])

    def check_other_search_criteria(self):
        last_activity = self.driver.find_element(
            By.CSS_SELECTOR, 'select[name=last_activity]')
        last_activity.send_keys('Less than 6 months ago')

        if self.only_with_photos:
            photos = self.driver.find_element(
                By.CSS_SELECTOR, 'select[name=profile_default_pic]')
            photos.send_keys('Profiles with Photos')

        russian_girls_checkbox = self.driver.find_element(By.ID, 'Q_69_935')
        if not russian_girls_checkbox.is_selected():
            russian_girls_checkbox.click()
        any_girls_checkbox = self.driver.find_element(By.ID, 'Q_69_-1')
        if any_girls_checkbox.is_selected():
            any_girls_checkbox.click()
        time.sleep(1)

    def click_submit_search_button(self):
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name=btn_submit]')
        submit_button.click()

    def check_all_and_click_green_big_send_button(self):
        if not self.has_men_search_results():
            print 'No results'
            return

        current_href = self.driver.current_url

        select_all_dropdown = self.driver.find_element(
            By.CSS_SELECTOR, 'button.ms-choice'
        )
        select_all_dropdown.click()
        time.sleep(1)

        dropdown = self.driver.find_element(By.CSS_SELECTOR, '.ms-drop.bottom')
        batch_checkbox_inputs = dropdown.find_elements(By.CSS_SELECTOR, 'input[data-name="selectItem"]')
        batch_values = []
        for checkboxInput in batch_checkbox_inputs:
            batch_values.append(checkboxInput.get_attribute('value'))

        for value in batch_values:
            checkbox = self.driver.find_element(By.CSS_SELECTOR, 'input[value="' + value + '"]')
            checkbox.click()
            self.click_big_green_button()
            does_not_want = 'User does not want to receive intro letters!'
            if does_not_want in self.driver.page_source:
                print 'Does not want'
                return
            self.select_intro_letter()
            self.select_photo_to_attach()
            self.click_send_message_button()
            time.sleep(1)
            self.driver.get(current_href)
            select_all_dropdown = self.driver.find_element(
                By.CSS_SELECTOR, 'button.ms-choice'
            )
            select_all_dropdown.click()
            time.sleep(1)

    def has_men_search_results(self):
        no_results_error_span = self.driver.find_elements(By.CSS_SELECTOR, 'span.error_star')
        if len(no_results_error_span) != 0:
            return False
        return True

    def click_big_green_button(self):
        send_intro_button = self.driver.find_element(
            By.PARTIAL_LINK_TEXT, 'SEND INTRO TO SELECTED MEMBERS')
        send_intro_button.click()

    def select_intro_letter(self):
        time.sleep(5)
        select_intro_letter = self.driver.find_element(By.CSS_SELECTOR, 'select#intro_letter')
        time.sleep(1)
        select_intro_letter.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        select_intro_letter.send_keys(Keys.ENTER)
        time.sleep(1)

    def select_photo_to_attach(self):
        chose_photos_attached_button = self.driver.find_element(
            By.ID, 'choose_photos_attached')
        chose_photos_attached_button.click()
        checkbox_selector = '.photo_list_bottom input[type=checkbox]'
        photo_checkboxes = self.driver.find_elements(By.CSS_SELECTOR, checkbox_selector)
        photo_checkboxes[0].click()

    def click_send_message_button(self):
        send_message_button = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name=btn_submit]')
        send_message_button.click()

    def extract_woman_name(self):
        name_link = self.driver.find_element(By.CSS_SELECTOR, 'div.f_left a')
        return name_link.text
