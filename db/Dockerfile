FROM timescale/timescaledb-ha:pg13-latest
USER root
ENV POSTGRES_USER dsadmin
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB sifdb
COPY scripts/* /docker-entrypoint-initdb.d/
# RUN apt-get update \
#     && apt-get install -y wget unzip; \
#     wget https://data.sifchain.finance/downloads/backup_data.zip; \
#     unzip backup_data.zip; \
#     rm backup_data.zip;
USER postgres
