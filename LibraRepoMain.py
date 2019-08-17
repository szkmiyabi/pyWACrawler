from LibraDriver import LibraDriver
from FileUtil import FileUtil
from DateUtil import DateUtil
from TextUtil import TextUtil
from ExcelUtil import ExcelUtil

class LibraRepoMain:

    # 検査結果レポートメイン処理
    @staticmethod
    def do_report(projectID, any_pageID, any_guideline):

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

        # 条件分岐
        if any_pageID == "" and any_guideline == "":
            lrp.fetch_report_sequential()
        else:
            lrp.fetch_report_single(any_pageID, any_guideline)
        
        # ログアウト
        lrp.logout()
        DateUtil.app_sleep(shortWait)
        lrp.shutdown()

        rep_data = lrp.getRepData()

        print("Excel書き出し処理に移ります。(" + DateUtil.get_logtime() + ")")
        ExcelUtil.save_xlsx(rep_data)
        print("Excel書き出し処理が完了しました。(" + DateUtil.get_logtime() + ")")
    
    # guidelineデータを初期化
    @staticmethod
    def do_reset_guideline():

        # 設定ファイルの読み込み
        user_data = FileUtil.getUserProperties("user.yaml")
        gLevel = user_data[7]

        # 書き出し内容を配列で制御
        gA = ["1.1.1","1.2.1","1.2.2","1.2.3","1.3.1","1.3.2","1.3.3","1.4.1","1.4.2","2.1.1","2.1.2","2.2.1","2.2.2","2.3.1","2.4.1","2.4.2","2.4.3","2.4.4","3.1.1","3.2.1","3.2.2","3.3.1","3.3.2","4.1.1","4.1.2"]
        gAA = ["1.2.4","1.2.5","1.4.3","1.4.4","1.4.5","2.4.5","2.4.6","2.4.7","3.1.2","3.2.3","3.2.4","3.3.3","3.3.4"]
        gAAA = ["1.2.6","1.2.7","1.2.8","1.2.9","1.4.6","1.4.7","1.4.8","1.4.9","2.1.3","2.2.3","2.2.4","2.2.5","2.3.2","2.4.8","2.4.9","2.4.10","3.1.3","3.1.4","3.1.5","3.1.6","3.2.5","3.3.5","3.3.6"]
        guideline_names = []
        if gLevel == "A":
            guideline_names = gA
        elif gLevel == "AA":
            guideline_names = gA + gAA
        else:
            guideline_names = gA + gAA + gAAA
        
        # テキストデータ書き込み
        FileUtil.write_text_data(guideline_names, "guideline_datas.txt")