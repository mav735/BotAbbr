# BotAbbr

A Telegram bot that helps users quickly find the meanings of various abbreviations. This bot listens for abbreviation queries and responds with definitions from a predefined list. The bot also allows the administrator to update the abbreviation list directly by sending a file.

## Requirements

- Ubuntu (tested on Ubuntu 20.04 and 22.04)
- Docker
- Telegram Bot API Token

## Installation Instructions

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/mav735/BotAbbr.git
cd BotAbbr
```

### Step 2: Install Docker on Ubuntu
To run this project in a Docker container, Docker needs to be installed on your Ubuntu system. Follow these steps to install Docker:

Update your existing package list:

```bash
sudo apt update
```

Add Docker’s official GPG key:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the package database and install Docker:

```bash
sudo apt update
sudo apt install docker-ce -y
```

### Step: 3 Build + Run Docker container

```bash
docker build -t botabbr -f Dockerfile .
docker run -d --name botabbr-container botabbr
```