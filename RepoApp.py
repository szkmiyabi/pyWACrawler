from LibraRepoMain import LibraRepoMain
from TextUtil import TextUtil
from DateUtil import DateUtil
import sys
import argparse

projectID = ""
any_pageID = ""
any_guideline = ""
reset_guideline_flag = False
args_flag = True

options = argparse.ArgumentParser()
options.add_argument('-t', help='projectID')
options.add_argument('-p', help='pageID')
options.add_argument('-g', help='guideline')
options.add_argument('-o', help='operation_name')
args = options.parse_args()

if args.t is not None:
    projectID = args.t
if args.p is not None:
    any_pageID = args.p
if args.g is not None:
    any_guideline = args.g
if args.o is not None:
    if args.o == "reset-guideline":
        reset_guideline_flag = True

if projectID == "" and any_pageID == "" and any_guideline == "" and reset_guideline_flag is False:
    args_flag = False

if args_flag is True:
    # report処理
    if projectID is not "":
        if TextUtil.is_projectID(projectID) is True:
            print("処理を開始します。(" + DateUtil.get_logtime() + ")")
            LibraRepoMain.do_report(projectID, any_pageID, any_guideline)
            print("処理を完了します。(" + DateUtil.get_logtime() + ")")
        else:
            print("不正なプロジェクトIDが指定されました。処理を中止します。")
    else:
        # guidelineデータリセット処理
        if reset_guideline_flag is True:
            LibraRepoMain.do_reset_guideline()
else:
    print("コマンドライン引数が指定されていないため処理を開始できません。")