# 🗄️ Discord Message Archiver

> **Download ALL your Discord messages locally - no size limits!**

A beautiful local web app that lets you archive your Discord messages from any server. Save your memories forever!

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![Discord.py](https://img.shields.io/badge/discord.py-2.3-blueviolet?logo=discord)
![License](https://img.shields.io/badge/License-MIT-yellow)

<p align="center">
  <img src="https://i.imgur.com/placeholder.png" alt="Screenshot" width="600">
</p>

## ✨ Features

- 🖥️ **Beautiful web interface** - runs locally on your PC
- 📥 **No size limits** - downloads directly to your computer
- 👥 **Multiple accounts** - archive all your alt accounts at once
- 📄 **Two formats** - JSON (full data) + human-readable TXT
- 🔒 **100% private** - everything runs on YOUR machine
- 🚀 **Easy to use** - just enter your IDs and click download

## 📦 What's in the Download?

Your ZIP file includes:

| File | Description |
|------|-------------|
| `*_messages.json` | Complete message data (for developers/backups) |
| `*_messages_readable.txt` | Easy-to-read text format |
| `archive_info.json` | Summary with stats |

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/discord-message-archiver.git
cd discord-message-archiver
pip install -r requirements.txt
```

### 2. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → name it → Create
3. Go to **"Bot"** section → Click **"Reset Token"** → Copy it
4. **Enable Intents** (scroll down on Bot page):
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT

### 3. Invite Bot to Your Server

1. In Developer Portal → **OAuth2** → **URL Generator**
2. Check scopes: `bot`
3. Check permissions: 
   - ☑️ Read Message History
   - ☑️ Read Messages/View Channels
4. Copy & open the URL to invite the bot

### 4. Run!

```bash
python app.py
```

Open **http://localhost:5000** in your browser 🎉

## 🔍 How to Get IDs

> **First:** Enable Developer Mode in Discord Settings → Advanced → Developer Mode

| What | How to Get |
|------|------------|
| **Bot Token** | Developer Portal → Bot → Reset Token → Copy |
| **Server ID** | Right-click server icon → "Copy Server ID" |
| **User ID** | Right-click your name → "Copy User ID" |

**Multiple accounts?** Comma-separate your User IDs: `123456789,987654321`

## 📖 How It Works

1. **You enter** your Bot Token, Server ID, and User ID(s)
2. **Bot connects** to Discord and finds the server
3. **Scans every channel** in the server
4. **Collects all messages** from your User ID(s)
5. **Creates a ZIP** with JSON + readable text files
6. **Downloads to your PC** - no Discord file limits!

## 📁 Example Output

**Readable TXT format:**
```
================================================================================
  📝 My Server - Message Archive
  📊 Total Messages: 1,234
  📅 Exported: December 30, 2024 at 02:30 PM
================================================================================

--------------------------------------------------------------------------------
  📢 #general
--------------------------------------------------------------------------------

[Jan 15, 2024 at 02:30 PM] YourName:
    Hello everyone! This is my first message!
    📎 Attachment: photo.png
    ⭐ Reactions: 👍×5 ❤️×3
```

## ❓ FAQ

**Does the bot need admin permissions?**
> No! Just "Read Message History" and "View Channels" - basic permissions only.

**Can it read private channels?**
> Only if the bot's role has access to them.

**Is there a message limit?**
> No! It downloads ALL messages from the beginning of time.

**Is my data safe?**
> Yes! Everything runs locally on your computer. Nothing is sent to any external server.

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Invalid bot token" | Make sure you copied the full token, try resetting it |
| "Server not found" | Make sure the bot is invited to the server |
| "No messages found" | Check your User ID is correct |
| Python 3.13+ errors | Run `pip install audioop-lts` |

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m 'Add cool feature'`)
4. Push to the branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💜 Support

If you find this useful, consider giving it a ⭐ on GitHub!

---

**Made with 💜 for preserving memories**
