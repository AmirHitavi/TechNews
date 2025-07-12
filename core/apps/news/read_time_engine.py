import re
from math import ceil


class NewsReadTimeEngine:
    WORDS_PER_MINUTE = 250
    SECONDS_PER_TAG = 5

    @staticmethod
    def word_count(text):
        words = re.findall(r"\w+", text)
        return len(words)

    @staticmethod
    def estimate(news):
        words_count_title = NewsReadTimeEngine.word_count(news.title)
        words_count_content = NewsReadTimeEngine.word_count(news.text)

        total_time = (
            words_count_title + words_count_content
        ) / NewsReadTimeEngine.WORDS_PER_MINUTE

        tags_count = news.tags.count()

        total_time += (tags_count * NewsReadTimeEngine.SECONDS_PER_TAG) // 60

        return ceil(total_time)
