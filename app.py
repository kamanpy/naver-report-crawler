from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/naver")
def crawl():

    page_num = request.args.get("page", "1")

    url = f"https://finance.naver.com/research/industry_list.naver?page={page_num}"

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url)

        page.wait_for_timeout(3000)

        rows = page.query_selector_all("table.type_1 tr")

        for row in rows:

            try:
                title_el = row.query_selector("td:nth-child(2) a")

                date_el = row.query_selector("td:nth-child(5)")

                if title_el and date_el:

                    title = title_el.inner_text().strip()

                    link = title_el.get_attribute("href")

                    date = date_el.inner_text().strip()

                    results.append({
                        "title": title,
                        "link": "https://finance.naver.com" + link,
                        "date": date
                    })

            except:
                pass

        browser.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
