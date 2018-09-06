# -*- coding: utf-8 -*-
import datetime as dt
from dateparser import parse

from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    YEARS_XPATH = '//div[contains(@style, "float:left; width: 22%;")]/a/@href'
    GAZETTE_XPATH = '//div[contains(@style, "float:left; width: 20%; padding: 10px;")]'
    
    TERRITORY_ID = "3301702"
    name = "rj_duque_de_caxias"
    
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    start_urls = ["http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"]
    download_url = 'http://duquedecaxias.rj.gov.br/portal/{}'

    def parse(self, response):
        """
        @url http://duquedecaxias.rj.gov.br/
        @returns items 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """

        divs = response.xpath(self.GAZETTE_XPATH)

        while divs:
            date, url = divs[:2]

            date = date.re_first(r'\>(\d+.*\d+)')
            url = url.css('a::attr(href)').extract_first()

            del divs[:2]

            if date and url:
                yield Gazette(
                    date=parse(date, languages=["pt"]),
                    file_urls=[self.download_url.format(url)],
                    is_extra_edition=False,
                    territory_id=self.TERRITORY_ID,
                    power="executive_legislature",
                    scraped_at=dt.datetime.utcnow(),
                )
                
        url_years = response.xpath(self.YEARS_XPATH).extract()

        for url in url_years:
            yield Request(self.download_url.format(url))