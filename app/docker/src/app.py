import dev_pod
from flask import Flask, request, redirect, url_for, render_template

namespace = ""
deploymentName = ""
createOutput = ""
backupState = ""

app = Flask(__name__)


@app.route("/", methods = ["GET"])
def root():
    return render_template('parent-index.html',
                            namespace=namespace,
                            deploymentName=deploymentName)

@app.route("/deploy", methods = ["GET", "POST"])
def deploy():
    if request.method == "POST":
        deployPost = {
            "namespace": request.form.get("namespace"),
            "deploymentName": request.form.get("deploymentName"),
            "backupState": request.form.get("backupState"),
        }
        if deployPost['backupState'] is None:
            deployPost['backupState'] = "false"
        else:
            deployPost['backupState'] = "true"
        dev_pod.deploy_dev_pod(deployPost['namespace'], deployPost['deploymentName'], deployPost['backupState'])

        return render_template('parent-deploy.html',
                                namespace=deployPost['namespace'],
                                deploymentName=deployPost['deploymentName'],
                                backupState=deployPost['backupState'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
