# Use an official Python runtime as a parent image
FROM python:3.11.3


# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5010

# Run app.py when the container launches
CMD ["python", "server.py"]

