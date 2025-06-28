import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ─── Configuration ────────────────────────────────────────────────────────────
DRIVER_PATH = r"C:\Users\russe\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"
TAG_PAGE    = "https://itch.io/games/tag-horror"
EMAIL_QUOTA = 1

# ─── Launch Chrome ─────────────────────────────────────────────────────────────
def browser():
    opts = webdriver.ChromeOptions()
    # Remove automation banners (optional)
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(service=Service(DRIVER_PATH), options=opts)

# ─── Extract email from one YouTube embed ─────────────────────────────────────
def extract_email(driver, iframe, seen):
    try:
        vid = iframe.get_attribute("src").split("/embed/")[-1].split("?")[0]
        driver.get(f"https://www.youtube.com/watch?v={vid}")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-video-primary-info-renderer")))

        channel_url = driver.find_element(By.XPATH, "//ytd-video-owner-renderer//a").get_attribute("href")
        if channel_url in seen:
            return None
        seen.add(channel_url)

        driver.get(channel_url.rstrip("/") + "/about")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-channel-about-metadata-renderer")))

        try:
            driver.find_element(By.XPATH, "//yt-formatted-string[text()='View Email Address']").click()
            time.sleep(1)
        except:
            return None

        try:
            driver.find_element(By.XPATH, "//iframe[contains(@src,'recaptcha')]")
            input("🔐 Solve CAPTCHA in browser, then type 'continue' and press Enter → ")
        except:
            pass

        return driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']").text.strip()

    except Exception:
        return None

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    driver = browser()
    wait = WebDriverWait(driver, 10)
    seen = set()
    emails = []

    try:
        # 1) Open YouTube for manual login
        driver.get("https://www.youtube.com/")
        input("🔐 Please sign in to YouTube in the opened window, then type 'continue' and press Enter → ")

        # 2) Start scraping after login
        driver.get(TAG_PAGE)
        games = [a.get_attribute("href") for a in wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".game_cell a.thumb_link"))
        )][:10]

        for game_url in games:
            if len(emails) >= EMAIL_QUOTA:
                break
            driver.get(game_url)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)

            iframes = driver.find_elements(By.XPATH, "//iframe[contains(@src,'youtube.com/embed')]")
            for iframe in iframes:
                if len(emails) >= EMAIL_QUOTA:
                    break
                email = extract_email(driver, iframe, seen)
                if email:
                    print("✅ Collected:", email)
                    emails.append(email)
                else:
                    print("– No email on this channel, moving on…")

        print(f"\n🎉 Done: Collected {len(emails)} emails →", emails)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
