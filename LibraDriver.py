from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import lxml.html
import html

class LibraDriver:

    # コンストラクタ
    def __init__(self, uid, pswd, projectID, appWait, driver_type):
        self.uid = uid
        self.pswd = pswd
        self.projectID = projectID
        self.systemWait = appWait[0]
        self.longWait = appWait[1]
        self.midWait = appWait[2]
        self.shortWait = appWait[3]
        self.app_url = "https://accessibility.jp/libra/"
        self.index_url = "https://jis.infocreate.co.jp/"
        self.rep_index_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/report/projID/"
        self.rep_detail_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/report2/projID/"
        self.sv_mainpage_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/index/projID/"

        # driverオプションの設定
        if driver_type == "chrome":
            options = ChromeOptions()
            options.executable_path = "/usr/bin/google-chrome"
            options.add_argument("--headless")
            self.wd = webdriver.Chrome(options=options)
        else:
            pass

        self.wd.implicitly_wait(self.systemWait)
        self.wd.set_window_size(1280, 900)
        self.wd.get(self.app_url)
    
    # wdのゲッター
    def getWd(self):
        return self.wd
    
    # screenshotを撮る
    def screenshot(self, filename):
        self.wd.save_screenshot(filename)
    
    # シャットダウン
    def shutdown(self):
        self.wd.quit()
    
    # ログイン
    def login(self):
        self.wd.find_element_by_id("uid").send_keys(self.uid)
        self.wd.find_element_by_id("pswd").send_keys(self.pswd)
        self.wd.find_element_by_id("btn").click()
    
    # ログアウト
    def logout(self):
        self.wd.get(self.index_url)
        time.sleep(self.shortWait)
        btnWrap = self.wd.find_element_by_id("btn")
        btnBase = btnWrap.find_element_by_tag_name("ul")
        btnBaseInner = btnBase.find_element_by_class_name("btn2")
        btnA = btnBaseInner.find_element_by_tag_name("a")
        btnA.click()
    
    # レポートインデックスページに遷移
    def browse_repo(self):
        self.wd.get(self.rep_index_url_base + self.projectID)
    
    # レポート詳細ページのURL生成
    def fetch_report_detail_path(self, pageID, guidelineID):
        return rep_detail_url_base + projectID + "/controlID/"  + pageID + "/guideline/" + guidelineID + "/"
    
    # DOMオブジェクトを取得
    def get_dom(self):
        html_str = self.wd.page_source
        return lxml.html.fromstring(html_str)
    
    # PID+URL一覧データ生成
    def get_page_list_data(self):
        datas = {}
        dom = self.get_dom()
        tbl = dom.xpath("/html/body/div[2]/div[1]/table")[0]
        rows = tbl.cssselect("tr td:first-child")
        pids = []
        for row in rows:
            td_val = row.text
            pids.append(td_val)
        map_cnt = len(pids)
        rows = tbl.cssselect("tr td:nth-child(2)")
        urls = []
        for row in rows:
            td_val = row.text
            urls.append(td_val)
        for i in range(0, map_cnt - 1):
            datas[pids[i]] = urls[i]
        return datas