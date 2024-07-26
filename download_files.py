import os
import scrapy
from urllib.parse import urlparse

class DownloadFilesSpider(scrapy.Spider):
    name = 'download_files'
    
    def __init__(self, base_url, *args, **kwargs):
        super(DownloadFilesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [base_url]
        self.base_url = base_url
        self.allowed_domains = [urlparse(base_url).netloc]

    def parse(self, response):
        self.logger.info(f'Parsing {response.url}')
        
        file_extensions = ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.php', '.json', '.xml', '.txt', '.pdf']
        if any(response.url.endswith(ext) for ext in file_extensions):
            self.save_file(response)
        
        for href in response.css('a::attr(href)').extract():
            full_url = response.urljoin(href)
            if self.is_valid_url(full_url):
                yield scrapy.Request(full_url, callback=self.parse)

    def is_valid_url(self, url):
        return any(url.endswith(ext) for ext in ['/', '.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.php', '.json', '.xml', '.txt', '.pdf'])

    def save_file(self, response):
        url_path = urlparse(response.url).path
        file_path = os.path.join('downloaded_website', url_path[1:])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(response.body)
        
        self.logger.info(f'Saved file {file_path}')
