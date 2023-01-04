import dev_pod
from flask import Flask, request, redirect, url_for, render_template

namespace = ""
deploymentName = ""
createOutput = ""
backupState = ""

app = Flask(__name__)


@app.route("/")
def root():
    return render_template('parent-index.html',
                            namespace=namespace,
                            deploymentName=deploymentName)

@app.route("/deploy", methods =["GET", "POST"])
def deploy():
    if request.method == "POST":
        namespace = request.form.get("namespace")
        deploymentName = request.form.get("deploymentName")
        backupState = request.form.get("backupState")
        dev_pod.deploy_dev_pod(namespace, deploymentName, backupState)

        return render_template('parent-deploy.html',
                                namespace=namespace,
                                deploymentName=deploymentName,
                                backupState=backupState)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
