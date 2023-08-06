"""
# Purpose of this file is to provide general functionalities within an application. This makes application development
# more effective. Just focus on your main tasks and dont care about the annoying interface functionalites.
"""

# **********************************************************************************************************************
# Imports
# **********************************************************************************************************************
import csv
import glob
import shutil
import time
import matplotlib.pyplot as plt
import json
import os
import datetime as dt
import pandas as pd
import requests
from PyPDF2 import PdfFileMerger
import global_vars


# **********************************************************************************************************************
# Functions
# **********************************************************************************************************************


# ----------------------------------------------------------------------------------------------------------------------
# List Operations, Convertions
# ----------------------------------------------------------------------------------------------------------------------
def calculate_quotient(dividend_data, divisor_data):
    quotient_list = [(x / y) * 100 for x, y in zip(dividend_data, divisor_data)]

    return quotient_list


def keep_every_nth(start, lst, n):
    a = lst[start::n]
    return a


def reverse_lists(x: list, y: list) -> tuple:
    x = x[::-1]
    y = y[::-1]

    return x, y


def convert_list_elements_to_float(y):
    y_converted = []
    for x in y:
        x = float(x)
        y_converted.append(x)
    return y_converted


def convert_list_of_strings_to_int(y):
    return [int(float(x)) for x in y]


def convert_list_elements_to_date_instance(dates_as_strings):
    dates_as_dates = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates_as_strings]

    return dates_as_dates


def convert_to_date(dates_as_string):
    date_as_dates = dt.datetime.strptime(dates_as_string, '%Y-%m-%d').date()

    return date_as_dates


# ----------------------------------------------------------------------------------------------------------------------
# String Operations
# ----------------------------------------------------------------------------------------------------------------------
def split_indicator_in_two(indicator):
    dividend_str = indicator.split('_to_')[0]
    divisor_str = indicator.split('_to_')[1]

    return dividend_str, divisor_str


def split_line(line):
    a = line.split(',')[0]
    b = line.split(',')[1]

    return a, b


def remove_string(line):
    return line[:-2]


# ----------------------------------------------------------------------------------------------------------------------
# File Operations
# ----------------------------------------------------------------------------------------------------------------------
def read_data_from_file(filename):
    try:
        if os.path.isfile(filename):
            with open(filename) as json_file:
                data = json.load(json_file)
                return data

    except FileExistsError:
        print("File does not exist")


def read_lines_data_from_file(filename):
    try:
        if os.path.isfile(filename):
            with open(filename) as file:
                lines = file.readlines()
                return lines

    except FileExistsError:
        print("File does not exist")


def write_to_file_in_csv_format(data, name_of_file: str) -> None:
    f = open(name_of_file, "w")
    f.write(str(data))
    f.close()


def write_to_file_in_json_format(data, name_of_file: str) -> None:
    try:
        f = open(name_of_file, "w")
        json_data = json.dumps(data, indent=4)
        f.write(str(json_data))
        f.close()
    except Exception as e:
        print(f"{e} ## Serialization was not successful for file: {name_of_file}")


def pdf_merger(path):
    merger = PdfFileMerger()

    os.chdir(path)
    for file in glob.glob("*.pdf"):
        merger.append(file)

    merger.write(path + "\\result.pdf")
    merger.close()


def delete_all_lines_from_file():
    with open(global_vars.filepath_my_json + "\\atestsite.html", "w") as file:
        file.truncate()


def add_file_to_main_html_file(indicator, complete_string):
    f = open(global_vars.filepath_my_json + '\\atestsite.html', 'a')

    message = """
    <html>
       <center>
        <figure>
            <figcaption> {} im Quartal </figcaption>
            <img src="{}" vspace=30 alt="my img"/>    
        </figure>
       </center>
    </html>
    """.format(indicator, complete_string)

    f.write(message)
    f.close()
    pass


def save_figure(path, indicator):
    complete_string_svg = path + f"\\plot_{indicator}" + ".svg"
    complete_string_pdf = path + f"\\plot_{indicator}" + ".pdf"

    plt.tight_layout()
    plt.savefig(complete_string_svg, dpi=300, bbox_inches="tight")
    plt.savefig(complete_string_pdf, dpi=300, bbox_inches="tight")

    # add_file_to_main_html_file(indicator, complete_string_svg)
    pass


def get_file_age_in_hours(filepath) -> float:
    delta = time.time() - os.path.getmtime(filepath)
    delta_in_hours = delta / 3600
    return delta_in_hours


def copy_and_rename_file(src_file, dest_file):
    shutil.copy(src_file, dest_file)


# ----------------------------------------------------------------------------------------------------------------------
# CSV File Processing
# ----------------------------------------------------------------------------------------------------------------------

def convert_and_save_to_csv(data, name_of_file):
    data_csv = data.to_csv()
    write_to_file_in_csv_format(data_csv, name_of_file)


def yahoo_csv_data_formatting(file):
    # this function makes some operations on csv data
    csvreader = csv.reader(file)
    header = next(csvreader)

    # remove list elements which are empty
    header = list(filter(None, header))

    # extract rows and filter empty lists from the base list
    rows = []
    for row in csvreader:
        rows.append(row)

    rows = list(filter(None, rows))

    # remove spaces from indicators
    for row in rows:
        row_stripped = row[0].replace(" ", "")

        row[0] = row_stripped

    return header, rows


# ----------------------------------------------------------------------------------------------------------------------
# Plotting Data with Matplotlib
# ----------------------------------------------------------------------------------------------------------------------
def only_plot(data):
    plt.figure()

    x = data[0]
    y = data[1]

    if len(x) == len(y):
        plt.plot(x, y, )
        plt.scatter(x, y)

    plt.legend()
    plt.show()


def merge_csv_files(file_list, symbol_list):
    try:
        for idx, symbol in enumerate(symbol_list):
            destination_file_path = os.getcwd() + + "total_data_" + symbol + ".csv"

            frames = [pd.read_csv(f) for f in file_list]
            combined_csv = pd.concat(frames, axis="columns")
            combined_csv.to_csv(destination_file_path, index=True, encoding='utf-8-sig')
            print("merge was successful")
            return destination_file_path
    except:
        print("merge failed!")


def merge_json_file_list(file_list, symbol_list):
    for idx, symbol in enumerate(symbol_list):
        dest_file = global_vars.filepath_yahoo + "yahoo_total_data_" + symbol + ".json"

        # copy and rename the first file
        copy_and_rename_file(file_list[idx][0], dest_file)

        # iterate over the array but start from the second element in the array
        for item in file_list[idx][1:]:
            merge_two_json_files(dest_file, item)


def merge_two_json_files(base_file, merge_file):
    base_file_data = read_data_from_file(base_file)
    merge_file_data = read_data_from_file(merge_file)

    for quarter in merge_file_data["quarterlyReports"]:
        date = quarter["fiscalDateEnding"]

        # base_quarter is an object
        for base_quarter in base_file_data["quarterlyReports"]:

            base_date = base_quarter["fiscalDateEnding"]

            if date == base_date:
                for key_value_pair in quarter.items():

                    # Iterate over key value pairs. Add to object if not already there.
                    if key_value_pair not in base_quarter:
                        append_key_value_to_object(base_quarter, key_value_pair[0], key_value_pair[1])

    write_to_file_in_json_format(base_file_data, base_file)


# ----------------------------------------------------------------------------------------------------------------------
# Processing on JSON Data
# ----------------------------------------------------------------------------------------------------------------------

# add key value to an object
def append_key_value_to_object(obj, key, value):
    obj[key] = value

    return obj


def append_object_to_json_array(merge_object, base_object):
    base_object.append(merge_object)
    print(base_object)
    pass


def get_key_value_from_local_file(indicator, s):
    try:
        symbol_info = read_data_from_file("yahoo_info_data_" + s[0] + ".json")
        i = symbol_info[indicator]

        return i

    except Exception as e:
        print(f" {e} ### live data from yahoo failed and no locally data for {indicator} available")


def delete_object_key(json_data_object, key):
    del json_data_object[key]
    return json_data_object


def create_json_object_finance(s):
    d = {'symbol': s, "quarterlyReports": []}
    return d


def add_keys_values_to_object(list_filtered):
    # create object
    obj = {}

    for elem in list_filtered:
        # add key und value to obj
        obj[elem[0]] = elem[1]

    return obj


def extract_indicator_from_my_json_file(data_json: dict, indicator: str, symbol: str) -> list:
    reports = data_json['quarterlyReports']
    time_points = []
    value_points = []
    for i in reports:
        # i ist ein  Array
        try:
            time_points.append(i['fiscalDateEnding'])  # releaseDate
            value_points.append(i[indicator])
        except Exception as e:
            print(f" {e} ### Appending data element to array didn't work with indicator {indicator}. "
                  f"Is the indicator in the data?")
            exit()
    value_points, time_points = reverse_lists(value_points, time_points)

    data = [time_points, value_points, symbol, indicator]

    return data


def extract_quarterly_report_data(data_json: dict, indicator: str, symbol: str) -> list:
    # this function is a direct copy of extract_quarterly_report_data_from_alpha!
    # And based on the namings in alpha data
    reports = data_json['quarterlyReports']
    time_points = []
    value_points = []
    for i in reports:
        # i ist ein  Array
        try:
            time_points.append(i['fiscalDateEnding'])
            value_point = i[indicator]
            if value_point == "None":
                print(f"Analyzing of {indicator} not possible, since no data available - data == None")
            value_points.append(i[indicator])
        except Exception as e:
            print(f"{e} ## Appending data element to array didn't work with indicator {indicator}. "
                  f"Is the indicator in the data?")
            exit()
    value_points, time_points = reverse_lists(value_points, time_points)

    data = [time_points, value_points, symbol, indicator]

    return data


def get_data(input_data, indicator, symbol):
    # if you change this please also change get_float_data
    # quotient: research and development:
    try:
        list_dividend = extract_quarterly_report_data(input_data, indicator, symbol=symbol)

        # convert to int
        list_dividend_converted = convert_list_of_strings_to_int(list_dividend[1])

        data = [list_dividend[0], list_dividend_converted, symbol, indicator]

        return data
    except Exception as e:
        print(f" {e} ### Function call: get data failed - parameter:{indicator}; {symbol} ")
    return 1  # error if 1 is returned


def get_float_data(input_data, indicator, symbol):
    # if you change this please also change get_data

    # quotient: research and development:
    try:
        list_dividend = extract_quarterly_report_data(input_data, indicator, symbol=symbol)

        # convert to int
        temp_converted = convert_list_elements_to_float(list_dividend[1])
        list_dividend_converted = convert_list_of_strings_to_int(temp_converted)

        data = [list_dividend[0], list_dividend_converted, symbol, indicator]
        return data

    except Exception as e:
        print(f"{e} ## Function call: get float data failed - parameter:{indicator}; {symbol} ")
    return 1  # error if 1 is returned


def filter_data(data_list, options):
    packed_indicators = []
    indicators = []
    for i in options:
        indicator = filter(lambda x: x[3] == i, data_list)
        indicator_list = list(indicator)
        if len(indicator_list) != 0:
            packed_indicators.append(indicator_list)

    # unpacking the list because with append to indicators -
    # we have one list element too much - what we didn't have when doing list(filter(...))
    # unpack one level
    temp = packed_indicators[0]

    for i in temp:
        indicators.append(i)

    return indicators

# ----------------------------------------------------------------------------------------------------------------------
# HTTP Processes
# ----------------------------------------------------------------------------------------------------------------------

def http_basic_access_authentication():
    try:
        resp = requests.post('https://pes.ciplus.vi.vector.int/login/auth/', data={}, auth=('abc', 'abc'), verify=False)
        print(resp)
    except ValueError:
        print("Auth login didnt work")

