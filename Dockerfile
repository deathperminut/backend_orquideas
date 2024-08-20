# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /orcas
WORKDIR /app

# Copy the current directory contents into the container at /orcas
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the orcas runs on
EXPOSE 8080

# Run migrate and then start the Django development server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8080
# Configura el comando de inicio para el contenedor
CMD ["python3","manage.py","runserver","0.0.0.0:8080"]