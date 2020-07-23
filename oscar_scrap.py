from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class scrap_oscar:

    def __init__(self):
        self.timer = 1
        self.year_row_num = 1
        url = "https://www.imdb.com/?ref_=nv_home"
        op = Options()
        op.headless = True
        op.add_argument('disable-infobars')
        op.add_argument('--window-size=1920x1080')
        self.dr = webdriver.Chrome(options = op, executable_path = 'chromedriver')
        self.dr.set_page_load_timeout(15)
        try:
            self.dr.get(url)
        except TimeoutException:
            print("Page load time crossed set limit of 15 sec")
            exit()

    def nav(self):
        self.exceptions("#imdbHeader-navDrawerOpen--desktop")
        self.dr.find_element_by_css_selector("#imdbHeader-navDrawerOpen--desktop").click()
        self.exceptions("[href='/oscars/?ref_=nv_ev_acd']")
        self.dr.find_element_by_css_selector("[href='/oscars/?ref_=nv_ev_acd']").click()
        self.dr.find_element_by_css_selector("[title='Winners']").click()
        year_row_len = len(self.dr.find_elements_by_css_selector("div.event-history-widget__years>"
                                                            "div.event-history-widget__years-row"))
        while self.year_row_num <= year_row_len:
            year_num = 1
            year_len_str = "div.event-history-widget__years>div.event-history-widget__years-row" \
                           ":nth-child(" + str(self.year_row_num) + ")>span"
            year_len = len(self.dr.find_elements_by_css_selector(year_len_str))
            while year_num <= year_len:
                selector_str = 'div.event-history-widget__years>div.event-history-widget__years-row' \
                               ':nth-child(' + str(self.year_row_num) + ')>span:nth-child(' + str(year_num) + ')>a'
                year = self.dr.find_element_by_css_selector(selector_str)
                print('Year:', year.text)
                year.click()
                try:
                    print("Oscar winner:", self.dr.find_element_by_css_selector("div.event-widgets__winner-badge"
                                                                         "+div.event-widgets__nominees>"
                                                                         "div.event-widgets__primary-nominees>span>"
                                                                         "span.event-widgets__nominee-name>a").text, "\n")
                except NoSuchElementException:
                    print("No data available this year\n")
                year_num += 1
            self.year_row_num += 1
        self.dr.quit()

    def exceptions(self, locator):
        try:
            WebDriverWait(self.dr, self.timer).until(cond.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        except NoSuchElementException:
            print("Element not visible to click")
            self.dr.quit()
            quit()

if __name__ == '__main__':
    oscar = scrap_oscar()
    oscar.nav()
