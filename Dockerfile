# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install Nginx and certbot
RUN apt-get update && apt-get install -y nginx certbot python3-certbot-nginx

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy Nginx configuration template (make sure to have it in your project directory)
COPY nginx.conf /etc/nginx/nginx.conf

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 and 443 available to the world outside this container
EXPOSE 80 443

# Define environment variable
ENV NAME World

# Command to run both Nginx and Gunicorn
CMD service nginx start && gunicorn -b localhost:9000 app:app
