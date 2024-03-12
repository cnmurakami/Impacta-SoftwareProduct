FROM python:3.12.2
RUN pip install flask
RUN pip install requests
RUN pip install flask_mysqldb
RUN mkdir templates
RUN mkdir static
COPY server.py /
COPY templates/*  /templates/
COPY static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
CMD ["python","server.py"]