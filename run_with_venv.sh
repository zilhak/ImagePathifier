#!/bin/bash

# ImagePathifier Run Script with Virtual Environment for macOS/Linux

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Setting up...${NC}"
    
    # Check if setup script exists
    if [ -f "setup_venv.sh" ]; then
        # Make setup script executable
        chmod +x setup_venv.sh
        # Run setup
        ./setup_venv.sh
        if [ $? -ne 0 ]; then
            echo -e "${RED}Setup failed. Please check the error messages above.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}setup_venv.sh not found. Creating virtual environment manually...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    fi
fi

# Activate virtual environment and run application
echo -e "${GREEN}Starting ImagePathifier...${NC}"
source venv/bin/activate && python ImagePathifier.py

# Check if the application exited successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}ImagePathifier closed successfully.${NC}"
else
    echo -e "${RED}ImagePathifier exited with an error.${NC}"
    exit 1
fi