ARG IMAGE_TAG=jammy
FROM docker.io/ubuntu:$IMAGE_TAG
LABEL maintainer="MikeB <mike@donthurt.us>"

ENV DEBIAN_FRONTEND=nointeractive

RUN apt update && \
    apt upgrade -y && \
    apt install -y openssh-server curl sudo vim git rsync zsh

RUN mkdir /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N '' && \
    curl https://github.com/youvegotmoxie.keys -o /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys && \
    apt autoremove && apt autoclean && \
    echo "ubuntu ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu

RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt update && \
    apt install -y gh

RUN curl https://github.com/containerd/nerdctl/releases/download/v1.1.0/nerdctl-1.1.0-linux-amd64.tar.gz -o nerdctl.tar.gz && \
    tar xzvf nerdctl.tar.gz && \
    chmod +x nerdctl && \
    mv nerdctl /usr/local/bin/docker && \
    rm nerdctl* containerd-rootless*.sh

RUN mkdir /run/sshd && \
    ssh-keygen -A

EXPOSE 22
VOLUME [ "/home" ]

CMD ["service", "ssh", "start", "-D"]