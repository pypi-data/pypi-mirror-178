# Author: Charlie BROMBERG (Shutdown - @_nwodtuhs)

FROM debian

ARG TAG="local"
ARG VERSION="local"
ARG BUILD_DATE="n/a"

LABEL org.exegol.tag="${TAG}"
LABEL org.exegol.version="${VERSION}"
LABEL org.exegol.build_date="${BUILD_DATE}"
LABEL org.exegol.app="Exegol"
LABEL org.exegol.src_repository="https://github.com/ThePorgs/Exegol-images"

RUN echo "${TAG}-${VERSION}" > /opt/.exegol_version

ADD sources /root/sources
RUN chmod +x /root/sources/install.sh

#RUN /root/sources/install.sh install_base
#RUN /root/sources/install.sh neo4j_install
#RUN /root/sources/install.sh bloodhound_v4
#RUN apt-get install -y libgbm1

RUN /root/sources/install.sh deploy_exegol
RUN /root/sources/install.sh update
RUN apt-get update && apt-get install -y git curl zsh zip wget python3 python3-pip vim procps
RUN /root/sources/install.sh install_ohmyzsh
RUN /root/sources/install.sh install_openvpn
RUN /root/sources/install.sh install_logrotate

WORKDIR /workspace

ENTRYPOINT ["/.exegol/entrypoint.sh"]
