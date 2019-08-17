from LibraDriver import LibraDriver
from FileUtil import FileUtil
from DateUtil import DateUtil
from TextUtil import TextUtil

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

# LibraDriverインスタンス
lrp = LibraDriver(uid, pswd, "551", appWait, driver_type)

# Libraログイン
lrp.login()
DateUtil.app_sleep(shortWait)
print(DateUtil.get_logtime() + "login")

# レポートインデックスページに遷移
lrp.browse_repo()
DateUtil.app_sleep(shortWait)
print(DateUtil.get_logtime() + "report index")

# PID＋URL一覧データ取得
datas = lrp.get_page_list_data()

# Libraログアウト
lrp.logout()
DateUtil.app_sleep(shortWait)
print(DateUtil.get_logtime() + "logout")

# Libraシャットダウン
lrp.shutdown()
print(DateUtil.get_logtime() + "shutdown")

# PID＋URL一覧を表示
for key, value in datas.items():
    print(key, value)

