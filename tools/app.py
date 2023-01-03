import dev_pod
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory, send_file, Response

namespace = ""
deploymentName = ""
createOutput = ""
backupState = ""

app = Flask(__name__)


@app.route("/")
def root():
    return render_template('index.html',
                            namespace=namespace,
                            deploymentName=deploymentName)

@app.route("/deploy", methods =["GET", "POST"])
def deploy():
    if request.method == "POST":
        namespace = request.form.get("namespace")
        deploymentName = request.form.get("deploymentName")
        backupState = request.form.get("backupState")
        dev_pod.deploy_dev_pod(namespace, deploymentName)

        return render_template('deploy.html',
                                namespace=namespace,
                                deploymentName=deploymentName,
                                backupState=backupState)

if __name__ == "__main__":
    app.run()
