import requests, datetime, pyperclip, colorama, string, random, json, time, os
from playwright.sync_api import sync_playwright
from io import BytesIO

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def center(text):
    console_width = os.get_terminal_size().columns
    blank_lines = (os.get_terminal_size().lines // 2) - 1
    centered_text = text.center(console_width)
    return '\n' * blank_lines + centered_text

def timestamp():
    return f"{colorama.Fore.LIGHTBLUE_EX}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}{colorama.Style.RESET_ALL}"

def name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def save(image_bytes, format):
    folder = 'avatar'
    file_name = f"{name()}.{format.lower()}"
    
    with open(os.path.join(folder, file_name), 'wb') as img_file:
        img_file.write(image_bytes)

    return f"[{timestamp()}] scraped avatar > {file_name}"

def config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data = config('config.json')
delay = data.get('delay', 2)
format = data.get('format', 'jpg')

folder = 'avatar'
if not os.path.exists(folder):
    os.makedirs(folder)
    clear()
    folder_path = os.path.abspath(folder)
    print(center(f"[{timestamp()}] created avatar folder > {folder_path}"))
else:
    clear()
    folder_path = os.path.abspath(folder)
    print(center(f"[{timestamp()}] folder found > {folder_path}, copied to clipboard"))

pyperclip.copy(folder_path)
time.sleep(4)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    while True:
        clear()
        print(center(f"[{timestamp()}] scraping avatars"))
        page.goto("https://discord-tracker.com/avatars/")
        time.sleep(5)

        avatar_elements = page.query_selector_all('a img')
        scraped_count = 0

        if avatar_elements:
            for avatar in avatar_elements:
                avatar_url = avatar.get_attribute('src')
                if avatar_url and avatar_url.startswith('http'):
                    image_response = requests.get(avatar_url)
                    if image_response.status_code == 200:
                        image_bytes = BytesIO(image_response.content)
                        message = save(image_bytes.getvalue(), format)
                        clear()
                        print(center(message))
                        scraped_count += 1
                        time.sleep(0.5)

            clear()
            print(center(f"[{timestamp()}] scraped {scraped_count} avatars"))
            print(center(f"[{timestamp()}] scraping new avatars"))
            time.sleep(delay)
        else:
            clear()
            print(center(f"[{timestamp()}] retrying"))
            time.sleep(delay)
