FROM postgres:13

COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY setup.sh /docker-entrypoint-initdb.d/setup.sh

VOLUME /var/lib/postgresql/data

RUN mkdir -p /var/log/postgresql
RUN chown postgres:postgres /var/log/postgresql

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
