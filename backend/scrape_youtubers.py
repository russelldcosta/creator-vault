from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


DRIVER_PATH = r"C:\Users\russe\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"
TAG_PAGE = "https://itch.io/games/tag-horror"
EMAIL_QUOTA = 1


def human_sleep(min_s=1.0, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))


def browser():
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(service=Service(DRIVER_PATH), options=opts)


def extract_email(driver, iframe, seen):
    try:
        # Visit the video page
        vid = iframe.get_attribute("src").split("/embed/")[-1].split("?")[0]
        driver.get(f"https://www.youtube.com/watch?v={vid}")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.TAG_NAME, "ytd-video-primary-info-renderer")
        ))

        # Go to the channel's /about page
        channel_url = driver.find_element(
            By.XPATH, "//ytd-video-owner-renderer//a"
        ).get_attribute("href")
        if channel_url in seen:
            return None
        seen.add(channel_url)
        driver.get(channel_url.rstrip("/") + "/about")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, "additional-info-container")
        ))

        # Scroll to the 'More info' section
        more_info = driver.find_element(By.ID, "additional-info-container")
        driver.execute_script("arguments[0].scrollIntoView(true);", more_info)
        human_sleep(1.5, 2.5)

        # Click "View email address"
        view_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#view-email-button-container button")
        ))
        view_btn.click()
        human_sleep(2, 3)

        # Switch to reCAPTCHA iframe and tick the box
        anchor_iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src,'api2/anchor')]")
        ))
        driver.switch_to.frame(anchor_iframe)
        tick = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.ID, "recaptcha-anchor")
        ))
        tick.click()
        human_sleep(3, 4.5)
        driver.switch_to.default_content()

        # Wait for and click the Submit button
        submit_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "submit-btn")
        ))
        human_sleep(1.2, 2.2)
        submit_btn.click()

        # Get the email element
        email_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "email")
        ))
        return email_el.text.strip()

    except Exception as e:
        print("❌ Failed to extract email:", e)
        return None


def main():
    driver = browser()
    wait = WebDriverWait(driver, 10)
    seen = set()
    emails = []

    try:
        # Manual sign in
        driver.get("https://www.youtube.com/")
        input("🔐 Sign in to YouTube in the opened window, then type 'continue' & press Enter → ")

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
            human_sleep()

            iframes = driver.find_elements(By.XPATH, "//iframe[contains(@src,'youtube.com/embed')]")
            for frame in iframes:
                if len(emails) >= EMAIL_QUOTA:
                    break
                email = extract_email(driver, frame, seen)
                if email:
                    print("✅ Collected:", email)
                    emails.append(email)
                else:
                    print("– No email, skipping…")

        print(f"\n🎉 Done: Collected {len(emails)} emails →", emails)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
