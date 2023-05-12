# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Add the current directory contents into the container at /app
ADD toolkitui/* /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app when the container launches
CMD streamlit run RLHI_Data_Generator.py
