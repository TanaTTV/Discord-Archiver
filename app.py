"""
Discord Message Archiver - SPEED OPTIMIZED EDITION
Features:
- Parallel channel scanning (5x faster)
- No slow HTML generation
- Instant JSON saves
- Stream to disk
"""

import asyncio
import json
import os
import io
import zipfile
import threading
import aiohttp
import base64
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import discord
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION - SPEED SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════

CONCURRENT_CHANNELS = 8  # Scan 8 channels simultaneously
CONCURRENT_DOWNLOADS = 15  # Download 15 attachments at once

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL STATE
# ═══════════════════════════════════════════════════════════════════════════════

download_progress = {
    "status": "idle",
    "message": "",
    "current_channel": "",
    "channels_done": 0,
    "total_channels": 0,
    "messages_found": 0,
    "attachments_downloaded": 0,
    "total_attachments": 0,
    "percent": 0
}

downloaded_data = {
    "messages": [],
    "server_name": "",
    "attachments": {},
    "ready": False,
    "options": {}
}

server_channels = {
    "channels": [],
    "server_name": ""
}

OUTPUT_FOLDER = Path("downloads")
OUTPUT_FOLDER.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

def format_message(msg: discord.Message) -> dict:
    """Convert Discord message to dict - FAST version"""
    return {
        "id": str(msg.id),
        "timestamp": msg.created_at.isoformat(),
        "author": {
            "id": str(msg.author.id),
            "name": msg.author.name,
            "display_name": msg.author.display_name,
            "is_bot": msg.author.bot
        },
        "content": msg.content,
        "channel": {
            "id": str(msg.channel.id),
            "name": getattr(msg.channel, 'name', 'DM')
        },
        "attachments": [
            {"filename": att.filename, "url": att.url, "size": att.size}
            for att in msg.attachments
        ],
        "reactions": [
            {"emoji": str(r.emoji), "count": r.count}
            for r in msg.reactions
        ] if msg.reactions else [],
        "reply_to": str(msg.reference.message_id) if msg.reference else None
    }


def format_timestamp(iso_string: str) -> str:
    """Convert ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return iso_string


def create_readable_txt(messages: list, title: str) -> str:
    """Create human-readable text - OPTIMIZED"""
    lines = [
        "=" * 80,
        f"  {title}",
        f"  Total Messages: {len(messages):,}",
        f"  Exported: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        "=" * 80,
        ""
    ]
    
    current_channel = None
    for msg in messages:
        ch = msg["channel"]["name"]
        if ch != current_channel:
            current_channel = ch
            lines.extend(["", "-" * 80, f"  #{current_channel}", "-" * 80, ""])
        
        ts = format_timestamp(msg["timestamp"])
        author = msg["author"]["display_name"]
        bot = " [BOT]" if msg["author"].get("is_bot") else ""
        content = msg["content"] or "[No text]"
        
        lines.append(f"[{ts}] {author}{bot}:")
        lines.extend(f"    {line}" for line in content.split('\n'))
        
        for att in msg.get("attachments", []):
            lines.append(f"    [Attachment: {att['filename']}]")
        
        lines.append("")
    
    lines.extend(["=" * 80, "  End of Archive", "=" * 80])
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# ZIP CREATION - FAST VERSION (NO HTML)
# ═══════════════════════════════════════════════════════════════════════════════

def create_zip_fast(messages: list, server_name: str, attachments: dict, options: dict) -> io.BytesIO:
    """Create ZIP without slow HTML generation"""
    zip_buffer = io.BytesIO()
    safe_name = "".join(c for c in server_name if c.isalnum() or c in (' ', '-', '_')).strip()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Main JSON
        zf.writestr(f"{safe_name}_messages.json", 
                   json.dumps(messages, indent=2, ensure_ascii=False))
        
        # Readable TXT
        zf.writestr(f"{safe_name}_readable.txt",
                   create_readable_txt(messages, f"{server_name} - Archive"))
        
        # Per-user files if requested
        if options.get("separate_users"):
            users = {}
            for msg in messages:
                uid = msg["author"]["id"]
                if uid not in users:
                    users[uid] = {"name": msg["author"]["display_name"], "msgs": []}
                users[uid]["msgs"].append(msg)
            
            for uid, data in users.items():
                uname = "".join(c for c in data["name"] if c.isalnum() or c in (' ', '-', '_')).strip()
                zf.writestr(f"by_user/{uname}_{uid}.json",
                           json.dumps(data["msgs"], indent=2, ensure_ascii=False))
        
        # Per-channel files
        channels = {}
        for msg in messages:
            ch = msg["channel"]["name"]
            if ch not in channels:
                channels[ch] = []
            channels[ch].append(msg)
        
        for ch_name, ch_msgs in channels.items():
            safe_ch = "".join(c for c in ch_name if c.isalnum() or c in (' ', '-', '_')).strip()
            zf.writestr(f"by_channel/{safe_ch}.txt",
                       create_readable_txt(ch_msgs, f"#{ch_name}"))
        
        # Attachments
        for filename, data in attachments.items():
            try:
                zf.writestr(f"attachments/{filename}", base64.b64decode(data))
            except:
                pass
        
        # Summary
        user_counts = {}
        for msg in messages:
            uid = msg["author"]["id"]
            if uid not in user_counts:
                user_counts[uid] = {"name": msg["author"]["display_name"], "is_bot": msg["author"].get("is_bot"), "count": 0}
            user_counts[uid]["count"] += 1
        
        summary = {
            "server": server_name,
            "exported": datetime.now().isoformat(),
            "total_messages": len(messages),
            "total_attachments": len(attachments),
            "channels": sorted(channels.keys()),
            "users": sorted(user_counts.values(), key=lambda x: x["count"], reverse=True),
            "date_range": {
                "oldest": messages[0]["timestamp"] if messages else None,
                "newest": messages[-1]["timestamp"] if messages else None
            }
        }
        zf.writestr("archive_info.json", json.dumps(summary, indent=2))
    
    zip_buffer.seek(0)
    return zip_buffer


# ═══════════════════════════════════════════════════════════════════════════════
# PARALLEL CHANNEL SCANNING
# ═══════════════════════════════════════════════════════════════════════════════

async def scan_channel(channel, user_ids: list, include_bots: bool, date_from, date_to) -> list:
    """Scan a single channel - returns list of messages"""
    messages = []
    try:
        async for msg in channel.history(limit=None, oldest_first=True, after=date_from, before=date_to):
            if user_ids and msg.author.id not in user_ids:
                continue
            if not include_bots and msg.author.bot:
                continue
            messages.append(format_message(msg))
    except discord.Forbidden:
        pass
    except Exception as e:
        print(f"Error scanning {channel.name}: {e}")
    return messages


async def download_attachment(session: aiohttp.ClientSession, url: str, filename: str) -> tuple:
    """Download single attachment"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status == 200:
                data = await resp.read()
                if len(data) <= 25 * 1024 * 1024:  # 25MB limit
                    return (filename, base64.b64encode(data).decode())
    except:
        pass
    return (filename, None)


async def run_discord_download(bot_token: str, server_id: int, user_ids: list, options: dict):
    """PARALLEL channel scanning - FAST"""
    global download_progress, downloaded_data
    
    download_progress["status"] = "connecting"
    download_progress["message"] = "Connecting to Discord..."
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    intents.guilds = True
    intents.members = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        global download_progress, downloaded_data
        
        try:
            download_progress["message"] = f"Connected as {client.user.name}!"
            
            guild = client.get_guild(server_id)
            if not guild:
                download_progress["status"] = "error"
                download_progress["message"] = "Server not found! Make sure bot is invited."
                await client.close()
                return
            
            download_progress["status"] = "scanning"
            download_progress["message"] = f"Scanning {guild.name} with {CONCURRENT_CHANNELS}x parallel..."
            
            # Filter channels
            channels = guild.text_channels
            selected = options.get("channels", [])
            if selected:
                channels = [c for c in channels if str(c.id) in selected]
            
            download_progress["total_channels"] = len(channels)
            
            # Parse dates
            date_from = date_to = None
            if options.get("date_from"):
                try:
                    date_from = datetime.fromisoformat(options["date_from"]).replace(tzinfo=timezone.utc)
                except:
                    pass
            if options.get("date_to"):
                try:
                    date_to = datetime.fromisoformat(options["date_to"]).replace(tzinfo=timezone.utc)
                except:
                    pass
            
            include_bots = options.get("include_bots", True)
            all_messages = []
            attachment_urls = []
            
            # PARALLEL SCANNING with real-time updates
            async def scan_and_update(channel):
                """Scan channel and update progress immediately"""
                nonlocal all_messages, attachment_urls
                
                download_progress["current_channel"] = channel.name
                msgs = await scan_channel(channel, user_ids, include_bots, date_from, date_to)
                
                for msg in msgs:
                    msg["server"] = guild.name
                    all_messages.append(msg)
                    if options.get("download_attachments"):
                        for att in msg.get("attachments", []):
                            attachment_urls.append((att["url"], att["filename"]))
                
                download_progress["channels_done"] += 1
                download_progress["messages_found"] = len(all_messages)
                download_progress["total_attachments"] = len(attachment_urls)
                download_progress["percent"] = int((download_progress["channels_done"] / len(channels)) * 100)
                
                return len(msgs)
            
            # Create semaphore to limit concurrent channels
            sem = asyncio.Semaphore(CONCURRENT_CHANNELS)
            
            async def scan_with_limit(channel):
                async with sem:
                    return await scan_and_update(channel)
            
            # Start all scans with concurrency limit
            tasks = [scan_with_limit(ch) for ch in channels]
            await asyncio.gather(*tasks)
            
            # PARALLEL ATTACHMENT DOWNLOADS
            attachments_data = {}
            if options.get("download_attachments") and attachment_urls:
                download_progress["status"] = "downloading"
                download_progress["message"] = f"Downloading {len(attachment_urls)} attachments..."
                
                async with aiohttp.ClientSession() as session:
                    for i in range(0, len(attachment_urls), CONCURRENT_DOWNLOADS):
                        batch = attachment_urls[i:i + CONCURRENT_DOWNLOADS]
                        tasks = [download_attachment(session, url, f"{i+j}_{fn}") 
                                for j, (url, fn) in enumerate(batch)]
                        results = await asyncio.gather(*tasks)
                        
                        for fn, data in results:
                            if data:
                                attachments_data[fn] = data
                        
                        download_progress["attachments_downloaded"] = min(i + CONCURRENT_DOWNLOADS, len(attachment_urls))
                        download_progress["percent"] = int((download_progress["attachments_downloaded"] / len(attachment_urls)) * 100)
            
            # Sort and save
            all_messages.sort(key=lambda x: x["timestamp"])
            
            downloaded_data["messages"] = all_messages
            downloaded_data["server_name"] = guild.name
            downloaded_data["attachments"] = attachments_data
            downloaded_data["ready"] = True
            downloaded_data["options"] = options
            
            download_progress["status"] = "complete"
            download_progress["message"] = f"Done! {len(all_messages):,} messages from {guild.name}"
            
        except Exception as e:
            download_progress["status"] = "error"
            download_progress["message"] = str(e)
        
        await client.close()
    
    try:
        await client.start(bot_token)
    except discord.LoginFailure:
        download_progress["status"] = "error"
        download_progress["message"] = "Invalid bot token!"
    except Exception as e:
        download_progress["status"] = "error"
        download_progress["message"] = str(e)


async def fetch_server_channels(bot_token: str, server_id: int):
    """Fetch channels for selection"""
    global server_channels
    
    intents = discord.Intents.default()
    intents.guilds = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        global server_channels
        try:
            guild = client.get_guild(server_id)
            if guild:
                server_channels["server_name"] = guild.name
                server_channels["channels"] = [
                    {"id": str(c.id), "name": c.name, "category": c.category.name if c.category else "No Category"}
                    for c in guild.text_channels
                ]
        except:
            pass
        await client.close()
    
    try:
        await client.start(bot_token)
    except:
        pass


def start_download_thread(bot_token: str, server_id: int, user_ids: list, options: dict):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_discord_download(bot_token, server_id, user_ids, options))
    loop.close()


def start_fetch_channels_thread(bot_token: str, server_id: int):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_server_channels(bot_token, server_id))
    loop.close()


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/fetch-channels', methods=['POST'])
def fetch_channels():
    global server_channels
    
    data = request.json
    bot_token = data.get('bot_token', '').strip()
    server_id = data.get('server_id', '').strip()
    
    if not bot_token or not server_id:
        return jsonify({"error": "Bot token and Server ID required"}), 400
    
    try:
        server_id = int(server_id)
    except:
        return jsonify({"error": "Invalid Server ID"}), 400
    
    server_channels = {"channels": [], "server_name": ""}
    
    thread = threading.Thread(target=start_fetch_channels_thread, args=(bot_token, server_id))
    thread.start()
    thread.join(timeout=15)
    
    if server_channels["channels"]:
        return jsonify(server_channels)
    return jsonify({"error": "Could not fetch channels"}), 400


@app.route('/api/start', methods=['POST'])
def start_download():
    global download_progress, downloaded_data
    
    data = request.json
    bot_token = data.get('bot_token', '').strip()
    server_id = data.get('server_id', '').strip()
    user_ids = data.get('user_ids', '').strip()
    
    options = {
        "include_bots": data.get('include_bots', True),
        "download_attachments": data.get('download_attachments', False),
        "separate_users": data.get('separate_users', False),
        "date_from": data.get('date_from', ''),
        "date_to": data.get('date_to', ''),
        "channels": data.get('channels', [])
    }
    
    if not bot_token:
        return jsonify({"error": "Bot token required"}), 400
    if not server_id:
        return jsonify({"error": "Server ID required"}), 400
    
    try:
        server_id = int(server_id)
        user_id_list = []
        if user_ids:
            user_id_list = [int(uid.strip()) for uid in user_ids.split(',') if uid.strip()]
    except:
        return jsonify({"error": "Invalid ID format"}), 400
    
    download_progress = {
        "status": "starting",
        "message": "Starting...",
        "current_channel": "",
        "channels_done": 0,
        "total_channels": 0,
        "messages_found": 0,
        "attachments_downloaded": 0,
        "total_attachments": 0,
        "percent": 0
    }
    downloaded_data = {"messages": [], "server_name": "", "attachments": {}, "ready": False}
    
    thread = threading.Thread(target=start_download_thread, args=(bot_token, server_id, user_id_list, options))
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True})


@app.route('/api/progress')
def get_progress():
    return jsonify(download_progress)


@app.route('/api/download')
def download_file():
    """Fast ZIP download - NO HTML"""
    global downloaded_data
    
    if not downloaded_data.get("ready"):
        return jsonify({"error": "No download ready"}), 400
    
    messages = downloaded_data["messages"]
    server_name = downloaded_data["server_name"]
    attachments = downloaded_data.get("attachments", {})
    options = downloaded_data.get("options", {})
    
    if not messages:
        return jsonify({"error": "No messages"}), 400
    
    zip_buffer = create_zip_fast(messages, server_name, attachments, options)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in server_name if c.isalnum() or c in (' ', '-', '_')).strip()
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{safe_name}_archive_{timestamp}.zip"
    )


@app.route('/api/quick-save')
def quick_save():
    """INSTANT save - just JSON to disk"""
    global downloaded_data
    
    if not downloaded_data.get("messages"):
        return jsonify({"error": "No messages in memory"}), 400
    
    messages = downloaded_data["messages"]
    server_name = downloaded_data.get("server_name", "backup")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in server_name if c.isalnum() or c in (' ', '-', '_')).strip()
    
    # Save JSON
    json_path = OUTPUT_FOLDER / f"{safe_name}_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False)
    
    return jsonify({
        "success": True,
        "messages": len(messages),
        "file": str(json_path.absolute()),
        "size_mb": round(json_path.stat().st_size / 1024 / 1024, 2)
    })


@app.route('/api/save-local')
def save_local():
    """Save ZIP to disk"""
    global downloaded_data
    
    if not downloaded_data.get("ready"):
        return jsonify({"error": "No download ready"}), 400
    
    messages = downloaded_data["messages"]
    server_name = downloaded_data["server_name"]
    attachments = downloaded_data.get("attachments", {})
    options = downloaded_data.get("options", {})
    
    if not messages:
        return jsonify({"error": "No messages"}), 400
    
    zip_buffer = create_zip_fast(messages, server_name, attachments, options)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in server_name if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{safe_name}_archive_{timestamp}.zip"
    
    filepath = OUTPUT_FOLDER / filename
    with open(filepath, 'wb') as f:
        f.write(zip_buffer.read())
    
    return jsonify({
        "success": True,
        "path": str(filepath.absolute()),
        "filename": filename,
        "size_mb": round(filepath.stat().st_size / 1024 / 1024, 2)
    })


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    print("""
+===============================================================================+
|           DISCORD MESSAGE ARCHIVER - SPEED OPTIMIZED EDITION                  |
+===============================================================================+
|                                                                               |
|   OPTIMIZATIONS:                                                              |
|     [x] Parallel scanning: 8 channels at once                                 |
|     [x] Parallel downloads: 15 attachments at once                            |
|     [x] No slow HTML generation                                               |
|     [x] Instant JSON save endpoint                                            |
|                                                                               |
|   Open: http://localhost:5000                                                 |
|                                                                               |
|   Quick Save: http://localhost:5000/api/quick-save                            |
|                                                                               |
+===============================================================================+
    """)
    app.run(debug=False, port=5000, threaded=True)
