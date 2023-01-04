FROM python:3.11.1-alpine3.17

RUN adduser -D devpod
WORKDIR /usr/src/app
COPY --chown=devpod:devpod src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=devpod:devpod src/app.py ./
COPY --chown=devpod:devpod src/dev_pod.py ./
COPY --chown=devpod:devpod src/templates ./templates
COPY --chown=devpod:devpod src/static ./static
RUN chmod +x ./app.py ./dev_pod.py

USER devpod
EXPOSE 8000

ENTRYPOINT [ "python3", "./app.py" ]