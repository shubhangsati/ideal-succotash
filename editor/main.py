from flask import Flask, render_template, request, redirect, url_for
import random
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("Home_Screen.html")


@app.route("/code")
def code():
    return render_template("Code.html")

@app.route('/compileCode/<lang>', methods=['POST'])
def compileCode(lang):
    filename = str(random.random())[2:] + "." + lang
    f = open(filename, 'w')
    code = request.form['value']
    f.write(code)
    f.close()
    
    if (lang == "cpp"):
        fileobject = filename[:-4]
        ca = ["g++", filename, "-o", fileobject]
        sp = subprocess.Popen(ca, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errlines = sp.stderr.readlines()
        outlines = sp.stdout.readlines()
        sp2 = subprocess.Popen(["rm", filename])
        if len(errlines) == 0:
            fileobject = "./" + fileobject
            cb = [fileobject]
            subp = subprocess.Popen(cb, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            errlines = subp.stderr.readlines()
            outlines = subp.stdout.readlines()
            sp2 = subprocess.Popen(["rm", fileobject])
            if len(errlines) == 0:
                retval = "Ran Successfully <br>"
                for i in range(len(outlines)):
                    line = outlines[i]
                    retval += line.decode('utf-8').strip() + "<br>"
                return retval
            else:
                retval = "Runtime Error <br>"
                for i in range(len(errlines)):
                    line = errlines[i]
                    retval += line.decode('utf-8').strip() + "<br>"
                return retval
        else:
            retval = "Compilation Error <br>"
            for i in range(len(errlines)):
                line = errlines[i]
                retval += line.decode('utf-8').strip() + "<br>"
            return retval

    else:
        command = ["python", filename]
        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errlines = sp.stderr.readlines()
        outlines = sp.stdout.readlines()
        sp2 = subprocess.Popen(["rm", filename])
        if len(errlines) == 0:
            retval = "Ran successfully <br> "
            for i in range(len(outlines)):
                line = outlines[i]
                retval += line.decode('utf-8').strip() + "<br>"
            return retval
        else:
            retval = "Errors encountered <br>"
            for i in range(len(errlines)):
                line = errlines[i]
                retval += line.decode('utf-8').strip() + "<br>"
            return retval




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
