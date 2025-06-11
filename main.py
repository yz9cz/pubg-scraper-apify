from apify import Actor
from playwright.sync_api import sync_playwright

def get_player_name(player_id: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.midasbuy.com/midasbuy/buy/pubgm", timeout=60000)
        page.wait_for_timeout(3000)

        try:
            if page.is_visible("xpath=/html/body/div[2]/div/div[14]/div[3]"):
                page.click("xpath=/html/body/div[2]/div/div[14]/div[3]")
        except:
            pass

        page.click("xpath=/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div")
        page.wait_for_timeout(2000)

        page.fill("xpath=/html/body/div[2]/div/div[5]/div[2]/div[1]/div[2]/div/div[2]/div/input", player_id)
        page.wait_for_timeout(2000)

        page.click("xpath=/html/body/div[2]/div/div[5]/div[2]/div[1]/div[3]/div/div")
        page.wait_for_timeout(5000)

        try:
            player_name = page.inner_text("xpath=/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/span[1]").strip()
            return player_name
        except:
            return None
        finally:
            browser.close()

async def main():
    async with Actor:
        input_data = await Actor.get_input() or {}
        player_id = input_data.get("player_id")

        if not player_id:
            await Actor.push_data({"error": "player_id is required"})
            return

        name = get_player_name(player_id)
        if name:
            await Actor.push_data({"player_id": player_id, "name": name})
        else:
            await Actor.push_data({"player_id": player_id, "error": "Name not found"})
