FROM debian

COPY sources/exegol/entrypoint.sh /entrypoint.sh
RUN chmod 700 /entrypoint.sh

CMD "default"
ENTRYPOINT ["/entrypoint.sh"]
