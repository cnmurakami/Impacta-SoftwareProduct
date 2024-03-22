FROM python:3.12.2
EXPOSE 5000
RUN pip install flask
RUN pip install requests
RUN pip install flask_mysqldb
RUN mkdir templates
RUN mkdir static
COPY server.py /
COPY backend/* /backend/
COPY templates/*  /templates/
COPY static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
RUN chmod -R a+rwx backend
CMD python server.py