ARG IMAGE_TAG=jammy
ARG VAULT_VER=1.12
ARG KUBE_VER=1.25.5

FROM docker.io/bitnami/kubectl:$KUBE_VER as kube
FROM docker.io/hashicorp/vault:$VAULT_VER as vault
FROM docker.io/ubuntu:$IMAGE_TAG

LABEL maintainer="MikeB <mike@donthurt.us>"

ENV DEBIAN_FRONTEND=noninteractive
ENV NERDCTL_VER=1.1.0
ENV SSHD_CONFIG=/etc/ssh/sshd_config

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y openssh-server curl sudo vim git rsync zsh wget bash

RUN sed -i 's/^#PermitRootLogin/PermitRootLogin/' "${SSHD_CONFIG}" && \
    sed -i 's/^#SyslogFacility/SyslogFacility/' "${SSHD_CONFIG}" && \
    sed -i 's/^#LogLevel/LogLevel/' "${SSHD_CONFIG}" && \
    sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' "${SSHD_CONFIG}"

RUN mkdir /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N '' && \
    curl https://github.com/youvegotmoxie.keys -o /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys && \
    apt-get autoremove && apt-get autoclean && \
    echo "ubuntu ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu

## Linter complaint about pipes
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt-get/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    apt-get autoclean && apt-get autoremove

## Disable for now. Not very useful
#RUN cd /root && wget https://github.com/containerd/nerdctl/releases/download/v${NERDCTL_VER}/nerdctl-full-${NERDCTL_VER}-linux-amd64.tar.gz && \
#    tar Cxzvvf /usr/local nerdctl-full-${NERDCTL_VER}-linux-amd64.tar.gz && \
#    rm -f nerdctl-full-${NERDCTL_VER}-linux-amd64.tar.gz

RUN mkdir /run/sshd && \
    ssh-keygen -A

COPY --from=kube --chown=root:root /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl
COPY --from=vault --chown=root:root /bin/vault /usr/local/bin/vault

EXPOSE 22
VOLUME [ "/home" ]

CMD ["service", "ssh", "start", "-D"]