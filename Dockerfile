
# Base Image
FROM python:3.11

# Installing required packages 
RUN pip install pandas
RUN pip install numpy
RUN pip install argparse

# Setting /app as the working directory
WORKDIR /app

# Copying the current directory contents into the container
COPY . /app/

# Running pipeline.py file when container starts running
CMD ["python", "pipeline.py"]
