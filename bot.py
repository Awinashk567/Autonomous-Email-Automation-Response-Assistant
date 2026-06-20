import threading
from flask import Flask
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time
from openai import OpenAI

# --- DUMMY WEB SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Awinash's AOL Bot is Running 24/7 on Cloud!"

def run_flask():
    # Render khud ek PORT deta hai, warna default 5000 use hoga
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- BOT CONFIGURATION ---
load_dotenv()
EMAIL = os.getenv("AOL_EMAIL", "")
PASSWORD = os.getenv("AOL_PASSWORD", "") 
STATE_FILE = "aol_session.json"
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

# 🛠️ POINTING TO GROQ
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=OPENAI_KEY,
)

# 🧠 THE UPGRADED AI BRAIN FUNCTION
def get_ai_reply(sender, subject, body):
    try:
        print("🧠 Thinking... Generating human-like AI reply via Groq...")
        prompt = f"""
        You are Awinash Kumar. Write a natural, human-like reply to the following incoming email.
        
        Guidelines:
        - Write EXACTLY as a human (as Awinash). NEVER mention being an AI, automated bot, or assistant.
        - If the sender is family (like mom/dad) or a friend, use a warm, casual, and loving tone. Use natural greetings.
        - If it's a professional email, be polite but keep it natural.
        - Keep the reply concise (2-3 sentences).
        - Always end the email EXACTLY with this signature block:

        Awinash Kumar
        Mo: 72________
        Email: {EMAIL}

        Sender: {sender}
        Subject: {subject}
        Email Body: {body}
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n❌ AI ERROR DETECTED: {e}\n")
        return f"Hello,\n\nI have received your email regarding '{subject}' and will get back to you shortly.\n\nAwinash Kumar\nMo: 72________\nEmail: {EMAIL}"

# 👻 SAFE POPUP KILLER FUNCTION
def clear_popups(page):
    try:
        popup_selectors = [
            'button:has-text("Got it")', 
            'button:has-text("Dismiss")',
            'span[title="Close"]',
            'text="Got it"'
        ]
        for selector in popup_selectors:
            if page.locator(selector).first.is_visible(timeout=500):
                print(f"👻 Popup killer active: Killing {selector}...")
                page.locator(selector).first.click(force=True)
                time.sleep(1)
    except:
        pass

def run_aol_bot():
    with sync_playwright() as p:
        print("🌐 Launching Browser in Headless mode for Cloud...")
        # 🛠️ CLOUD FIX: headless=True aur Linux server arguments
        browser = p.chromium.launch(
            headless=True, 
            slow_mo=200, 
            args=['--no-sandbox', '--disable-setuid-sandbox', '--ignore-certificate-errors', '--disable-dev-shm-usage']
        )
        
        if os.path.exists(STATE_FILE):
            print("🍪 Memory file found! Loading saved session...")
            context = browser.new_context(storage_state=STATE_FILE, ignore_https_errors=True)
        else:
            print("🆕 No memory found. Starting fresh session...")
            context = browser.new_context(ignore_https_errors=True)
            
        page = context.new_page()
        print("🚀 Going to AOL Mail...")
        page.goto("https://mail.aol.com/", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5) 
        
        # --- LOGIN CHECK ---
        try:
            if page.get_by_text("Log in", exact=True).first.is_visible(timeout=3000):
                page.get_by_text("Log in", exact=True).first.click()
                time.sleep(4)
            email_box = page.locator("input[name='username'], #login-username")
            if email_box.is_visible(timeout=3000):
                email_box.fill(EMAIL)
                email_box.press("Enter")
                page.locator("input[name='password'], #login-passwd").wait_for(timeout=10000)
                page.locator("input[name='password'], #login-passwd").fill(PASSWORD)
                page.locator("input[name='password'], #login-passwd").press("Enter")
                time.sleep(8)
                context.storage_state(path=STATE_FILE)
        except: pass

        processed_subjects = set()
        unread_url = "https://mail.aol.com/d/search/referrer=unread&keyword=is%253Aunread&accountIds=1&excludefolders=ARCHIVE"

        while True:
            print("\n" + "="*50)
            clear_popups(page)
            
            print("📂 Navigating directly to Unread Search URL...")
            try: page.keyboard.press("Escape")
            except: pass
                
            page.goto(unread_url, wait_until="domcontentloaded")
            time.sleep(8) 
            
            clear_popups(page)

            print("🔍 Checking for unread emails...")
            email_rows = page.locator('div[data-test-id="message-list"] div[role="article"], a[data-test-id="message-list-item"]')
            
            try:
                email_rows.first.wait_for(state="visible", timeout=6000)
            except:
                print("🎉 ALL CAUGHT UP! Waiting for new mails...")
                time.sleep(15) # Agar mail nahi hai, toh thoda ruk kar wapas check karega
                continue 

            # --- THE AD-BLOCKER LOGIC ---
            mail_clicked = False
            count = email_rows.count()
            
            for i in range(count):
                row = email_rows.nth(i)
                row_text = row.inner_text()
                
                if "Ad\n" in row_text[:10] or "Ad" in row_text[:5]:
                    continue
                
                print(f"🖱️ Real unread mail found! Opening...")
                row.click(force=True)
                mail_clicked = True
                break 
                
            if not mail_clicked:
                print("🎉 ALL CAUGHT UP! Only Ads left in the list.")
                time.sleep(15)
                continue

            time.sleep(6) 
            clear_popups(page)

            # --- SMART SCRAPING ---
            try:
                print("⏳ Reading email content...")
                page.locator('[data-test-id="message-group-subject-text"]').first.wait_for(state="visible", timeout=10000)
                
                subject = page.locator('[data-test-id="message-group-subject-text"]').first.inner_text()
                sender = page.locator('[data-test-id="message-from"]').first.inner_text()
                
                try:
                    body = page.locator('div[data-test-id="message-view-body"]').first.inner_text(timeout=3000)
                except:
                    body = "[No readable text found]"
                    
                print(f"✅ Extracted -> From: {sender} | Sub: {subject}")
            except Exception as e:
                print("🔄 Could not read mail, restarting cycle...")
                continue 

            if subject in processed_subjects:
                print("🛑 Already processed, skipping.")
                break
            processed_subjects.add(subject)

            if EMAIL.lower() in sender.lower() or sender.lower().strip() == "me":
                print("🛑 Self-mail, skipping reply.")
                continue 

            # --- GENERATE AI REPLY ---
            ai_reply_text = get_ai_reply(sender, subject, body)

            # --- REPLY FLOW ---
            print("⚙️ Typing and Sending AI Reply...")
            try:
                reply_btn = page.locator('text="Reply"').first
                reply_btn.wait_for(state="visible", timeout=5000)
                reply_btn.click(force=True)
                time.sleep(4) 
                
                message_box = page.locator('div[contenteditable="true"], div[role="textbox"]').first
                message_box.wait_for(state="visible", timeout=5000)
                
                message_box.fill(ai_reply_text)
                time.sleep(3) 
                
                send_btn = page.locator('text="Send"').first
                send_btn.click(force=True)
                print("✅ AI REPLY SENT SUCCESSFULLY!")
                time.sleep(6) 
            except Exception as e: 
                print(f"❌ Reply/Send Error: {e}")
            
            # --- DOUBLE SHIELD SYNC ---
            print("🛡️ Syncing state...")
            page.reload(wait_until="domcontentloaded")
            time.sleep(6)

if __name__ == "__main__":
    # 1. Start the Flask Dummy Server in a Background Thread
    server_thread = threading.Thread(target=run_flask)
    server_thread.daemon = True # Ye ensures karta hai ki script band hone par server bhi band ho jaye
    server_thread.start()
    
    # 2. Start the Main Bot Automation
    run_aol_bot()