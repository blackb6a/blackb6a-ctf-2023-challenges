FROM python:buster

RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
RUN pip install flask
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/* 

COPY server.py /
RUN echo "#!/bin/sh\necho b6actf{InjEcTThEInjEcTIngInjEcTors_AND_0_UNION_SELECT_1_--_1e308}" > /proof_2ad5d6c6-6130-4aaf-aecf-ab91991b53d9.sh
RUN echo "#!/bin/sh\nrm -rf /tmp/* /home/sqlmap/*" > /cls
RUN chmod -R 555 /sqlmap-dev
RUN chmod 555 /server.py /proof*.sh  /cls
RUN crontab -l | { cat; echo "*/30 * * * * /cls"; } | crontab
RUN adduser --disabled-password sqlmap
ENV G_SITEKEY 6Lfe2SEaAAAAAGurMvdKBjendG6oUDhdmOlVIvvj
ENV G_SECRET 6Lfe2SEaAAAAAJVLnkjcJ-A2qY0_CCVnGSiODCAo
CMD ["bash","-c","cron & runuser -u sqlmap -- python /server.py"]