import dev_pod
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory, send_file, Response

namespace = "test-pod-0"
deploymentName = "testing-pod"

app = Flask(__name__)


@app.route("/")
def root():
    return render_template('parent-root.html',
                            namespace=namespace,
                            deploymentName=deploymentName)

@app.route("/deploy")
def deploy():
    dev_pod.deploy_dev_pod(namespace, deploymentName)

if __name__ == "__main__":
    app.run()
