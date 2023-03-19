import scrapy

from parser_bot.items import ProblemItem


class ProblemSpider(scrapy.Spider):
    name = "problems"
    start_urls = ['https://codeforces.com/problemset?order=BY_SOLVED_DESC']

    def parse(self, response, **kwargs):
        # Извлечение всех ссылок на задачи со страницы
        links = response.xpath("//table[@class='problems']/./tr/td[@class='id']/a/@href").extract()
        base_url = "https://codeforces.com"

        # Извлечение параметров задач
        for link in links:
            solves = response.xpath(f"//a[@href='{link}']/../.."
                                    f"//a[@title='Количество решивших задачу']/text()").get()
            rating = response.xpath(f"//a[@href='{link}']/../..//span[@class='ProblemRating']/text()").get()

            p_item = ProblemItem()
            p_item['problem_name'] = response.xpath(f"//a[@href='{link}']/../.././td/div/a/text()").get().strip()
            p_item['problem_number'] = response.xpath(f"//a[@href='{link}']/text()").get().strip()
            p_item['solves'] = int(solves.strip()[1:]) if solves else None
            p_item['themes'] = response.xpath(f"//a[@href='{link}']/../.." +
                                              "//a[@class='notice']/text()").extract()
            p_item['rating'] = rating
            p_item['problem_link'] = base_url + link

            yield p_item

        # Получение последней страницы и итерация по ним
        last_page = max([int(p) for p in response.xpath("//span[@class='page-index']/a/text()").extract()])
        for page in range(2, last_page):
            url = f"https://codeforces.com/problemset/page/{page}?order=BY_SOLVED_DESC"
            yield response.follow(url, callback=self.parse)
