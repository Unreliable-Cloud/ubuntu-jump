import dev_pod
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory, send_file, Response

namespace = ""
deploymentName = ""
createOutput = ""

app = Flask(__name__)


@app.route("/")
def root():
    return render_template('parent-root.html',
                            namespace=namespace,
                            deploymentName=deploymentName)

@app.route("/deploy", methods =["GET", "POST"])
def deploy():
    if request.method == "POST":
        namespace = request.form.get("namespace")
        deploymentName = request.form.get("deploymentName")
        createOutput = dev_pod.deploy_dev_pod(namespace, deploymentName)
        return createOutput

if __name__ == "__main__":
    app.run()
