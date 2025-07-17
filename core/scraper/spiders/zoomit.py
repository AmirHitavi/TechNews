import scrapy


class ZoomitSpider(scrapy.Spider):
    name = "zoomit"
    allowed_domains = ["zoomit.ir"]
    start_urls = [
        "https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber=1"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True}, callback=self.parse)

    def parse(self, response):
        article_urls = response.css("a.fNLyDV::attr(href)").getall()

        for url in article_urls[::-1]:
            yield response.follow(
                url, meta={"playwright": True}, callback=self.parse_news_page
            )

        current_page = int(response.url.split("pageNumber=")[1])

        if current_page < 5:
            next_page = current_page + 1
            next_page_url = f"https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber={next_page}"

            yield response.follow(
                next_page_url, callback=self.parse, meta={"playwright": True}
            )

    def parse_news_page(self, response):

        content = ""

        stop_titles = [
            "تبلیغات",
            "مقاله‌های مرتبط",
            "مقاله‌ی مرتبط",
            "مطالعه ",
        ]

        content_divs = response.css("div.sc-481293f7-1.jrhnOU")
        for div in content_divs:
            paragraphs = div.css(".sc-9996cfc-0")
            for p in paragraphs:
                text_parts = p.css("::text").getall()
                clean_text = " ".join(t.strip() for t in text_parts if t.strip())

                if any(stop in clean_text for stop in stop_titles):
                    continue
                if (
                    "داغ‌ترین مطالب روز" in clean_text
                    or "مقالات جدید پیشنهادی" in clean_text
                ):
                    break

                if clean_text:
                    content += clean_text + "\n"

        tags = response.xpath(
            "/html/body/div/div[2]/div[1]/main/article/header/div/div/div[2]/div[1]"
        ).css("a")
        tags_list = [
            tag.css("span::text").get().strip()
            for tag in tags
            if tag.css("span::text").get()
        ]

        yield {
            "title": response.css("h1::text").get().strip(),
            "content": content.strip(),
            "source": response.url,
            "tags": tags_list,
        }
