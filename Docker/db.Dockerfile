FROM postgres:15.2-alpine
COPY init.sql /docker-entrypoint-initdb.d/