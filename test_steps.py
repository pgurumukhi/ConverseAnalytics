__author__ = 'Shridhar'
from selenium.webdriver.common.by import By
import time


def test_1(driver):
    driver.switch_to.frame(0)
    know_more = driver.find_element(By.CSS_SELECTOR, "div.adelem")
    # driver.get_screenshot_as_file("test1.png")
    know_more.click()
    time.sleep(2)
    # driver.get_screenshot_as_file("test2.png")
    close = driver.find_element(By.NAME, "closebutton 1")
    close.click()
    time.sleep(2)


