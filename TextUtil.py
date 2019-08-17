import re

class TextUtil:

    # brタグを改行コード変換
    @staticmethod
    def br_decode(self, data):
        return re.sub(r'<br>', "\r\n", data)
    
    # タグをデコード
    @staticmethod
    def tag_decode(data):
        res = re.sub(r'&lt;', "", data)
        res = re.sub(r'&gt;', "", res)
        return res
    
    # プロジェクトIDかどうか判定
    @staticmethod
    def is_projectID(data):
        if re.search(r'[0-9]+', data, re.DOTALL):
            return True
        else:
            return False
    
    # カンマ区切りテキストかどうか判定
    @staticmethod
    def is_csv(data):
        if re.search(r',', data, re.DOTALL):
            return True
        else:
            return False
    
    # レポートのヘッダー行を生成
    @staticmethod
    def get_header():
        return [["管理番号","URL","達成基準","状況/要件","実装番号","検査結果","検査員","コメント","対象ソースコード","修正ソースコード"]]

    # 達成基準番号をJIS2016形式に変換
    @staticmethod
    def jis2016_encode(data):
        return re.sub(r'7\.', "", data)
    
    # 達成基準番号がJIS2016以前の形式かどうか判定
    @staticmethod
    def is_jis2016_lower(data):
        if re.search(r'^7\.', data, re.DOTALL):
            return True
        else:
            return False