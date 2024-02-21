#!/bin/bash

# Check if python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python first."
    exit
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the necessary libraries
pip install pillow gradio numpy

# Deactivate the virtual environment
deactivate

echo "Setup is complete. You can now run the app by activating the virtual environment and running the python script."
echo "To activate the virtual environment, use: source venv/bin/activate"
echo "To run the app, use: python3 app.py"