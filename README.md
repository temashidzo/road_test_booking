# ![Main](docs/gif/road.gif)

## <div align="center">Overview</div>

<div align="center">
This is a service designed for quickly booking available slots for road tests for a driver's license using a Telegram bot. The service automates the process of checking and booking available slots for road tests, removing the need for manually checking websites every few minutes.
</div>

<div align="center">
The service uses **Selenium** to interact with the booking website and logs all activity. You can configure various steps of the booking process in a configuration file to adapt it to different services.
</div>

---

### <div align="center">🛠 Technologies Used</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Telegram_Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Bot" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Asyncio-808080?style=for-the-badge" alt="Asyncio" />
</div>

---

## <div align="center">📦 Features</div>

### <div align="center">Automated Booking</div>

<div align="center">
  <img src="link-to-your-booking-process-screenshot" alt="Booking Process" />
</div>

<div align="center">
The bot checks for available time slots for road tests on the official booking website and sends them directly to your Telegram.
</div>

---

### <div align="center">Custom Data Input</div>

<div align="center">
  <img src="link-to-your-user-data-input-screenshot" alt="User Data Input" />
</div>

<div align="center">
Users input their details such as name, document number, postal code, and date of birth through the bot.
</div>

---

### <div align="center">Periodic Slot Checking</div>

<div align="center">
Once the details are submitted, the service periodically checks the booking service at a predefined interval for available time slots.
</div>

---

## <div align="center">🚀 How It Works</div>

<div align="left">

1. **User Data Input**: Users enter their information via the Telegram bot, including document number and postal code.

<div align="center">
  ![Input](docs/img/data_input.png)
</div>
   
2. **Slot Search**: The service uses Selenium to browse the website and search for available slots at regular intervals.

3. **Notifications**: When available slots are found, users receive updates directly in their Telegram chat.

4. **Logging**: All actions, searches, and responses are logged to ensure transparency.

5. **Configurable**: Through a configuration file, the system can easily be adapted for other booking services with minimal code changes.

</div>

---

## <div align="center">🔧 Configuration</div>

<div align="center">
The service uses Selenium for browser automation, and you can configure various booking steps by modifying the `config.yaml` file. This allows for flexibility in adapting to different booking systems.
</div>

---

## <div align="center">📈 Logging</div>

<div align="center">
All interactions, checks, and updates are logged for auditing and debugging purposes.
</div>

---

## <div align="center">🤖 Customizable</div>

<div align="center">
This system can be adapted to other services beyond road tests by configuring the YAML file for different workflows, without requiring significant code changes.
</div>
