# Hotel Booking & Smart Lock Automation (HotRes + TTLock)

A simple but effective script that eliminates manual guest check-ins. The system automatically fetches today's reservations from the hotel system, generates unique door codes, and sends them to guests via SMS or email.

## What does this project do?
* **Saves time:** Automatically fetches the list of today's arrivals from the HotRes API.
* **Generates codes:** Communicates with smart locks via the TTLock API and sets a 4-digit passcode valid only until the end of the guest's stay.
* **Sends notifications:** Automatically sends a welcome message and access code via SMS (for local numbers) or email (for international guests).
* **Runs in the background:** Saves processed reservations locally to avoid spamming guests, and sends an SMS alert to the administrator if an API failure occurs.

## Tech Stack
* **Language:** Python 3 (using `requests` and `python-dotenv`)
* **Integrations:** HotRes API, TTLock API, SMSPlanet API, Gmail SMTP
* **Infrastructure:** Docker and Docker Compose – ready to deploy on any server without worrying about the environment setup.

## How to run it?

1. Clone this repository to your local machine.
2. Configure API keys. Create the following environment files and fill them with your credentials:
   * `secret.env` (root directory) – with the admin's phone number.
   * `HotResAPI/ApiAuth.env` – keys for the booking system.
   * `MessageAPI/api_token.env` – credentials for SMSPlanet and email.
3. Run the app using Docker:
   ```bash
   docker-compose up --build
  (Alternatively, you can run it the classic way: pip install -r requirements.txt followed by python main.py).
