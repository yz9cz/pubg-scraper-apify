# PUBG Player Name Scraper API

API لاستخراج اسم لاعب PUBG من موقع Midasbuy باستخدام Web Scraping مع Selenium.

## Endpoint

### `GET /get_name?player_id=5443564406`

- `player_id`: معرف لاعب PUBG (9-10 أرقام).
- **الاستجابة:**

```json
{
  "player_id": "5443564406",
  "name": "اسم اللاعب"
}
