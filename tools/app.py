import dev_pod
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory, send_file, Response

app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    createPod = dev_pod.deploy_dev_pod("test-pod-0", "testing")
    return createPod

if __name__ == "__main__":
    app.run()
