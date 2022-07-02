ARG IMAGE_TAG=jammy
FROM docker.io/ubuntu:$IMAGE_TAG
LABEL maintainer="MikeB <mike@donthurt.us>"

RUN apt update && apt upgrade -y && apt-get install -y openssh-server curl sudo
RUN mkdir /root/.ssh && \
  chmod 0700 /root/.ssh && \
  ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N '' && \
  curl https://github.com/youvegotmoxie.keys -o /root/.ssh/authorized_keys && \
  chmod 0600 /root/.ssh/authorized_keys && \
  apt autoremove && apt autoclean && \
  echo "ubuntu ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu

RUN mkdir /run/sshd && \
  ssh-keygen -A && \
  apt autoremove -y curl

EXPOSE 22
VOLUME [ "/home" ]

CMD ["service", "ssh", "start", "-D"]
