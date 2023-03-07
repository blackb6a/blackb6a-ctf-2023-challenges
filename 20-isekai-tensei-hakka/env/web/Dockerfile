FROM brunoipjg/apache-php-5.2

COPY wog3.tar.gz /tmp/wog3.tar.gz
WORKDIR /tmp
RUN tar -zxvf wog3.tar.gz && mv /tmp/wog3/* /usr/local/apache2/htdocs && rm -rf /tmp/*
RUN sed -i "s/'localhost/'wog3-db/g" /usr/local/apache2/htdocs/forum_support/config/config.php
RUN sed -i "s/d=''/d='flag{Un1ink_za_worId_Un1ock_za_res3t}'/g" /usr/local/apache2/htdocs/forum_support/config/config.php
COPY rezero.php /usr/local/apache2/htdocs/rezero.php
RUN php /usr/local/apache2/htdocs/rezero.php
RUN crontab -l | { cat; echo "*/30 * * * * php /usr/local/apache2/htdocs/rezero.php"; } | crontab 
RUN cp /usr/local/apache2/htdocs/index.htm /usr/local/apache2/htdocs/index.html
RUN chown -R root:root /usr/local/apache2/htdocs && \
    find /usr/local/apache2/htdocs -type d -exec chmod 555 {} \; && \
    find /usr/local/apache2/htdocs -type f -exec chmod 444 {} \;
