from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import undetected_chromedriver as uc
import time
import random
from main import save_youtuber

import whisper
import requests
import os

# Load Whisper model once
model = whisper.load_model("base")

TAG_PAGE    = "https://itch.io/games/tag-horror"
EMAIL_QUOTA = 1


def human_sleep(min_s=1.0, max_s=2.5):
    time.sleep(random.uniform(min_s, max_s))


def human_move(driver, element):
    """Tiny random mouse movements before interacting."""
    try:
        size = element.size
        actions = ActionChains(driver)
        for _ in range(random.randint(2, 4)):
            x = random.randint(1, size['width'] - 1)
            y = random.randint(1, size['height'] - 1)
            actions.move_by_offset(x, y).pause(random.uniform(0.1, 0.3))
        actions.move_to_element(element).perform()
    except:
        pass


def solve_audio_captcha(driver):
    """First click checkbox, then optionally solve audio challenge, or detect simple tick success."""
    try:
        driver.switch_to.default_content()

        # 1) Tick the “I’m not a robot” checkbox
        cb_iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src,'api2/anchor')]")
        ))
        driver.switch_to.frame(cb_iframe)
        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "recaptcha-anchor")
        ))
        human_move(driver, checkbox)
        checkbox.click()
        human_sleep(2, 3)
        # Check if simple tick solved
        checked = checkbox.get_attribute("aria-checked")
        driver.switch_to.default_content()
        if checked == 'true':
            # solved with single click
            return True

        # 2) Switch into the challenge iframe
        ch_iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src,'api2/bframe')]")
        ))
        driver.switch_to.frame(ch_iframe)

        # 3) Click audio challenge button
        audio_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.ID, "recaptcha-audio-button")
        ))
        human_move(driver, audio_btn)
        audio_btn.click()
        human_sleep(2, 3)

        # 4) Download and transcribe audio
        audio_src = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "audio-source")
        )).get_attribute("src")
        with open(".temp.mp3", "wb") as f:
            f.write(requests.get(audio_src).content)
        result = model.transcribe(".temp.mp3")
        answer = result["text"].strip()

        # 5) Submit the answer
        input_box = driver.find_element(By.ID, "audio-response")
        input_box.send_keys(answer)
        human_sleep(1, 2)
        driver.find_element(By.ID, "recaptcha-verify-button").click()
        human_sleep(3, 5)

        driver.switch_to.default_content()
        try:
            os.remove(".temp.mp3")
        except:
            pass

        return True

    except Exception as e:
        print("⚠️ CAPTCHA solve failed:", e)
        driver.switch_to.default_content()
        return False


def browser():
    opts = uc.ChromeOptions()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--start-maximized")
    return uc.Chrome(options=opts)


def extract_channel_info(driver, iframe, seen):
    try:
        # 1) Open video page
        vid = iframe.get_attribute("src").split("/embed/")[-1].split("?")[0]
        driver.get(f"https://www.youtube.com/watch?v={vid}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.TAG_NAME, "ytd-video-primary-info-renderer")
        ))
        human_sleep(1.5, 2.5)

        # 2) Grab channel URL & name
        channel_el  = driver.find_element(By.XPATH, "//ytd-video-owner-renderer//a")
        channel_url = channel_el.get_attribute("href")
        if channel_url in seen:
            return None
        seen.add(channel_url)
        channel_name = channel_el.text.strip()

        # 3) Go straight to About to get email
        driver.get(f"{channel_url.rstrip('/')}/about")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "additional-info-container")
        ))
        human_sleep(1.5, 2.5)

        # 4) Scroll & click View Email
        more_info = driver.find_element(By.ID, "additional-info-container")
        driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth'});", more_info)
        human_sleep(1.5, 2.5)
        view_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#view-email-button-container button")
        ))
        human_move(driver, view_btn)
        view_btn.click()
        human_sleep(2, 3)

        # 5) Solve the reCAPTCHA
        if not solve_audio_captcha(driver):
            print("– Skipping due to captcha.")
            return None

        # 6) Click submit after captcha
        try:
            submit_btn = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID, "submit-btn"))
            )
            human_sleep(2, 3)
            human_move(driver, submit_btn)
            submit_btn.click()
            print("✅ Submit button clicked.")
            human_sleep(2, 3)
        except Exception as e:
            print("⚠️ Failed to click submit:", e)
            return None

        # 7) Wait and extract the email
        try:
            email_el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_href = email_el.get_attribute("href")
            email = email_href.replace("mailto:", "").strip() if email_href else email_el.text.strip()
            print("got email", email)
        except Exception as e:
            print("⚠️ Failed to find email element:", e)
            return None

        # 8) Finally, get subscriber count
        driver.get(channel_url)
        sub_el = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "subscriber-count")
        ))
        subs = sub_el.text.replace(" subscribers", "").replace(",", "")
        try:
            if "K" in subs:
                subs = int(float(subs.replace("K","")) * 1_000)
            elif "M" in subs:
                subs = int(float(subs.replace("M","")) * 1_000_000)
            else:
                subs = int(subs)
        except:
            subs = None

        return {
            "username":    channel_name,
            "link":        channel_url,
            "email":       email,
            "subscribers": subs,
            "genre":       "horror",
        }

    except Exception as e:
        print("❌ extract_channel_info error:", e)
        return None


def main():
    driver = browser()
    wait   = WebDriverWait(driver, 10)
    seen   = set()
    emails = []

    try:
        # 1) Manual login
        driver.get("https://www.youtube.com/")
        input("🔐 Sign in & then type 'continue' → ")

        # 2) Scrape each embedded video
        driver.get(TAG_PAGE)
        games = [a.get_attribute("href") for a in wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".game_cell a.thumb_link"))
        )][:10]

        for game in games:
            if len(emails) >= EMAIL_QUOTA:
                break
            driver.get(game)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            human_sleep(1, 2)

            frames = driver.find_elements(By.XPATH, "//iframe[contains(@src,'youtube.com/embed')]")
            for f in frames:
                if len(emails) >= EMAIL_QUOTA:
                    break
                info = extract_channel_info(driver, f, seen)
                if info:
                    print("✅ Collected:", info)
                    emails.append(info["email"])
                    save_youtuber(**info)
                else:
                    print("– No data, next…")
                human_sleep(1, 2)

        print(f"\n🎉 Done: {len(emails)} emails →", emails)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
