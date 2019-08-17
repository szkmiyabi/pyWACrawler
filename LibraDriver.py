from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import lxml.html
import html
from TextUtil import TextUtil
from FileUtil import FileUtil
from DateUtil import DateUtil

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
        self.guideline_file_name = "guideline_datas.txt"
        self.rep_data = []

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
    
    # rep_dataのゲッター
    def getRepData(self):
        return self.rep_data
    
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
        return self.rep_detail_url_base + self.projectID + "/controlID/"  + pageID + "/guideline/" + guidelineID + "/"
    
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
    
    # レポート詳細ページから検査結果データを生成
    def get_detail_table_data(self, pageID, pageURL, guideline):
        datas = []
        dom = self.get_dom()
        tbl = dom.xpath("/html/body/div[2]/div[2]/table")[0]
        cnt = 0
        for row in tbl.cssselect("tr"):
            cnt += 1
            if cnt < 2:
                pass
            else:
                tr = lxml.html.tostring(row).decode()
                trdom = lxml.html.fromstring(tr)
                row_datas = []
                row_datas.append(pageID)
                row_datas.append(pageURL)
                row_datas.append(guideline)
                for irow in trdom.cssselect("td"):
                    td_val = irow.text_content()
                    if td_val is None:
                        if self._is_including_tag(irow) is True:
                            row_datas.append(self._get_regx_text(irow))
                        else:
                            row_datas.append("")
                    else:
                        row_datas.append(td_val.strip())
                datas.append(row_datas)
        return datas

    def _is_including_tag(self, elm):
        tag_str = html.unescape(lxml.html.tostring(elm).decode())
        if re.search(r'<td.*?>(.+)</td>', tag_str.strip(), re.DOTALL):
            return True
        else:
            return False

    def _get_regx_text(self, elm):
        tag_str = html.unescape(lxml.html.tostring(elm).decode())
        tag_str = re.sub(r'(\r|\n|\r\n|\t|\s{2,})', "", tag_str)
        return re.search(r'<td.*?>(.+)</td>', tag_str.strip(), re.DOTALL).group(1)
    
    def _debug_print(self, data):
        for r in data:
            for c in r:
                print(c)

    # レポートデータ生成
    def fetch_report_sequential(self):

        # header
        self.rep_data.extend(TextUtil.get_header())

        self.wd.get(self.rep_index_url_base + self.projectID + "/")
        DateUtil.app_sleep(self.shortWait)

        guideline_rows = FileUtil.open_text_data(self.guideline_file_name)
        page_rows = self.get_page_list_data()

        # guidelineのループ
        for guideline in guideline_rows:
            guideline_disp = guideline
            if TextUtil.is_jis2016_lower(guideline) is False:
                guideline = "7." + guideline
            else:
                pass
            # pageのループ
            for key, value in page_rows.items():
                pageID = key
                pageURL = value
                print(pageID + ". " + guideline_disp + " を処理しています。(" + DateUtil.get_logtime() + ")")
                path = self.fetch_report_detail_path(pageID, guideline)
                self.wd.get(path)
                DateUtil.app_sleep(self.shortWait)
                self.rep_data.extend(self.get_detail_table_data(pageID, pageURL, guideline))
    
    # ページIDとガイドラインIDを個別に指定してレポートデータ生成
    def fetch_report_single(self, any_pageID, any_guideline):
        self.wd.get(self.rep_index_url_base + self.projectID + "/")
        DateUtil.app_sleep(self.shortWait)

        # 処理対象PIDデータの処理
        qy_page_rows = []
        new_page_rows = {}
        page_rows = self.get_page_list_data()
        if any_pageID == "":
            new_page_rows = page_rows
        else:
            # ループ用PIDマップの生成
            if TextUtil.is_csv(any_pageID) is True:
                tmp_arr = any_pageID.split(",")
                for r in tmp_arr:
                    qy_page_rows.append(r)
            else:
                qy_page_rows.append(any_pageID)
            for tmp_pid in qy_page_rows:
                for key, value in page_rows.items():
                    if tmp_pid == key:
                        new_page_rows[key] = value
            if len(new_page_rows) < 1:
                print("-p オプションで指定したPIDが存在しません。処理を停止します。")
            else:
                pass

        # 処理対象ガイドラインデータの処理
        guideline_rows = []
        if any_guideline == "":
            guideline_rows = FileUtil.open_text_data(self.guideline_file_name)
        else:
            if TextUtil.is_csv(any_guideline) is True:
                tmp_arr = any_guideline.split(",")
                for r in tmp_arr:
                    guideline_rows.append(r)
            else:
                guideline_rows.append(any_guideline)
        
        # header
        self.rep_data.extend(TextUtil.get_header())

        # guidelineのループ
        for guideline in guideline_rows:
            guideline_disp = guideline
            if TextUtil.is_jis2016_lower(guideline) is False:
                guideline = "7." + guideline
            else:
                pass
            # pageのループ
            for key, value in new_page_rows.items():
                pageID = key
                pageURL = value
                print(pageID + ". " + guideline_disp + " を処理しています。(" + DateUtil.get_logtime() + ")")
                path = self.fetch_report_detail_path(pageID, guideline)
                self.wd.get(path)
                DateUtil.app_sleep(self.shortWait)
                self.rep_data.extend(self.get_detail_table_data(pageID, pageURL, guideline))

