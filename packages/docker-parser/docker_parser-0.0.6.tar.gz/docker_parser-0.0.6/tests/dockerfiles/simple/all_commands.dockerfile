FROM ubuntu
RUN apt update
LABEL version="1.0"
# Depriciated, kept just for information, if starts failing, can be removed
MAINTAINER Ivan Mitruk
EXPOSE 80
ENTRYPOINT [ "executable", "param" ]
ENV MY_CAT fluffy
ADD some_file.txt /some_dir/
COPY some_file.txt dest
USER root
WORKDIR some_dir
ARG UID
# ONBUILD more later
ONBUILD RUN apt install vim
STOPSIGNAL 9
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
SHELL ["executable", "parameters"]
CMD executable