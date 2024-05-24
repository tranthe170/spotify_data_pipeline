# Base image
FROM apache/airflow:2.9.1

# Environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Install necessary system packages
USER root
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git apt-transport-https ca-certificates gnupg

# Add the Cloud SDK distribution URI as a package source
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install the Google Cloud SDK
RUN apt-get update && apt-get install -y google-cloud-sdk

# Switch to airflow user and upgrade pip
USER ${AIRFLOW_UID:-50000}
RUN pip install --upgrade pip

# Copy and install Python packages from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR $AIRFLOW_HOME

# Verify the installation
RUN gcloud --version
