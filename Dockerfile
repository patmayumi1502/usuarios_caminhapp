FROM python:3.6-alpine

ENV TOPICO=meu-topico
ENV HOST=caminhapp-net
ENV PORTA=9092
ENV SLACK=https://hooks.slack.com/services/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
ENV CANAL=lab-produtor


ADD . /code
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["python", "server.py"]

