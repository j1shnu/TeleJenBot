# Setting the base image
FROM python:3.9-slim-buster

# Setting the working directory in the container
WORKDIR /app/

# Copying the dependencies file to the working directory
COPY requirements.txt .

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copying the source code and contents to the working directory
COPY . .

# Command to start the Bot and will run on container start
CMD ["python3", "-m", "jenbot"]