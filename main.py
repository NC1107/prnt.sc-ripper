from selenium import webdriver
import string
import time

alphabet = string.ascii_lowercase

digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

driver = webdriver.Chrome(executable_path="driver/chromedriver_win32 (1)/chromedriver.exe")


def GetScreenshot():
    pass


def RipImages(amount):
    count = 0
    for letter1 in alphabet:
        for letter2 in alphabet:
            for num1 in digits:
                for num2 in digits:
                    for num3 in digits:
                        for num4 in digits:
                            driver.get(f"https://prnt.sc/{letter1}{letter2}{num1}{num2}{num3}{num4}")
                            image = driver.find_element_by_xpath("/html/body/div[3]/div/div").screenshot(
                                f"images/{letter1}{letter2}{num1}{num2}{num3}{num4}.png")
                            count += 1
                            if count == amount:
                                quit()


if __name__ == '__main__':
    RipImages(100000)
    driver.quit()
