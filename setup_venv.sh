#!/bin/bash

# Image Pathifier Virtual Environment Setup Script for macOS/Linux

echo "========================================"
echo "  ImagePathifier Virtual Environment Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi
echo ""

# Remove existing venv if exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip
echo ""

# Install packages
echo "Installing required packages..."
python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install packages."
    echo "Please check requirements.txt and try again."
    exit 1
fi
echo ""

echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "To run the program:"
echo "  1. source venv/bin/activate"
echo "  2. python ImagePathifier.py"
echo ""
echo "Or just run: ./run_with_venv.sh"
echo "========================================"