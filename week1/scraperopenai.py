import os
import time
from playwright.sync_api import sync_playwright

def scrape_openai_news():
    with sync_playwright() as p:
        user_data_dir = os.path.join(os.getcwd(), "playwright_data")
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser_context.pages[0] # Note: use [0] for persistent context
        
        try:
            print("Navigating to OpenAI News...")
            page.goto("https://openai.com", wait_until="networkidle")
            
            # Wait for the main content area to appear
            # Using a generic 'section' or 'main' often works better than specific tags
            page.wait_for_selector("main", timeout=10000)
            
            # SCROLL DOWN: This triggers "Lazy Loading" of images and text
            page.mouse.wheel(0, 1000)
            time.sleep(2)

            # BETTER SELECTOR: OpenAI currently uses 'h3' inside 'li' tags for news items
            # We will grab all text from elements that look like headlines
            items = page.locator("h3").all()
            
            print(f"\n✅ Found {len(items)} headlines:")
            for i, item in enumerate(items):
                title = item.inner_text().strip()
                if title:
                    print(f"{i+1}. {title}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            page.screenshot(path="debug.png")
        
        finally:
            browser_context.close()

if __name__ == "__main__":
    scrape_openai_news()
