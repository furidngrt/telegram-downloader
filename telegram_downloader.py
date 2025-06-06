import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfigurasi API Telegram
API_ID = 187435677  # API ID dari my.telegram.org
API_HASH = 'API_HASH'  # API Hash dari my.telegram.org
PHONE_NUMBER = 'NUMBER'  # Format: +178634764

# Konfigurasi download
CHANNEL_ID = None  # Akan diisi dengan Chat ID channel (contoh: -1001234567890)
DOWNLOAD_PATH = './downloads/'  # Folder untuk menyimpan file

class TelegramDownloader:
    def __init__(self, api_id, api_hash, phone_number):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone_number = phone_number
        
    async def get_channel_list(self):
        """Menampilkan daftar channel/group yang bisa diakses"""
        logger.info("Mengambil daftar channel/group...")
        
        dialogs = await self.client.get_dialogs()
        channels = []
        
        for dialog in dialogs:
            if dialog.is_channel or dialog.is_group:
                channels.append({
                    'id': dialog.entity.id,
                    'title': dialog.title,
                    'username': getattr(dialog.entity, 'username', None)
                })
        
        return channels
    
    async def display_channels(self):
        """Menampilkan channel yang tersedia untuk dipilih"""
        channels = await self.get_channel_list()
        
        print("\nDaftar Channel/Group yang tersedia:")
        print("-" * 50)
        for i, channel in enumerate(channels, 1):
            username_info = f"@{channel['username']}" if channel['username'] else "No username"
            print(f"{i}. {channel['title']}")
            print(f"   ID: {channel['id']}")
            print(f"   Username: {username_info}")
            print()
        
        return channels
        
    async def start_client(self):
        """Memulai client Telegram"""
        await self.client.start(phone=self.phone_number)
        logger.info("Client Telegram berhasil dimulai")
        
    async def download_videos_from_channel(self, channel_identifier, download_path, limit=None):
        """
        Download video dari channel Telegram
        
        Args:
            channel_identifier: Channel ID (integer) atau username (string dengan @)
            download_path: Path untuk menyimpan file
            limit: Batasan jumlah pesan yang diproses (None = semua)
        """
        # Buat folder download jika belum ada
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            
        try:
            # Ambil entity channel
            entity = await self.client.get_entity(channel_identifier)
            logger.info(f"Mengakses channel: {entity.title}")
            
            # Counter untuk video yang didownload
            video_count = 0
            
            # Iterasi melalui pesan di channel
            async for message in self.client.iter_messages(entity, limit=limit):
                if message.media:
                    # Cek apakah media adalah video
                    if isinstance(message.media, MessageMediaDocument):
                        # Cek apakah dokumen adalah video
                        if message.media.document.mime_type and message.media.document.mime_type.startswith('video/'):
                            try:
                                # Buat nama file
                                file_name = f"video_{message.id}"
                                
                                # Ambil ekstensi dari mime type
                                if message.media.document.mime_type == 'video/mp4':
                                    file_name += '.mp4'
                                elif message.media.document.mime_type == 'video/avi':
                                    file_name += '.avi'
                                elif message.media.document.mime_type == 'video/mkv':
                                    file_name += '.mkv'
                                else:
                                    file_name += '.video'
                                
                                file_path = os.path.join(download_path, file_name)
                                
                                # Skip jika file sudah ada
                                if os.path.exists(file_path):
                                    logger.info(f"File sudah ada: {file_name}")
                                    continue
                                
                                logger.info(f"Mendownload: {file_name}")
                                
                                # Download file
                                await self.client.download_media(
                                    message, 
                                    file=file_path,
                                    progress_callback=self.progress_callback
                                )
                                
                                video_count += 1
                                logger.info(f"Berhasil download: {file_name}")
                                
                            except Exception as e:
                                logger.error(f"Error download video {message.id}: {e}")
                                
            logger.info(f"Total video berhasil didownload: {video_count}")
            
        except Exception as e:
            logger.error(f"Error mengakses channel: {e}")
            
    async def download_specific_message(self, channel_identifier, message_id, download_path):
        """Download video dari pesan tertentu"""
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            
        try:
            entity = await self.client.get_entity(channel_identifier)
            message = await self.client.get_messages(entity, ids=message_id)
            
            if message and message.media:
                if isinstance(message.media, MessageMediaDocument):
                    if message.media.document.mime_type and message.media.document.mime_type.startswith('video/'):
                        file_name = f"video_{message_id}.mp4"
                        file_path = os.path.join(download_path, file_name)
                        
                        logger.info(f"Mendownload pesan {message_id}: {file_name}")
                        await self.client.download_media(
                            message, 
                            file=file_path,
                            progress_callback=self.progress_callback
                        )
                        logger.info(f"Berhasil download: {file_name}")
                    else:
                        logger.info("Pesan bukan video")
                else:
                    logger.info("Pesan tidak memiliki media")
            else:
                logger.info("Pesan tidak ditemukan")
                
        except Exception as e:
            logger.error(f"Error download pesan {message_id}: {e}")
    
    def progress_callback(self, current, total):
        """Callback untuk menampilkan progress download"""
        percentage = (current / total) * 100
        if int(percentage) % 10 == 0:  # Tampilkan setiap 10%
            logger.info(f"Progress: {percentage:.1f}%")
    
    async def close_client(self):
        """Tutup client"""
        await self.client.disconnect()
        logger.info("Client Telegram ditutup")

async def main():
    # Inisialisasi downloader
    downloader = TelegramDownloader(API_ID, API_HASH, PHONE_NUMBER)
    
    try:
        # Start client
        await downloader.start_client()
        
        # Pilih channel terlebih dahulu
        print("Mencari channel yang tersedia...")
        channels = await downloader.display_channels()
        
        if not channels:
            print("Tidak ada channel yang ditemukan!")
            return
        
        # Pilih channel
        while True:
            try:
                choice = int(input("Pilih nomor channel: ")) - 1
                if 0 <= choice < len(channels):
                    selected_channel = channels[choice]
                    channel_id = selected_channel['id']
                    print(f"Channel dipilih: {selected_channel['title']} (ID: {channel_id})")
                    break
                else:
                    print("Nomor tidak valid!")
            except ValueError:
                print("Masukkan nomor yang valid!")
        
        # Pilihan download
        print("\nPilih mode download:")
        print("1. Download semua video dari channel")
        print("2. Download video tertentu berdasarkan message ID")
        print("3. Download 10 video terbaru")
        
        choice = input("Masukkan pilihan (1/2/3): ")
        
        if choice == '1':
            # Download semua video
            await downloader.download_videos_from_channel(
                channel_id, 
                DOWNLOAD_PATH
            )
        elif choice == '2':
            # Download video tertentu
            message_id = int(input("Masukkan message ID: "))
            await downloader.download_specific_message(
                channel_id, 
                message_id, 
                DOWNLOAD_PATH
            )
        elif choice == '3':
            # Download 10 video terbaru
            await downloader.download_videos_from_channel(
                channel_id, 
                DOWNLOAD_PATH, 
                limit=100  # Cek 100 pesan terbaru untuk mencari video
            )
        else:
            print("Pilihan tidak valid")
            
    except Exception as e:
        logger.error(f"Error dalam main: {e}")
    finally:
        # Tutup client
        await downloader.close_client()

if __name__ == "__main__":
    # Pastikan event loop berjalan dengan benar
    asyncio.run(main())
