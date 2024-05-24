#!/bin/bash

# Run using the below command
# bash vm_setup.sh 

# Function to display informative messages
info() {
    echo -e "\033[1;32mℹ\033[0m $1"
}

# Function to display error messages
error() {
    echo -e "\033[1;31m✘ Error:\033[0m $1" >&2
    exit 1
}

# Check if the script is run using bash
if [ -z "$BASH_VERSION" ]; then
    error "Please run this script using bash."
fi

# Update package repositories
info "Running sudo apt-get update..."
sudo apt-get update || error "Failed to update package repositories."

# Install Docker
info "Installing Docker..."
sudo apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release || error "Failed to install dependencies."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg || error "Failed to add Docker's GPG key."
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null || error "Failed to set up Docker repository."
sudo apt-get update || error "Failed to update package repositories."
sudo apt-get -y install docker-ce docker-ce-cli containerd.io || error "Failed to install Docker."

# Configure Docker to run without sudo
info "Configuring Docker to run without sudo..."
sudo groupadd -f docker || error "Failed to add docker group."
sudo gpasswd -a "$USER" docker || error "Failed to add user to docker group."
sudo service docker restart || error "Failed to restart Docker service."

# Install Docker Compose
info "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose || error "Failed to download Docker Compose."
sudo chmod +x /usr/local/bin/docker-compose || error "Failed to make Docker Compose executable."

# Display Docker Compose version
info "Checking Docker Compose version..."
docker-compose --version || error "Failed to check Docker Compose version."

# Add Docker Compose directory to PATH
info "Updating PATH in .bashrc..."
echo 'export PATH="/usr/local/bin:$PATH"' >> "$HOME/.bashrc" || error "Failed to update .bashrc."
source "$HOME/.bashrc" || error "Failed to reload .bashrc."

info "Setup completed successfully!"
