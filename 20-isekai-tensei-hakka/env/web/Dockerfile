FROM brunoipjg/apache-php-5.2

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server && \
    rm -rf /var/lib/apt/lists/* 

RUN rm -rf /usr/local/lib/php/*.php /usr/local/src/mongo-php-driver-1.5.8 /usr/local/src/php-5.2.16

COPY wog3.tar.gz /tmp/wog3.tar.gz

WORKDIR /tmp
RUN tar -zxvf wog3.tar.gz && mv /tmp/wog3/* /usr/local/apache2/htdocs && rm -rf /tmp/*

COPY rezero.php /rezero
RUN chmod 555 /rezero
RUN crontab -l | { cat; echo "*/30 * * * * /rezero"; } | crontab 

RUN chown -R root:root /usr/local/apache2/htdocs && \
    find /usr/local/apache2/htdocs -type d -exec chmod 555 {} \; && \
    find /usr/local/apache2/htdocs -type f -exec chmod 444 {} \;

RUN chmod 777 /tmp
RUN echo "#!/bin/bash\nset -e\ncron & mysqld & sleep 3 && /rezero & /usr/local/apache2/bin/apachectl -e info -DFOREGROUND" > /usr/local/bin/run