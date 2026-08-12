# 📈 Binance Futures Testnet Trading Bot

A secure, lightweight, and interactive web application built with **Streamlit** that allows users to execute **Market** and **Limit** orders on the **Binance Futures Testnet** environment seamlessly.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://binance-trading-bot-d4yhxzwc528r9bahufetzx.streamlit.app/)

## 🚀 Live Demo
Access the live application here: [Binance Trading Bot App](https://binance-trading-bot-d4yhxzwc528r9bahufetzx.streamlit.app/)

---

## ✨ Features
* **Interactive UI:** Clean and simple dashboard designed using Streamlit.
* **Order Types:** Support for both **MARKET** and **LIMIT** orders.
* **Secure API Integration:** Utilizes HMAC SHA256 request signing for safe communication with Binance API.
* **Environment Security:** Uses Streamlit Secrets (`st.secrets`) to securely store API keys without exposing them in the codebase.
* **Testnet Support:** Safely tests trading strategies using Binance Futures Testnet funds without risking real capital.

---

## 🛠️ Tech Stack
* **Python** (Core Logic)
* **Streamlit** (Frontend & Deployment UI)
* **Requests** (HTTP Library for API communication)
* **Binance Futures Testnet API**

---

## ⚙️ Setup & Installation (Local Development)

If you want to run this project locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/binance-trading-bot.git](https://github.com/your-username/binance-trading-bot.git)
   cd binance-trading-bot
