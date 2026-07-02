import asyncio
import re
import os
import sys
import json
from telethon import TelegramClient, events
from colorama import Fore, Style, init
import msvcrt

# ===== رنگ‌آمیزی =====
init(autoreset=True)

# ===== فایل کانفیگ =====
CONFIG_FILE = 'config.json'

# ===== متغیرهای گلوبال =====
client = None
target_chat = None
interval = 300
message_text = 'میو'
is_running = False
task = None
always_login = False

# ===== بارگذاری و ذخیره تنظیمات =====
def load_config():
    global interval, always_login
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                interval = config.get('interval', 300)
                always_login = config.get('always_login', False)
            return True
    except:
        pass
    return False

def save_config():
    config = {
        'interval': interval,
        'always_login': always_login
    }
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

# ===== پاک کردن صفحه =====
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ===== لوگو =====
def print_logo():
    clear_screen()
    logo = f"""
{Fore.GREEN}╔═══════════════════════════════════════╗
{Fore.GREEN}║                                       ║
{Fore.GREEN}║   {Fore.LIGHTGREEN_EX}████████╗  █████╗  █████╗  ██╗  ██╗  █████╗  █████╗  {Fore.GREEN}║
{Fore.GREEN}║   {Fore.LIGHTGREEN_EX}╚══██╔══╝ ██╔══██╗██╔══██╗██║ ██╔╝ ██╔══██╗██╔══██╗{Fore.GREEN}║
{Fore.GREEN}║   {Fore.LIGHTGREEN_EX}   ██║    ███████║███████║█████╔╝  ███████║███████║{Fore.GREEN}║
{Fore.GREEN}║   {Fore.LIGHTGREEN_EX}   ██║    ██╔══██║██╔══██║██╔═██╗  ██╔══██║██╔══██║{Fore.GREEN}║
{Fore.GREEN}║   {Fore.LIGHTGREEN_EX}   ██║    ██║  ██║██║  ██║██║  ██╗ ██║  ██║██║  ██║{Fore.GREEN}║
{Fore.GREEN}║                                       ║
{Fore.GREEN}║        {Fore.LIGHTGREEN_EX}✨ TaaKaa-Self Bot ✨{Fore.GREEN}        ║
{Fore.GREEN}╚═══════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(logo)

# ===== نمایش منو =====
def print_menu(options, selected=0):
    print_logo()
    print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
    print(f"{Fore.CYAN}║      {Fore.YELLOW}Use ↑/↓ arrows or 1-{len(options)} keys{Fore.CYAN}      ║")
    print(f"{Fore.CYAN}║       {Fore.YELLOW}Press Enter to select{Fore.CYAN}           ║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
    print()
    
    for i, option in enumerate(options):
        if i == selected:
            print(f"{Fore.GREEN}▶ {i+1}. {option}{Style.RESET_ALL}")
        else:
            print(f"  {i+1}. {option}")
    
    status_color = Fore.GREEN if client else Fore.RED
    status_text = "✅ Logged in" if client else "❌ Not logged in"
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════╗")
    print(f"{Fore.CYAN}║  {Fore.YELLOW}Status:{Style.RESET_ALL} {status_color}{status_text}{Style.RESET_ALL}          {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
    print(f"\n{Fore.YELLOW}Press Ctrl+C to exit{Style.RESET_ALL}")

# ===== تنظیم API =====
def set_api_credentials():
    print_logo()
    print(f"{Fore.CYAN}🔑 Environment Variables{Style.RESET_ALL}")
    print()
    
    api_id = input(f"{Fore.CYAN}Enter API_ID (number): {Style.RESET_ALL}").strip()
    if not api_id.isdigit():
        print(f"{Fore.RED}❌ Invalid API_ID!{Style.RESET_ALL}")
        input("Press Enter...")
        return
    
    api_hash = input(f"{Fore.CYAN}Enter API_HASH (string): {Style.RESET_ALL}").strip()
    if len(api_hash) < 10:
        print(f"{Fore.RED}❌ Invalid API_HASH!{Style.RESET_ALL}")
        input("Press Enter...")
        return
    
    os.environ['API_ID'] = api_id
    os.environ['API_HASH'] = api_hash
    print(f"\n{Fore.GREEN}✅ Saved successfully!{Style.RESET_ALL}")
    input("Press Enter...")

# ===== ورود با شماره =====
async def login_with_phone():
    global client
    print_logo()
    print(f"{Fore.CYAN}📱 Login with Phone Number{Style.RESET_ALL}")
    print()
    
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    
    if not api_id or not api_hash:
        print(f"{Fore.RED}❌ Set API credentials first!{Style.RESET_ALL}")
        input("Press Enter...")
        return
    
    try:
        client = TelegramClient('session', int(api_id), api_hash)
        await client.start()
        print(f"\n{Fore.GREEN}✅ Logged in successfully!{Style.RESET_ALL}")
        if always_login:
            print(f"{Fore.CYAN}💾 Session saved{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    
    input("Press Enter...")

# ===== تنظیم تایمر =====
async def set_timer():
    global interval
    print_logo()
    print(f"{Fore.CYAN}⏰ Set Timer (current: {interval//60} min){Style.RESET_ALL}")
    print()
    
    try:
        minutes = input(f"{Fore.CYAN}Enter minutes: {Style.RESET_ALL}").strip()
        if minutes:
            interval = int(minutes) * 60
            save_config()
            print(f"{Fore.GREEN}✅ Timer set to {minutes} minutes{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}❌ Invalid input!{Style.RESET_ALL}")
    
    input("Press Enter...")

# ===== Always Login =====
async def set_always_login():
    global always_login
    print_logo()
    print(f"{Fore.CYAN}🔐 Always Login Mode{Style.RESET_ALL}")
    print()
    
    if always_login:
        print(f"{Fore.GREEN}✅ Already enabled{Style.RESET_ALL}")
        input("Press Enter...")
        return
    
    confirm = input(f"{Fore.CYAN}Enable Always Login? (y/n): {Style.RESET_ALL}").lower()
    if confirm == 'y':
        always_login = True
        save_config()
        print(f"{Fore.GREEN}✅ Always Login enabled!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Cancelled{Style.RESET_ALL}")
    
    input("Press Enter...")

# ===== پشتیبانی =====
def support_us():
    print_logo()
    print(f"{Fore.CYAN}📢 Support{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}📱 Telegram: @TaaKaaOrg{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🐙 GitHub: ItzJustEren/TaaKaa-Self{Style.RESET_ALL}")
    input("\nPress Enter...")

# ===== اجرای ربات =====
async def run_bot():
    global client, target_chat, interval, message_text, is_running, task
    
    print_logo()
    print(f"{Fore.GREEN}🚀 Starting Bot...{Style.RESET_ALL}")
    
    if not client:
        print(f"{Fore.RED}❌ Login first!{Style.RESET_ALL}")
        input("Press Enter...")
        return
    
    print(f"{Fore.CYAN}📝 Check Saved Messages for /start{Style.RESET_ALL}")
    
    @client.on(events.NewMessage(pattern='/start', from_me=True))
    async def start_command(event):
        await event.respond('🤖 Bot started!\nSend chat ID/link:')
    
    @client.on(events.NewMessage(from_me=True))
    async def handle_messages(event):
        nonlocal target_chat, interval, message_text, is_running, task
        
        msg = event.message.text
        if not msg or msg.startswith('/'):
            return
        
        if target_chat is None:
            try:
                chat = await client.get_entity(msg)
                target_chat = chat
                await event.respond(f'✅ Chat "{chat.title}" saved!\nEnter timer (minutes):')
            except Exception as e:
                await event.respond(f'❌ Error: {e}')
        
        elif interval == 300 and target_chat:
            try:
                minutes = int(re.findall(r'\d+', msg)[0])
                interval = minutes * 60
                save_config()
                await event.respond(f'⏰ Timer: {minutes} min\nEnter message text:')
            except:
                await event.respond('❌ Enter a number!')
        
        elif message_text == 'میو' and target_chat and interval != 300:
            message_text = msg
            await event.respond(f'✅ Message: "{message_text}"\n🚀 Starting...')
            
            if is_running and task:
                task.cancel()
            
            is_running = True
            task = asyncio.create_task(send_periodic())
            await event.respond(f'✅ Active! Sending every {interval//60} min\nSend /stop to stop.')
    
    @client.on(events.NewMessage(pattern='/stop', from_me=True))
    async def stop_command(event):
        nonlocal is_running, task
        if is_running:
            is_running = False
            if task:
                task.cancel()
            await event.respond('⛔ Stopped! Send /start to restart.')
        else:
            await event.respond('⚠️ Not running!')
    
    async def send_periodic():
        nonlocal is_running
        while is_running:
            try:
                if target_chat:
                    await client.send_message(target_chat, message_text)
                    print(f'{Fore.GREEN}✅ Sent "{message_text}" to {target_chat.title}{Style.RESET_ALL}')
            except Exception as e:
                print(f'{Fore.RED}❌ Error: {e}{Style.RESET_ALL}')
            
            for _ in range(interval):
                if not is_running:
                    break
                await asyncio.sleep(1)
    
    await client.run_until_disconnected()

# ===== منوی اصلی =====
async def main_menu():
    load_config()
    options = [
        "Environment Variables",
        "Login with Phone",
        "Set Timer",
        "Always Login",
        "Support",
        "Start Bot"
    ]
    selected = 0
    
    while True:
        print_menu(options, selected)
        try:
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    selected = (selected - 1) % len(options)
                elif key == b'P':
                    selected = (selected + 1) % len(options)
            elif key == b'\r':
                clear_screen()
                if selected == 0:
                    set_api_credentials()
                elif selected == 1:
                    await login_with_phone()
                elif selected == 2:
                    await set_timer()
                elif selected == 3:
                    await set_always_login()
                elif selected == 4:
                    support_us()
                elif selected == 5:
                    await run_bot()
            elif key == b'\x03':
                clear_screen()
                print(f"{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
                break
        except:
            pass

if __name__ == '__main__':
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        clear_screen()
        print(f"{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        input("Press Enter...")
