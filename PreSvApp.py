from PreSvMain import PreSvMain
from TextUtil import TextUtil
from DateUtil import DateUtil
import sys
import argparse

projectID = ""
any_pageID = ""
args_flag = True

options = argparse.ArgumentParser()
options.add_argument('-t', help='projectID')
options.add_argument('-p', help='pageID')
args = options.parse_args()

if args.t is not None:
    projectID = args.t
if args.p is not None:
    any_pageID = args.p

if projectID == "" and any_pageID == "":
    args_flag = False

if args_flag is True:
    # report処理
    if projectID is not "":
        if TextUtil.is_projectID(projectID) is True:
            print("処理を開始します。(" + DateUtil.get_logtime() + ")")
            PreSvMain.do_exec(projectID, any_pageID)
            print("処理を完了します。(" + DateUtil.get_logtime() + ")")
        else:
            print("不正なプロジェクトIDが指定されました。処理を中止します。")
else:
    print("コマンドライン引数が指定されていないため処理を開始できません。")