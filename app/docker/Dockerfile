ARG KUBE_VER=1.25.5

FROM docker.io/bitnami/kubectl:$KUBE_VER as kube
FROM python:3.11.1-alpine3.17

ENV HELM_VER=3.10.3

RUN adduser -D devpod
WORKDIR /usr/src/app
COPY --chown=devpod:devpod src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=devpod:devpod src/app.py ./
COPY --chown=devpod:devpod src/dev_pod.py ./
COPY --chown=devpod:devpod src/helm /home/devpod/helm
COPY --chown=devpod:devpod src/templates ./templates
COPY --chown=devpod:devpod src/static ./static
RUN chmod +x ./app.py ./dev_pod.py
RUN chown -Rv devpod:devpod /usr/src/app

# Install Helm
RUN wget https://get.helm.sh/helm-v${HELM_VER}-linux-amd64.tar.gz && \
    tar xzvf helm-v${HELM_VER}-linux-amd64.tar.gz && \
    chmod +x linux-amd64/helm && mv linux-amd64/helm /usr/local/bin/helm && \
    rm -rf linux-amd64 && rm helm-v${HELM_VER}-linux-amd64.tar.gz

COPY --from=kube --chown=root:root /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl

USER devpod
EXPOSE 8000

ENTRYPOINT [ "python3", "./app.py" ]