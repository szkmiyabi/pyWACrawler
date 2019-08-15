from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.alert import Alert

# browser起動
options = ChromeOptions()
options.executable_path = "/usr/bin/google-chrome"
options.add_argument("--headless")
wd = webdriver.Chrome(options=options)

# googleにアクセス
wd.get("https://www.yahoo.co.jp/")

# htmlを取得し表示する
html = wd.page_source
print(html)

# browser終了
wd.quit()