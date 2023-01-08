ARG IMAGE_TAG=jammy
ARG VAULT_VER=1.12
ARG KUBE_VER=1.25.5
ARG TF_VER=1.3.6
ARG PKR_VER=1.8.5
ARG HELM_DOCS_VER=1.11.0
ARG TILT_VER=0.30.13
ARG KUSTOMIZE_VER=4.5.6

FROM docker.io/bitnami/kubectl:$KUBE_VER as kube
FROM docker.io/hashicorp/vault:$VAULT_VER as vault
FROM docker.io/hashicorp/terraform:$TF_VER as terraform
FROM docker.io/hashicorp/packer:$PKR_VER as pkr
FROM docker.io/jnorwood/helm-docs:v$HELM_DOCS_VER as helm-docs
FROM docker.io/tiltdev/tilt:v$TILT_VER as tilt
FROM docker.io/ubuntu:$IMAGE_TAG

LABEL maintainer="MikeB <mike@donthurt.us>"

ENV DEBIAN_FRONTEND=noninteractive
ENV NERDCTL_VER=1.1.0
ENV SSHD_CONFIG=/etc/ssh/sshd_config
ENV KUBECOLOR_VER=0.0.25
ENV HELM_VER=3.10.3

WORKDIR /root

# Setup dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y openssh-server curl sudo vim git rsync zsh wget bash apt-transport-https \
        python3 python3-pip python3-venv ca-certificates lsb-release gnupg

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
RUN wget https://get.helm.sh/helm-v${HELM_VER}-linux-amd64.tar.gz && \
    tar xzvf helm-v${HELM_VER}-linux-amd64.tar.gz && \
    chmod +x linux-amd64/helm && mv linux-amd64/helm /usr/local/bin/helm && \
    rm -rf linux-amd64 && rm helm-v${HELM_VER}-linux-amd64.tar.gz

# Install Kustomize
RUN wget "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv${KUSTOMIZE_VER}/kustomize_v${KUSTOMIZE_VER}_darwin_amd64.tar.gz" && \
    tar xzvf kustomize_v${KUSTOMIZE_VER}_darwin_amd64.tar.gz && chmod +x kustomize && mv kustomize /usr/local/bin/kustomize && \
    rm kustomize_v${KUSTOMIZE_VER}_darwin_amd64.tar.gz

# Install Docker
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
        apt update && apt install -y docker-ce-cli docker-compose-plugin && \
        apt autoclean && apt autoremove

# Regenerate SSH host keys
RUN mkdir /run/sshd && \
    ssh-keygen -A

WORKDIR /

# Install Vault and kubectl
COPY --from=kube --chown=root:root /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl
COPY --from=vault --chown=root:root /bin/vault /usr/local/bin/vault
COPY --from=terraform --chown=root:root /bin/terraform /usr/local/bin/terraform
COPY --from=pkr --chown=root:root /bin/packer /usr/local/bin/packer
COPY --from=helm-docs --chown=root:root /usr/bin/helm-docs /usr/local/bin/helm-docs
COPY --from=tilt --chown=root:root /usr/local/bin/tilt /usr/local/bin/tilt

EXPOSE 22
VOLUME [ "/home" ]

CMD ["service", "ssh", "start", "-D"]
