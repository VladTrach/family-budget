FROM python:3.10.7-slim

# Add a new user "john" with user id 8877
RUN useradd -m -u 8877 app

# Set work directory
WORKDIR /code
RUN chown app /code

# Change to non-root privilege
USER app

# Copy project
COPY . /code/

# Install dependencies
RUN python -m pip install -U --force-reinstall pip
RUN pip install -r requirements.txt
