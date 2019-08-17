from LibraDriver import LibraDriver
from FileUtil import FileUtil
from DateUtil import DateUtil
from TextUtil import TextUtil
from JsUtil import JsUtil
import os

class PreSvMain:

    # メイン処理
    @staticmethod
    def do_exec(projectID, any_pageID):
        # 設定データロード
        user_data = FileUtil.getUserProperties("user.yaml")
        uid = user_data[0]
        pswd = user_data[1]
        systemWait = user_data[2]
        longWait = user_data[3]
        midWait = user_data[4]
        shortWait = user_data[5]
        driver_type = user_data[6]
        appWait = [systemWait, longWait, midWait, shortWait]

        # LibraDriverインスタンスの生成
        lrp = LibraDriver(uid, pswd, projectID, appWait, driver_type)

        # ログイン
        lrp.login()
        DateUtil.app_sleep(shortWait)

        # レポートインデックスページ
        lrp.browse_repo()
        DateUtil.app_sleep(shortWait)

        # PID＋URL一覧データ取得
        page_rows = lrp.get_page_list_data()

        # 条件分岐
        qy_page_rows = []
        new_page_rows = {}
        if any_pageID == "":
            new_page_rows = page_rows
        else:
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

        # ログアウト+Libraリソース取得
        lrp.logout()
        wd = lrp.getWd()

        # directory作成
        save_dir = FileUtil.get_save_directory(projectID)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # PIDのループ処理
        for key, value in new_page_rows.items():
            pageID = key
            pageURL = value
            print(pageID + " を処理しています。(" + DateUtil.get_logtime() + ")")
            wd.get(pageURL)
            lrp.fullpage_screenshot(save_dir + pageID + ".png")

            # alt属性値明示
            wd.execute_script(JsUtil.image_alt())
            # target属性値明示
            wd.execute_script(JsUtil.target_attr())

            # screenshot
            lrp.fullpage_screenshot(save_dir + pageID + ".alt.target.png")

        # シャットダウン
        lrp.shutdown()


        

