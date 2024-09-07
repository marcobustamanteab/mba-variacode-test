FROM python:3.10-slim

# Set the WD inside the container
WORKDIR /app

# Copy the current directory in /app
COPY . .

# Install from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

# Expose port 5000
EXPOSE 5000

# Define env variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py
CMD ["flask", "run"]