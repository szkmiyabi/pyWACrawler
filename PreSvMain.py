from LibraDriver import LibraDriver
from FileUtil import FileUtil
from DateUtil import DateUtil
from TextUtil import TextUtil
from JsUtil import JsUtil
import os

class PreSvMain:

    # メイン処理
    @staticmethod
    def do_exec(projectID, any_pageID, any_operation, layered_flag):
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
        save_dir = FileUtil.get_save_directory(projectID + "-presv")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # operation配列の整備
        operations = []
        if TextUtil.is_csv(any_operation) is True:
            tmp_arr = any_operation.split(",")
            for r in tmp_arr:
                operations.append(r)
        else:
            operations.append(any_operation)

        # PIDのループ処理
        for key, value in new_page_rows.items():
            pageID = key
            pageURL = value
            print(pageID + " を処理しています。(" + DateUtil.get_logtime() + ")")
            wd.get(pageURL)
            lrp.fullpage_screenshot(save_dir + pageID + ".png")

            # operation配列のループ処理
            for opt in operations:
                if opt == "css-cut" or opt == "cc":
                    wd.execute_script(JsUtil.css_cut())
                elif opt == "document-link" or opt == "dl":
                    wd.execute_script(JsUtil.document_link())
                elif opt == "image-alt" or opt == "ia":
                    wd.execute_script(JsUtil.image_alt())
                elif opt == "lang-attr" or opt == "la":
                    wd.execute_script(JsUtil.lang_attr())
                elif opt == "semantic-check" or opt == "sc":
                    wd.execute_script(JsUtil.semantic_check())
                elif opt == "tag-label-and-title-attr" or opt == "tl-ta":
                    wd.execute_script(JsUtil.tag_label_and_title_attr())
                elif opt == "target-attr" or opt == "ta":
                    wd.execute_script(JsUtil.target_attr())
                # layered=falseなら個別screenshot
                if layered_flag is False:
                    lrp.fullpage_screenshot(save_dir + pageID + "." + opt + ".png")
                    wd.get(pageURL) # reload

            # layered=trueなら最後でscreenshot
            if layered_flag is True:
                sufix = ""
                for cop in operations:
                    sufix = sufix + cop + "."
                lrp.fullpage_screenshot(save_dir + pageID + "." + sufix + "png")

        # シャットダウン
        lrp.shutdown()


        

