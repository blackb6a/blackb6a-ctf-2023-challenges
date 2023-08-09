FROM python:alpine
RUN apk --no-cache add chromium chromium-chromedriver tini build-base libffi-dev
RUN pip install flask && pip install selenium==4.10.0

WORKDIR /app
COPY *.py .

ENV H_SITEKEY 218e8859-e05e-46d5-a2c0-a903f23742c9
ENV H_SECRET 0xDB88489a72C3b9945823cE649d172748f8EE6F61
ENV FLAG_RCE b6actf{Master_Password=***************************************************************}
ENV AUTH DidSomeoneBotherXSSChallenges

USER nobody
EXPOSE 3000

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python","server.py"]