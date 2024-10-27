<div align="center">

![Main](docs/gif/road.gif)

**This service automates booking available slots for road tests using a Telegram bot, eliminating the need for manual checks.**

---

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Telegram Bot](https://img.shields.io/badge/Telegram_Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Asyncio](https://img.shields.io/badge/Asyncio-808080?style=for-the-badge)

---


## User Data Input

The user enters their information, such as document number, postal code, and birth date.

<img src="docs/img/data_input.png" alt="User Data Input" width="800"/>

## Slot Availability Check

The service checks for available slots at regular intervals.

<img src="docs/img/calendar.png" alt="Calendar" width="250"/>

## Notifications

Available slots are sent directly to the user in the Telegram bot.

<img src="docs/img/response.png" alt="Response"/>

## Booking Confirmation

Once the user selects a slot, the service books it, and the confirmation is sent via Telegram.

<img src="docs/img/booking.png" alt="Booking" width="250"/>

---


  
# 📦 Features

<div align="center">
  
**Configurable YAML File**: Allows customization of every step when interacting with the booking service.

**Full Logging**: Logs all service actions for transparency and debugging.

**Captcha Handling**: Supports solving captchas during the booking process.

**Customizable Check Intervals**: You can set how often the service checks for available slots.

**Concurrent Requests**: Supports handling multiple users asynchronously.

</div>

---

# 🤖 Customizable

The service is highly customizable and can be adapted to other booking services or workflows by modifying the configuration in the YAML file.

</div>
