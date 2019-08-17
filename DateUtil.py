import datetime
import time

class DateUtil:

    # 現在の日付時刻文字列生成
    @staticmethod
    def fetch_now_datetime():
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S")

    # 現在の時刻からファイル名を生成
    @staticmethod
    def fetch_filename_from_datetime(extension):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S") + "." + extension
    
    # ログ出力の時刻文字列を生成
    @staticmethod
    def get_logtime():
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d %H:%M:%S")

    # アプリのスリープ
    @staticmethod
    def app_sleep(second):
        time.sleep(second)