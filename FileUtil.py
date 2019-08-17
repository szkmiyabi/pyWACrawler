import yaml
import datetime

class FileUtil:

    # 設定データファイルの読み込み
    @staticmethod
    def getUserProperties(filename):
        datas = []
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            datas.append(data["uid"])
            datas.append(data["pswd"])
            datas.append(data["systemWait"])
            datas.append(data["longWait"])
            datas.append(data["midWait"])
            datas.append(data["shortWait"])
            datas.append(data["driver"])
            datas.append(data["guidelineLevel"])
        return datas
    
    # テキストデータを読み込み
    @staticmethod
    def open_text_data(filename):
        datas = []
        with open(filename) as f:
            datas = [s.strip() for s in f.readlines()]
        return datas

    # 配列をテキストデータとして書き込み
    @staticmethod
    def write_text_data(rows, filename):
        lines = [s + '\n' for s in rows]
        with open(filename, "w") as f:
            f.writelines(lines)
    
    # ユニークなディレクトリ名を取得
    @staticmethod
    def get_save_directory(prefix):
        if prefix is not "":
            prefix = prefix + "-"
        datetime_fmt = datetime.datetime.today()
        body = datetime_fmt.strftime("%Y%m%d-%H%M%S")
        return prefix + body + "/"


