from flask import Flask, jsonify, request, render_template

app = Flask(__name__)



@app.route("/upload")
def upload_file():
    global uploaded_xml
    uploaded_xml = "Zatím nic"
    global uploaded_json
    uploaded_json = "Ještě taky nic"
    global uploaded_are_equal
    uploaded_are_equal = "Nevíme"
    return render_template("upload.html", xml_to_show=uploaded_xml, json_to_show=uploaded_json, same_to_show = uploaded_are_equal)


@app.route("/uploader-oba", methods = ['GET', 'POST'])
def upload_oba():
    if request.method == "POST":
        uploaded_xml = request.files["file1"].read().decode("utf-8")
        uploaded_json = request.files["file2"].read().decode("utf-8")
        if uploaded_xml == uploaded_json:
            uploaded_are_equal = "Ano, jsou stejné"
        if uploaded_xml != uploaded_json:
            uploaded_are_equal = "Ne, nejsou stejné"
        return render_template("upload.html", xml_to_show=uploaded_xml, json_to_show=uploaded_json, same_to_show = uploaded_are_equal)


if __name__ == '__main__':
    app.run(debug=True)
