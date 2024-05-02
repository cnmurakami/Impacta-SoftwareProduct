FROM python:3.12.2
# EXPOSE 5000
ENV DOCKED Yes
RUN pip install flask
RUN pip install requests
RUN pip install flask_mysqldb
RUN mkdir app
WORKDIR /app/
RUN mkdir templates
RUN mkdir static
RUN mkdir backend
COPY server.py /app
COPY backend/ /app/backend/
COPY templates/  /app/templates/
COPY static/  /app/static/
# RUN chmod -R a+rwx /app/static
# RUN chmod -R a+rwx /app/templates
# RUN chmod -R a+rwx /app/backend
RUN chmod -R 755 /app/static
RUN chmod -R 755 /app/templates
RUN chmod -R 755 /app/backend
CMD python server.py