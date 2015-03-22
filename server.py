#!/usr/bin/env python
import webbrowser
import sys
import os
from flask import Flask
app = Flask(__name__)

@app.route("/fuzz_files/<filename>")
def fuzz_files(filename=None):
    return open("fuzz_files/%s" % filename).read()

@app.route("/done")
def done():
    return "done."

@app.route("/")
@app.route("/<fuzz_id>")
def hello(fuzz_id=None):
    fuzz_files=[]
    html = "provide /&lt;fuzz_id&gt;"
    iframes = ""
    if fuzz_id:
        fuzz_files = [("fuzz_files/%s" % f) for f in os.listdir("fuzz_files/") if f[:len(fuzz_id)]==fuzz_id]
        print fuzz_files
        html = open("templates/server.html").read()
        html = html.replace("{{iframes}}", str(fuzz_files))
    return html

if __name__ == "__main__":
    webbrowser.open_new_tab('http://127.0.0.1:5000/%s' % sys.argv[1])
    app.run(host="127.0.0.1", port=5000, debug=False)