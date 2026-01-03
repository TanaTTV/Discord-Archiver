# 🗄️ Discord Personal History Backup

> **A local utility for archiving your own message history and server data for offline viewing and data sovereignty.**

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![Discord.py](https://img.shields.io/badge/discord.py-2.3-blueviolet?logo=discord)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

> **⚠️ Compliance & Safety Warning**
>
> This tool is designed for **personal archival purposes only** (e.g., backing up your own servers or DMs).
>
> * **Do not** use this tool to mass-scrape servers where you do not have administrative rights.
> * **Respect Rate Limits:** Aggressive scraping violates Discord's Terms of Service and can result in account termination.
> * **Privacy:** Do not distribute archives containing other users' data without their consent.
> * **Liability:** The user assumes all responsibility for data privacy compliance (GDPR/CCPA) and account safety.

---

## ✨ Features

- 🕸️ **Local Web Interface** — Runs entirely on your machine via a simple browser UI
- 📄 **Standard JSON and Human-Readable TXT Exports** — Portable formats for long-term archival
- 🔒 **Self-Hosted: Your Data Stays on Your Machine** — No third-party servers or cloud uploads
- ⚙️ **Configurable Speed Settings for API Safety** — Adjust concurrency to respect Discord's rate limits
- 🚀 **Easy Setup** — Minimal dependencies, runs with standard Python

---

## 📦 What's in the Backup?

Your backup archive includes:

| File | Description |
|------|-------------|
| `*_messages.json` | Complete message data in JSON format (for developers/long-term storage) |
| `*_readable.txt` | Human-readable text format for easy browsing |
| `by_channel/*.txt` | Messages organized by channel |
| `archive_info.json` | Summary metadata with export statistics |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/TanaTTV/discord-personal-backup.git
cd discord-personal-backup
pip install -r requirements.txt
```

### 2. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → Name it → Create
3. Go to **"Bot"** section → Click **"Reset Token"** → Copy it securely
4. **Enable Required Intents** (scroll down on Bot page):
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT

### 3. Invite Bot to Your Server

1. In Developer Portal → **OAuth2** → **URL Generator**
2. Check scopes: `bot`
3. Check permissions: 
   - ☑️ Read Message History
   - ☑️ Read Messages/View Channels
4. Copy & open the generated URL to invite the bot

### 4. Run the Application

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## ⚙️ Configuration & Safety

This tool includes configurable concurrency settings in `app.py`. **We strongly recommend adjusting these for safe, compliant operation.**

Open `app.py` and locate these variables near the top of the file:

```python
CONCURRENT_CHANNELS = 8   # Number of channels to scan simultaneously
CONCURRENT_DOWNLOADS = 15 # Number of attachments to download at once
```

### Recommended Safe Settings

| Variable | Default | Recommended | Description |
|----------|---------|-------------|-------------|
| `CONCURRENT_CHANNELS` | `8` | `1` | Set to `1` to fetch channels sequentially and avoid API abuse flags |
| `CONCURRENT_DOWNLOADS` | `15` | `5` | Set to `5` or lower to prevent rate limiting or IP-based restrictions |

> **⚠️ Important:** High concurrency settings may flag your account for API abuse. Discord actively monitors for aggressive API usage patterns. **We recommend keeping these values low** to ensure your bot token and account remain in good standing.

---

## 📖 How It Works

1. **Authentication** — You provide your Bot Token to authenticate via Discord's official API
2. **Server Access** — The bot connects to the specified server where it has been invited
3. **Sequential Fetching** — Message history is fetched sequentially via the official Discord API
4. **Filtering** — Messages are filtered by the User ID(s) you specify (for personal backup)
5. **Local Storage** — Data streams securely to local storage in JSON and TXT formats
6. **Export** — Download a ZIP archive or save directly to your `downloads/` folder

---

## 🔍 How to Get IDs

> **First:** Enable Developer Mode in Discord: **Settings → Advanced → Developer Mode**

| ID Type | How to Obtain |
|---------|---------------|
| **Bot Token** | Developer Portal → Your Application → Bot → Reset Token → Copy |
| **Server ID** | Right-click the server icon → "Copy Server ID" |
| **User ID** | Right-click your username → "Copy User ID" |

### About User ID Filtering

The **User ID** field filters the backup to only include messages from the specified user(s). This is intended for **backing up your own messages** rather than archiving an entire server.

- Leave blank to include all messages (requires appropriate permissions and use case)
- Enter your own User ID to back up only your personal message history
- Separate multiple IDs with commas: `123456789,987654321`

---

## 📁 Example Output

**Readable TXT format:**
```
================================================================================
  📝 My Server - Message Archive
  📊 Total Messages: 1,234
  📅 Exported: January 03, 2026 at 12:30 AM
================================================================================

--------------------------------------------------------------------------------
  #general
--------------------------------------------------------------------------------

[Jan 15, 2024 at 02:30 PM] YourName:
    Hello everyone! This is my message.
    [Attachment: photo.png]
```

---

## ❓ FAQ

**What permissions does the bot need?**
> Minimal permissions: "Read Message History" and "View Channels" only. No admin access required.

**Can it access private channels?**
> Only channels where the bot's role has explicit access permissions.

**Is my data sent anywhere?**
> No. This tool runs 100% locally. All data is stored on your machine and never transmitted to external servers.

**Is this compliant with Discord's Terms of Service?**
> When used responsibly for personal archival with safe rate limit settings, yes. Aggressive scraping or misuse may violate the ToS.

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid bot token" | Verify the token is complete; try resetting it in the Developer Portal |
| "Server not found" | Ensure the bot has been invited to the target server |
| "No messages found" | Verify your User ID is correct and you have messages in accessible channels |
| Python 3.13+ compatibility | Run `pip install audioop-lts` if you encounter audio-related errors |

---

## 🤝 Contributing

Contributions are welcome! Please ensure any changes maintain compliance with Discord's Terms of Service.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This software is provided "as-is" for personal archival purposes. The developers assume no liability for:

- Violations of Discord's Terms of Service
- Account suspensions or terminations resulting from misuse
- Privacy violations or non-compliance with data protection regulations (GDPR, CCPA, etc.)
- Any damages arising from the use of this software

**Use responsibly and at your own risk.**

---

**Made for personal data sovereignty and digital archival.**
