from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from AutoTraderScraper import AutoTraderScraper as ATS
from GumTreeScraper import GumTreeScraper as GTS

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("_tt_enable_cookies=1")
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    # autotrader = ATS(driver, "DA99EZ", 20, 2012, 2014, 500, 2500, [])
    # autotrader.scrape()
    # print(autotrader.cars())
    gumtree = GTS(driver, "DA99EZ", 15, 500, 2500)
    gumtree.scrape()
    print(gumtree.cars)
