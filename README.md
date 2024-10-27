# ![autocomplete](docs/gif/road2.gif)

## Overview

This is a service designed for quickly booking available slots for road tests for a driver's license using a Telegram bot. The service automates the process of checking and booking available slots for road tests, removing the need for manually checking websites every few minutes.

The service uses **Selenium** to interact with the booking website and logs all activity. You can configure various steps of the booking process in a configuration file to adapt it to different services.

---

### 🛠 Technologies Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Telegram Bot](https://img.shields.io/badge/Telegram_Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Asyncio](https://img.shields.io/badge/Asyncio-808080?style=for-the-badge)

---

## 📦 Features

### Automated Booking

![Booking Process](link-to-your-booking-process-screenshot)

The bot checks for available time slots for road tests on the official booking website and sends them directly to your Telegram.

### Custom Data Input

![User Data Input](link-to-your-user-data-input-screenshot)

Users input their details such as name, document number, postal code, and date of birth through the bot.

### Periodic Slot Checking

Once the details are submitted, the service periodically checks the booking service at a predefined interval for available time slots.

---

## 🚀 How It Works

1. **User Data Input**: Users enter their information via the Telegram bot, including document number and postal code.
   
2. **Slot Search**: The service uses Selenium to browse the website and search for available slots at regular intervals.

3. **Notifications**: When available slots are found, users receive updates directly in their Telegram chat.

4. **Logging**: All actions, searches, and responses are logged to ensure transparency.

5. **Configurable**: Through a configuration file, the system can easily be adapted for other booking services with minimal code changes.

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.x
- Docker (optional but recommended)

### Installation

Clone the repository:

```bash
git clone https://github.com/your-repo-url.git
cd road-test-booking-service. 
```

---

## 🔧 Configuration

The service uses Selenium for browser automation, and you can configure various booking steps by modifying the config.yaml file. This allows for flexibility in adapting to different booking systems.

## 📈 Logging

All interactions, checks, and updates are logged for auditing and debugging purposes.

## 🤖 Customizable

This system can be adapted to other services beyond road tests by configuring the YAML file for different workflows, without requiring significant code changes.

