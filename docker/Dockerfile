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
ENV KUBECOLOR_VER=0.0.25

# Setup dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y openssh-server curl sudo vim git rsync zsh wget bash apt-transport-https

# Configure SSH
RUN sed -i 's/^#PermitRootLogin/PermitRootLogin/' "${SSHD_CONFIG}" && \
    sed -i 's/^#SyslogFacility/SyslogFacility/' "${SSHD_CONFIG}" && \
    sed -i 's/^#LogLevel/LogLevel/' "${SSHD_CONFIG}" && \
    sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' "${SSHD_CONFIG}"

# Setup SSH keys
RUN mkdir /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N '' && \
    curl https://github.com/youvegotmoxie.keys -o /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys && \
    echo "ubuntu ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt update && \
    apt install -y gh

# Install Kubecolor
RUN wget https://github.com/hidetatz/kubecolor/releases/download/v${KUBECOLOR_VER}/kubecolor_${KUBECOLOR_VER}_Linux_x86_64.tar.gz && \
    tar xzvf kubecolor_${KUBECOLOR_VER}_Linux_x86_64.tar.gz && \
    chmod +x kubecolor && mv kubecolor /usr/local/bin && rm LICENSE README.md

# Install Helm
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    apt update && \
    apt install -y helm  && \
    apt autoclean && apt autoremove

# Regenerate SSH host keys
RUN mkdir /run/sshd && \
    ssh-keygen -A

# Install Vault and kubectl
COPY --from=kube --chown=root:root /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl
COPY --from=vault --chown=root:root /bin/vault /usr/local/bin/vault

EXPOSE 22
VOLUME [ "/home" ]

CMD ["service", "ssh", "start", "-D"]