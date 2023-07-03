from flask import Flask, request, render_template
import xmltodict
import json
import pandas

app = Flask(__name__)


def flatten_json(y):
    out = {}

    def flatten(x, name=''):

        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:

            for a in x:
                flatten(x[a], name + a + '_')

        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:

            i = 0

            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# def make_comparable_keys(dictionary: dict):
#     keys_list = list(dictionary.keys())
#     comparable_keys_list = []
#
#     for key in keys_list:
#


def make_nice_keys(dictionary: dict, dividing_string: str):
    keys_list = list(dictionary.keys())
    nice_keys_list = []

    for key in keys_list:
        nice_key = key.split(dividing_string)[-1]
        nice_keys_list.append(nice_key)

    new_nice_dictionary = dict(zip(nice_keys_list, list(dictionary.values())))

    return new_nice_dictionary


def same_value_key_pairs(dictionary1: dict, dictionary2: dict):
    d1_keys = set(dictionary1.keys())
    d2_keys = set(dictionary2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    same = set(o for o in shared_keys if dictionary1[o] == dictionary2[o])
    return same


def different_value_key_pairs(dictionary1: dict, dictionary2: dict):
    d1_keys = set(dictionary1.keys())
    d2_keys = set(dictionary2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    different = {o: (dictionary1[o], dictionary2[o]) for o in shared_keys if dictionary1[o] != dictionary2[o]}
    return different


def convert_all_values_to_string(dictionary: dict):
    transformed_dictionary = dictionary
    for key in transformed_dictionary:
        transformed_dictionary[key] = str(transformed_dictionary[key])
    return transformed_dictionary


@app.route("/upload")
def upload_file():

    return render_template("upload.html")


@app.route("/uploader-oba", methods=['GET', 'POST'])
def upload_oba():
    if request.method == "POST":
        uploaded_xml = request.files["file1"].read().decode("utf-8")
        uploaded_json = request.files["file2"].read().decode("utf-8")
        uploaded_xml_dict = make_nice_keys(dictionary=flatten_json(xmltodict.parse(uploaded_xml)), dividing_string=":")
        uploaded_json_dict = convert_all_values_to_string(make_nice_keys(dictionary=flatten_json(json.loads(uploaded_json)), dividing_string="_"))

        same_values = same_value_key_pairs(uploaded_json_dict, uploaded_xml_dict)
        different_values = different_value_key_pairs(uploaded_json_dict, uploaded_xml_dict)

        same_values_panda_df = pandas.DataFrame(data=same_values).rename(columns={0: "Hodnoty jsou stejné pro:"})
        table_same_values = same_values_panda_df.to_html(classes=["table",
                                                                  "table-bordered",
                                                                  "table-striped",
                                                                  "table-hover"], index=False)

        different_values_panda_df = pandas.DataFrame(data=different_values)
        table_different_values = different_values_panda_df.T.rename(columns={0: "JSON:", 1: "XML"}).to_html(classes=["table",
                                                                                                                     "table-bordered",
                                                                                                                     "table-striped",
                                                                                                                     "table-hover",
                                                                                                                     "width="])

        return render_template("upload.html",
                               xml_to_show=uploaded_xml,
                               json_to_show=uploaded_json,
                               uploaded_xml_dict=uploaded_xml_dict,
                               uploaded_json_dict=uploaded_json_dict,
                               same_values=same_values,
                               different_values=different_values,
                               table_same_values=table_same_values,
                               table_different_values=table_different_values
                               )


if __name__ == '__main__':
    app.run(debug=True)
