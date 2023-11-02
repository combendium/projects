# Use the official defacto Python image from
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Copy all the files needed for the app to work
COPY flask_inference.py .
COPY dropout_eff_netv2m_epoch_07_0.81_0.79.h5 .
COPY requirements.txt .

# Install all the necessary libraries
RUN pip install -r requirements.txt

# Run the API!
CMD python flask_inference.py
