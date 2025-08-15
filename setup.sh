#!/bin/bash

# Setup script for Data Assistant Project in Streamlit Cloud
echo "🚀 Setting up Data Assistant Project..."

# Install system dependencies
apt-get update
apt-get install -y sqlite3 python3-dev build-essential

# Create necessary directories
mkdir -p new_data_assistant_project/src/database
mkdir -p new_data_assistant_project/data

# Set permissions
chmod 755 new_data_assistant_project/src/database
chmod 755 new_data_assistant_project/data

echo "✅ Setup completed successfully!"
