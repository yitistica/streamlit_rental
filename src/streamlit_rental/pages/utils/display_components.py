import pandas as pd


def convert_a_dict_to_table(info_dict):
    info_list = list()
    info_list.append(info_dict)
    df = pd.DataFrame(info_list).T

    return df
