import asyncio
import re
import os
import sys
import msvcrt
import json
from telethon import TelegramClient, events
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_FILE = 'config.json'
client = None
target_chat = None
interval = 300
message_text = 'میو'
is_running = False
task = None
always_login = False

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def print_menu(options, selected=0):
    print_logo()
    print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
    print(f"{Fore.CYAN}║      {Fore.YELLOW}Use ↑/↓ arrows to navigate{Fore.CYAN}      ║")
    print(f"{Fore.CYAN}║       {Fore.YELLOW}Press Enter to select{Fore.CYAN}           ║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
    print()
    
    for i, option in enumerate(options):
        if i == selected:
            print(f"{Fore.GREEN}▶ {option}{Style.RESET_ALL}")
        else:
            print(f"  {option}")
    
    status_color = Fore.GREEN if client else Fore.RED
    status_text = "✅ Logged in" if client else "❌ Not logged in"
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════╗")
    print(f"{Fore.CYAN}║  {Fore.YELLOW}Status:{Style.RESET_ALL} {status_color}{status_text}{Style.RESET_ALL}          {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
    print(f"\n{Fore.YELLOW}Press Ctrl+C to exit{Style.RESET_ALL}")

async def login_with_qr():
    global client
    print_logo()
    print(f"{Fore.CYAN}📱 Login with Phone Number{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. شماره موبایل خودت رو وارد کن{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. کد تایید رو از تلگرام دریافت کن{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3. وارد اکانتت میشی!{Style.RESET_ALL}")
    print()
    
    try:
        if always_login and os.path.exists('session.session'):
            print(f"{Fore.CYAN}🔐 استفاده از سشن ذخیره شده...{Style.RESET_ALL}")
            client = TelegramClient('session', 0, '')
            await client.start()
            print(f"\n{Fore.GREEN}✅ با موفقیت وارد شدی (از سشن)!{Style.RESET_ALL}")
        else:
            # اینجا دیگه از StringSession استفاده نمیکنیم
            client = TelegramClient('session', 0, '')
            await client.start()
            print(f"\n{Fore.GREEN}✅ با موفقیت وارد شدی!{Style.RESET_ALL}")
            if always_login:
                print(f"{Fore.CYAN}💾 سشن برای همیشه ذخیره شد{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ خطا: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
        return False

async def set_timer():
    global interval
    print_logo()
    print(f"{Fore.CYAN}⏰ Set Timer{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Current timer: {interval//60} minutes{Style.RESET_ALL}")
    print()
    
    try:
        minutes = input(f"{Fore.CYAN}Enter minutes (default 5): {Style.RESET_ALL}")
        if minutes.strip():
            interval = int(minutes) * 60
            save_config()
            print(f"{Fore.GREEN}✅ Timer set to {minutes} minutes{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✅ Timer kept at {interval//60} minutes{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}❌ Invalid input!{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

async def set_always_login():
    global always_login
    print_logo()
    print(f"{Fore.CYAN}🔐 Always Login Mode{Style.RESET_ALL}")
    
    if always_login:
        print(f"{Fore.GREEN}✅ Already enabled!{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}⚠️  با فعال‌سازی این گزینه، سشن شما برای همیشه ذخیره میشه{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚠️  دیگه نیازی به لاگین مجدد نخواهید داشت{Style.RESET_ALL}")
    confirm = input(f"{Fore.CYAN}Enable Always Login? (y/n): {Style.RESET_ALL}")
    
    if confirm.lower() == 'y':
        always_login = True
        save_config()
        print(f"{Fore.GREEN}✅ Always Login enabled!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💾 دفعه بعد با سشن ذخیره شده وارد میشی{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Cancelled{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

def support_us():
    print_logo()
    print(f"{Fore.CYAN}📢 Support Us{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}📱 Telegram Channel:{Style.RESET_ALL}")
    print(f"   {Fore.YELLOW}https://t.me/TaaKaaOrg{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}🐙 GitHub Repository:{Style.RESET_ALL}")
    print(f"   {Fore.YELLOW}https://github.com/ItzJustEren/TaaKaa-Self{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}📢 Support Group:{Style.RESET_ALL}")
    print(f"   {Fore.YELLOW}https://t.me/TaaKaaOrg{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}💡 Follow us for updates and support!{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

async def run_bot():
    global client, target_chat, interval, message_text, is_running, task
    
    print_logo()
    print(f"{Fore.GREEN}🚀 Starting TaaKaa-Self Bot...{Style.RESET_ALL}")
    
    if not client:
        print(f"{Fore.RED}❌ Please login first!{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to return...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}📝 Bot is running... Check Saved Messages{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 Type /start in Saved Messages to begin{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 Type /stop in Saved Messages to stop{Style.RESET_ALL}")
    
    @client.on(events.NewMessage(pattern='/start', from_me=True))
    async def start_command(event):
        await event.respond('🤖 Bot started!\n\nSend chat ID/link (e.g. @mygroup):')
    
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
                await event.respond(f'✅ Chat "{chat.title}" saved!\n⏰ Enter timer (minutes):')
            except Exception as e:
                await event.respond(f'❌ Invalid chat! Try again:\n{e}')
        
        elif interval == 300 and target_chat is not None:
            try:
                numbers = re.findall(r'\d+', msg)
                if numbers:
                    minutes = int(numbers[0])
                    interval = minutes * 60
                    save_config()
                    await event.respond(f'⏰ Timer: {minutes} minutes\n✏️ Enter message text:')
                else:
                    await event.respond('❌ Enter valid number (e.g. 5):')
            except:
                await event.respond('❌ Invalid input!')
        
        elif message_text == 'میو' and target_chat is not None and interval != 300:
            message_text = msg
            await event.respond(f'✅ Message saved: "{message_text}"\n🚀 Starting...')
            
            if is_running and task:
                task.cancel()
            
            is_running = True
            task = asyncio.create_task(send_periodic())
            await event.respond(f'✅ Bot active!\n📤 Sending "{message_text}" every {interval//60} minutes\n🛑 Send /stop to stop.')
    
    @client.on(events.NewMessage(pattern='/stop', from_me=True))
    async def stop_command(event):
        nonlocal is_running, task
        if is_running:
            is_running = False
            if task:
                task.cancel()
            await event.respond('⛔ Bot stopped! Send /start to restart.')
        else:
            await event.respond('⚠️ Bot is not running!')
    
    async def send_periodic():
        nonlocal is_running
        while is_running:
            try:
                if target_chat:
                    await client.send_message(target_chat, message_text)
                    print(f'{Fore.GREEN}✅ Message "{message_text}" sent to {target_chat.title}{Style.RESET_ALL}')
            except Exception as e:
                print(f'{Fore.RED}❌ Error: {e}{Style.RESET_ALL}')
            
            for _ in range(interval):
                if not is_running:
                    break
                await asyncio.sleep(1)
    
    await client.run_until_disconnected()

async def main_menu():
    load_config()
    
    options = [
        "Login with Phone Number",
        "Set Timer",
        "Set Always Login",
        "Support us (GitHub & Telegram)",
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
                    await login_with_qr()
                elif selected == 1:
                    await set_timer()
                elif selected == 2:
                    await set_always_login()
                elif selected == 3:
                    support_us()
                elif selected == 4:
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
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
