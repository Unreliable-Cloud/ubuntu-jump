import dev_pod
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/", methods = ["GET"])
def root():
    return render_template('parent-index.html')

@app.route("/deploy", methods = ["GET", "POST"])
def deploy():
    if request.method == "POST":
        deployPost = {
            "namespace": request.form.get("namespace"),
            "deploymentName": request.form.get("deploymentName"),
            "backupState": request.form.get("backupState"),
            "shell": request.form.get("shell"),
        }

        if deployPost['shell'] == None:
          deployPost['shell'] = "/bin/bash"
        else:
          deployPost['shell'] = "/usr/bin/zsh"

        if deployPost['backupState'] == None:
            deployPost['backupState'] = False
        else:
            deployPost['backupState'] = True

        dev_pod.deploy_dev_pod(deployPost['namespace'], deployPost['deploymentName'], deployPost['backupState'], deployPost['shell'])

        return render_template('parent-deploy.html',
                                namespace=deployPost['namespace'],
                                deploymentName=deployPost['deploymentName'],
                                backupState=deployPost['backupState'],
                                shell=deployPost['shell'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
