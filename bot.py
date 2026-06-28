import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import webbrowser
import qrcode
from PIL import Image

print("🤖 TaaKaa-Self Bot - Login with QR Code")
print("=" * 50)
print("📱 1. یه QR کد برات میاد")
print("📱 2. با تلگرام گوشی اسکنش کن")
print("📱 3. وارد اکانتت میشی بدون نیاز به api!")
print("=" * 50)

async def main():
    # با یه سشن خالی شروع کن (نیاز به api نداره!)
    client = TelegramClient(StringSession(), 0, '')
    
    # لاگین با QR کد
    await client.start()
    
    print("\n✅ با موفقیت وارد شدی!")
    print("📝 حالا برو به Saved Messages و بنویس /start")
    print("📝 برای خروج Ctrl+C رو بزن")
    
    # متغیرها
    target_chat = None
    interval = 300  # ۵ دقیقه
    message_text = 'میو'
    is_running = False
    task = None
    
    @client.on(events.NewMessage(pattern='/start', from_me=True))
    async def start_command(event):
        await event.respond('🤖 ربات راه‌اندازی شد!\n\nلطفاً آیدی یا لینک گپ موردنظر رو وارد کن:\n(مثل @mygroup یا https://t.me/mygroup)')
    
    @client.on(events.NewMessage(from_me=True))
    async def handle_messages(event):
        nonlocal target_chat, interval, message_text, is_running, task
        
        msg = event.message.text
        if not msg or msg.startswith('/'):
            return
        
        # مرحله ۱: دریافت آیدی گپ
        if target_chat is None:
            try:
                chat = await client.get_entity(msg)
                target_chat = chat
                await event.respond(f'✅ گپ "{chat.title}" ذخیره شد!\n⏰ زمان بین ارسال پیام‌ها رو وارد کن (مثلاً ۵):')
            except Exception as e:
                await event.respond(f'❌ خطا! گپ پیدا نشد. دوباره تلاش کن:\n{e}')
        
        # مرحله ۲: دریافت زمان
        elif interval == 300 and target_chat is not None:
            try:
                numbers = re.findall(r'\d+', msg)
                if numbers:
                    minutes = int(numbers[0])
                    interval = minutes * 60
                    await event.respond(f'⏰ زمان تنظیم شد: هر {minutes} دقیقه\n✏️ پیام مورد نظر رو وارد کن (مثلاً میو):')
                else:
                    await event.respond('❌ عدد معتبر وارد کن! مثل: 5')
            except:
                await event.respond('❌ خطا! عدد معتبر وارد کن.')
        
        # مرحله ۳: دریافت پیام
        elif message_text == 'میو' and target_chat is not None and interval != 300:
            message_text = msg
            await event.respond(f'✅ پیام ذخیره شد: "{message_text}"\n🚀 شروع ارسال هر {interval//60} دقیقه...')
            
            if is_running and task:
                task.cancel()
            
            is_running = True
            task = asyncio.create_task(send_periodic())
            await event.respond('✅ ربات فعال شد! برای توقف /stop رو بزن.')
    
    @client.on(events.NewMessage(pattern='/stop', from_me=True))
    async def stop_command(event):
        nonlocal is_running, task
        if is_running:
            is_running = False
            if task:
                task.cancel()
            await event.respond('⛔ ربات متوقف شد!')
        else:
            await event.respond('⚠️ ربات در حال اجرا نیست!')
    
    async def send_periodic():
        nonlocal is_running
        while is_running:
            try:
                if target_chat:
                    await client.send_message(target_chat, message_text)
                    print(f'✅ "{message_text}" فرستاده شد به {target_chat.title}')
            except Exception as e:
                print(f'❌ خطا: {e}')
            
            # شمارش معکوس
            for _ in range(interval):
                if not is_running:
                    break
                await asyncio.sleep(1)
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 خداحافظ!")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        input("Enter بزن تا خارج شی...")
