from PreSvMain import PreSvMain
from TextUtil import TextUtil
from DateUtil import DateUtil
import sys
import argparse

projectID = ""
any_pageID = ""
any_operation = ""
layered_flag = True
args_flag = True

options = argparse.ArgumentParser()
options.add_argument('-t', help='projectID')
options.add_argument('-p', help='pageID')
options.add_argument('-o', help='operation')
options.add_argument('-l', help='layered')
args = options.parse_args()

if args.t is not None:
    projectID = args.t
if args.p is not None:
    any_pageID = args.p
if args.o is not None:
    any_operation = args.o
if args.l is not None and args.l == "no":
    layered_flag = False


if projectID == "" and any_pageID == "" and any_operation == "":
    args_flag = False

if args_flag is True:
    # report処理
    if projectID is not "":
        if TextUtil.is_projectID(projectID) is True:
            print("処理を開始します。(" + DateUtil.get_logtime() + ")")
            PreSvMain.do_exec(projectID, any_pageID, any_operation, layered_flag)
            print("処理を完了します。(" + DateUtil.get_logtime() + ")")
        else:
            print("不正なプロジェクトIDが指定されました。処理を中止します。")
else:
    print("コマンドライン引数が指定されていないため処理を開始できません。")