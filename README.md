# 📥 Telegram Video Downloader

A Python script to download videos from private Telegram channels.

## ✨ Features

- ✅ Download videos from private channels without usernames
- ✅ Auto-detect all accessible channels
- ✅ Download all videos or only recent videos
- ✅ Download specific videos by message ID
- ✅ Real-time progress indicator
- ✅ Skip existing files
- ✅ Robust error handling

## 📋 Requirements

- Python 3.7+
- Telegram account already joined to target channel
- Telegram API credentials

## 🚀 Installation

### 1. Clone or Download Script
Download the `telegram_downloader.py` file to your computer.

### 2. Install Dependencies
```bash
pip install telethon
```

### 3. Get API Credentials
You need to obtain your own Telegram API credentials:

1. Visit https://my.telegram.org
2. Login with your phone number
3. Go to "API Development Tools"
4. Create a new application to get your `API_ID` and `API_HASH`
5. Update the script with your credentials:
   ```python
   API_ID = 'YOUR_API_ID'  # Replace with your API ID
   API_HASH = 'YOUR_API_HASH'  # Replace with your API Hash
   PHONE_NUMBER = 'YOUR_PHONE_NUMBER'  # Format: +1234567890
   ```

## 📱 How to Run

### 1. Run the Script
```bash
python telegram_downloader.py
```

### 2. First-time Login
When running for the first time:
- Script will ask for **OTP code** sent to your Telegram
- Enter the 5-digit code received
- Session will be saved for future use

### 3. Select Channel
The script will display a list of accessible channels/groups:
```
Available Channels/Groups:
--------------------------------------------------
1. My Private Channel
   ID: -1001234567890
   Username: No username

2. Family Group  
   ID: -987654321
   Username: No username

Select channel number: 1
```

### 4. Choose Download Mode
```
Select download mode:
1. Download all videos from channel
2. Download specific video by message ID
3. Download 10 latest videos

Enter choice (1/2/3): 3
```

## 📁 Download Location

Videos will be saved in the `downloads/` folder in the same directory as the script.

### For macOS:
```bash
# Open downloads folder in Finder
open downloads/

# Or check folder contents
ls -la downloads/
```

### For Windows:
```cmd
# Open downloads folder
explorer downloads\

# Or check folder contents  
dir downloads\
```

### For Linux:
```bash
# Open downloads folder
xdg-open downloads/

# Or check folder contents
ls -la downloads/
```

## 🎯 Download Modes

### 1. Download All Videos
- Downloads all videos available in the channel
- ⚠️ Be careful if the channel has many videos

### 2. Download Specific Video
- Enter a specific message ID
- How to get message ID: right-click on message → Copy Message Link
- ID is at the end of URL: `t.me/c/1234567890/12345` → ID = 12345

### 3. Download Latest Videos
- Downloads up to 10 latest videos found
- Script will check the 100 most recent messages for videos

## 📊 Example Output

```
INFO:__main__:Telegram client started successfully
INFO:__main__:Accessing channel: Premium Content Channel
INFO:__main__:Downloading: video_3303.mp4
INFO:__main__:Progress: 10.0%
INFO:__main__:Progress: 50.0%
INFO:__main__:Progress: 100.0%
INFO:__main__:Successfully downloaded: video_3303.mp4
INFO:__main__:Total videos downloaded: 5
```

## 🔧 Troubleshooting

### Error: "Phone number not registered"
- Make sure the phone number is registered with Telegram
- Use international format: +62812345678

### Error: "Chat not found"
- Make sure you've joined the channel
- Channel might be deleted or you were kicked

### Videos not appearing in folder
- Check download progress reaches 100%
- Ensure sufficient storage space
- Check downloads folder permissions

### Slow downloads
- Normal for large video files
- Speed depends on internet and Telegram servers
- Can pause with Ctrl+C and resume later

## ⚡ Usage Tips

1. **Start with latest videos** (option 3) for testing
2. **Don't close terminal** while download is running
3. **Monitor storage space** for large videos
4. **Backup credentials** if needed
5. **Use WiFi** for downloading many videos

## 🛡️ Security

- Session file (`session_name.session`) stores your login
- Don't share session file with others
- API credentials are securely configured

## 📝 File Format

Videos will be saved with format:
- **Name**: `video_[message_id].mp4`
- **Example**: `video_3303.mp4`, `video_3302.mp4`
- **Format**: As original (MP4, AVI, MKV)

## 🤝 Support

If you encounter issues:
1. Ensure all requirements are met
2. Check internet connection
3. Restart script if needed
4. Check error logs for details

---

**🎉 Happy downloading with Telegram Video Downloader!**

*This script is created to easily download videos from private Telegram channels without usernames.*
