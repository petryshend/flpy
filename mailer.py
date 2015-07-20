from selenium import webdriver
from selenium.webdriver.common.by import By


class Mailer:

    base_url = 'http://www.foreignladies.com'
    username = 'LugaAgency'
    password = 'range683zip'

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.women_send_intro_links = []

    def start(self):
        print 'Start Mailer'
        self.open_home_page()
        self.go_to_login_page()
        self.submit_login_form()
        self.submit_agree_with_rules_form()
        self.go_to_women_list()
        self.collect_women_search_profile_links()
        for woman_link in self.women_send_intro_links:
            self.send_letters_for_woman(woman_link)

    def open_home_page(self):
        self.driver.get(self.base_url)

    def go_to_login_page(self):
        login_link_text = 'Affiliate Login'
        login_link = self.driver.find_element(By.LINK_TEXT, login_link_text)
        login_link.click()

    def submit_login_form(self):
        username_input = self.driver.find_element(By.ID, 'logins_ident')
        username_input.send_keys(self.username)

        password_input = self.driver.find_element(By.ID, 'logins_password')
        password_input.send_keys(self.password)

        submit_button = self.driver.find_element(By.NAME, 'btn_submit')
        submit_button.click()

    def submit_agree_with_rules_form(self):
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



