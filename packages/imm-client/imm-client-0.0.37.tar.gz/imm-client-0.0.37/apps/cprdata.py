from typing import final
from source.excel import Excel
from utils.utils import age
import json, dotenv, os, argparse
import os
from apps.config import print_errors, show_success, show_error
from apps.imm_api import imm_api_post
from datetime import datetime
import os
from apps.config import (
    console,
    error_style,
    success_style,
    show_error,
    print_errors,
    getJsonData,
)
from pathlib import Path
from functools import reduce
from utils.utils import append_ext
import shutil

excels = ["0008", "5669", "5562", "5406"]


def make_pr_excel(filename, language):

    # Create a temp directory
    temp_dir = Path(str(datetime.timestamp(datetime.now())))
    os.makedirs(temp_dir)

    try:
        # create forms seperately
        for model in excels:
            data = {"model": model, "language": language}
            r = imm_api_post("case/make", data)
            if r.status_code == 401:
                console.print(r.json().get("detail"), style=error_style)
                return
            output_excel_name = temp_dir / f"{model}.xlsx"
            with open(output_excel_name, "wb") as f:
                f.write(r.content)

        # merge forms
        es = [Excel(temp_dir / f"{e}.xlsx", language=language) for e in excels]
        e = reduce(lambda a, b: a + b, es)
        filename = append_ext(filename, ".xlsx")
        e.makeExcel(filename, protection=True)
        console.print(f"{filename} has been created", style=success_style)
    finally:
        # delete temp directory
        shutil.rmtree(temp_dir)


def check_pr_excel(filename, language):
    """Check input excel based on model"""
    excel_name = append_ext(filename, ".xlsx")
    for model in excels:
        data = {"model": model, "data": getJsonData(excel_name), "language": language}
        r = imm_api_post("case/check", data)

        if r.status_code == 200:
            console.print(r.json()[f"success for {model} check."], style=success_style)
        else:
            console.print(f"{model} check failed:", style=error_style)
            print_errors(r)


def getAppActions(pa):
    request = {"pa": pa.plain_dict}
    r = imm_api_post("pr/pickapp", request)
    if r.status_code == 200:
        return r.json()
    else:
        print_errors(r)
        return []


def getFormActions(pa, sp, dps, model):
    request = {
        "pa": pa.plain_dict,
        "sp": sp.plain_dict if sp else None,
        "dps": [dp.plain_dict for dp in dps],
        "model": model,
    }
    r = imm_api_post("pr/webform", request)
    if r.status_code == 200:
        return r.json()
    else:
        print_errors(r)
        return []


def login_prportal(rcic: str):
    # login
    path = os.path.abspath(os.path.join(os.path.expanduser("~"), ".immenv"))
    config = dotenv.dotenv_values(path)
    rcic = rcic or config.get("rcic")
    if not rcic:
        show_error(
            "You did not speficy using which rcic's portal. Please use -r rcic name"
        )
        return
    rcic_account = {
        "account": config.get(rcic + "_prportal_account"),
        "password": config.get(rcic + "_prportal_password"),
    }
    if not rcic_account["account"] or not rcic_account["password"]:
        show_error(
            f"{rcic}'s prportal account and/or password is not existed. Check the .immenv file in your home directory and add your profile"
        )
        exit(1)

    r = imm_api_post("pr/login", rcic_account)
    if r.status_code == 200:
        return r.json()
    else:
        print_errors(r)
        return []


def output(args, actions):
    if args.to:
        filename = append_ext(args.to, ".json")
        with open(filename, "w") as f:
            json.dump(actions, f, indent=3, default=str)
            show_success(f"{filename} is created")
    else:
        show_success(json.dumps(actions, indent=3, default=str))


def makeDocx(persons, docx_file):
    request = {"context": persons, "language": "English"}
    r = imm_api_post("pr/appendix", request)

    if r.status_code == 200:
        with open(docx_file, "wb") as f:
            f.write(r.content)
        show_success(f"{docx_file} has been downloaded from web")
    else:
        print_errors(r)


def is_above_18(dp):
    person = dp.dict.get("personal")
    dob = person.get("dob")
    return True if age(dob) else False


def main():
    parser = argparse.ArgumentParser(
        description="Used for generating data for webform filling."
    )
    # input source excel files for pa, sp, and dp
    parser.add_argument(
        "-pa",
        "--principal_applicant",
        help="Input principal applicant's excel file name. '.xlsx' is optional",
    )
    parser.add_argument(
        "-sp", "--spouse", help="Input spouse's excel file name.'.xlsx' is optional"
    )
    parser.add_argument(
        "-dp",
        "--dependants",
        help="Input dependants' excel file names, can be multiple.'.xlsx' is optional",
        nargs="+",
    )
    # get which rcic
    parser.add_argument("-r", "--rcic", help="Input rcic's name")
    # generate data for filling all, or specific form
    parser.add_argument(
        "-f",
        "--forms",
        help="Specify generating which form. Exp: -f 5669 5562 0008 5406. Without -f, the app will generate all forms' data ",
        nargs="+",
    )
    # save to file
    parser.add_argument(
        "-t", "--to", help="Input the output json file name'.json' is optional"
    )

    # make an additional appendix docx file including all information
    parser.add_argument(
        "-a", "--appendix", help="Input the appendix file name'.docx' is optional"
    )
    parser.add_argument(
        "-m",
        "--make",
        help="make an Excel for PR data input, '.xlsx' is optional",
    )
    parser.add_argument(
        "-check",
        "--check",
        help="Check an Excel for PR data, '.xlsx' is optional",
    )
    parser.add_argument(
        "-l", "--language", help="make an Excel with language. Default is English"
    )

    args = parser.parse_args()
    if args.make:
        language = args.language or "English"
        make_pr_excel(args.make, language)
        return

    if args.check:
        language = args.language or "English"
        check_pr_excel(args.check, language)
        return

    # get pa, sp, and dps object
    if args.principal_applicant:
        pa_excel = append_ext(args.principal_applicant, ".xlsx")
        pa = Excel(pa_excel)
    else:
        show_error(
            "You didn't input principal applicant's excel file. Please use -pa excel.xlsl"
        )

    if args.spouse:
        sp_excel = append_ext(args.spouse, ".xlsx")
        sp = Excel(sp_excel)
    else:
        sp = None

    dps = []
    if args.dependants:
        dp_excels = append_ext(args.dependants, ".xlsx")
        for excel in dp_excels:
            dps.append(Excel(excel))

    # make appendix doc file
    if args.appendix:
        dps_above_18 = [dp.plain_dict for dp in dps if is_above_18(dp)]
        sp = [sp.plain_dict] if sp else []
        makeDocx([pa.plain_dict, *sp, *dps_above_18], args.appendix)
        return
    # actions container
    actions = []

    actions += login_prportal(args.rcic)
    # pick an existing application.
    actions += getAppActions(pa)

    # if args.form exists, then loop the form and generate them, else generate all forms
    if args.forms:
        a5406 = a5562 = a5669 = a0008 = []
        for form in args.forms:
            if form == "5406":
                a5406 = getFormActions(pa, sp, dps, "5406")
            elif form == "5562":
                a5562 = getFormActions(pa, sp, dps, "5562")
            elif form == "5669":
                a5669 = getFormActions(pa, sp, dps, "5669")
            elif form == "0008":
                a0008 = getFormActions(pa, sp, dps, "0008")
            else:
                show_error(
                    f"{form} is not a valid form number in '5562','5406','5669','0008'"
                )

                return
        actions += a5406 + a5562 + a5669 + a0008
        output(args, actions)
        return
    else:
        for form in ["5406", "5562", "5669", "0008"]:
            actions += getFormActions(pa, sp, dps, form)
        output(args, actions)
        return


if __name__ == "__main__":
    # pa = Excel("/Users/jacky/desktop/demo/all.xlsx")
    # sp = Excel("/Users/jacky/desktop/demo/all.xlsx")
    # dps = [pa, sp]
    # actions = []
    # actions += login_prportal("jacky")
    # # pick an existing application.
    # actions += getAppActions(pa)

    # for form in ["5406", "5562", "5669", "0008"]:
    #     actions += getFormActions(pa, sp, dps, form)
    # from pprint import pprint

    # dps_above_18 = [
    #     dp.plain_dict for dp in dps if is_above_18(dp)
    # ]  # doesn't check if it is above 18. Just for test
    # sp = [sp.plain_dict] if sp else []
    # makeDocx([pa.plain_dict, *sp, *dps_above_18], "aa.docx")

    main()
