import dev_pod
from flask import Flask, request, redirect, url_for, render_template

namespace = "devpod-deploy"

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return redirect(url_for('create'))


@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template('parent-create.html')


@app.route("/docs", methods=["GET"])
def docs():
    return redirect("https://github.com/Unreliable-Cloud/ubuntu-jump")


@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    if request.method == "POST":
        deployPost = {
            "deploymentName": request.form.get("deploymentName"),
            "backupState": request.form.get("backupState"),
            "shell": request.form.get("shell"),
        }

        if deployPost['shell'] is None:
            deployPost['shell'] = "/bin/bash"
        else:
            deployPost['shell'] = "/usr/bin/zsh"

        if deployPost['backupState'] is None:
            deployPost['backupState'] = False
        else:
            deployPost['backupState'] = True

        dev_pod.deploy_pod(
            namespace, deployPost['deploymentName'], deployPost['backupState'], deployPost['shell'])

        return render_template('parent-deployed.html',
                               namespace=namespace,
                               deploymentName=deployPost['deploymentName'],
                               backupState=deployPost['backupState'],
                               shell=deployPost['shell'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
