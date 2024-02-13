import scrapy
import re
import redis
from rustore.items import FinderItem
from rustore.redis_settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_password
from urllib.parse import urljoin

BATCH_SIZE = 100


class ContactsSpider(scrapy.Spider):
    name = "contacts"
    social_media_domains = ['facebook.com',
                            'fb.com',
                            'twitter.com',
                            'instagram.com',
                            'youtube.com',
                            'linkedin.com',
                            'tiktok.com',
                            'xing.com',
                            'wa.me',
                            'api.whatsapp.com']


    def start_requests(self):
        redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_password)
        urls_batch = self.get_urls_batch(redis_conn)

        while urls_batch:
            for url in urls_batch:
                page_url = url.split('|URLH|')[1]
                key_url = url.split('|URLH|')[0]
                yield scrapy.Request(url=page_url,
                                     callback=self.parse,
                                     meta={'key_url': key_url})
            urls_batch = self.get_urls_batch(redis_conn)

    def get_urls_batch(self, redis_conn):
        urls_batch = []
        for _ in range(BATCH_SIZE):
            url = redis_conn.lpop('url')
            if url:
                urls_batch.append(url.decode('utf-8'))
            else:
                break
        return urls_batch


    def parse(self, response):

        # CMS
        cms_signatures = {
            'WordPress': ['/wp-content/', '/wp-includes/'],
            'Joomla': ['/components/', '/templates/'],
            'Drupal': ['/sites/default/', '/misc/drupal.js'],
            'Magento': ['/skin/frontend/'],
            'Shopify': ['cdn.shopify.com']
        }

        detected_cms = 'Unknown'

        for cms, paths in cms_signatures.items():
            for path in paths:
                if response.xpath(f"//*[contains(@src, '{path}') or contains(@href, '{path}')]").get():
                    detected_cms = cms
                    break
            if detected_cms != 'Unknown':
                break
        if detected_cms == 'Unknown':
            detected_cms = ''

        social_links = [link for link in links if any(domain in link for domain in self.social_media_domains)]
        social_links = ', '.join(social_links)

        # EMAIL
        email_pattern = r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\.[A-Z|a-z]{2,9}\b'
        matches_standard = re.findall(email_pattern, response.text)
        emails = [match for match in matches_standard if not re.match(r'.*(\.png|\.jpg|\.jpeg|\.heic|\.webp|\.gif'
                                                                      r'|\.PNG|\.JPG|\.JPEG|\.HEIC|\.WEBP|\.GIF)$',
                                                                      match)]
        unique_mails = []
        for item in emails:
            if (item.lower() not in unique_mails) \
                    and ('@sentry' not in item.lower()) \
                    and ('ingest.sentry.io' not in item.lower()) \
                    and ('@domain.com' not in item.lower()) \
                    and ('@example.com' not in item.lower()) \
                    and ('@email.here' not in item.lower()) \
                    and ('support@jouwweb.nl' not in item.lower()) \
                    and ('@email.com' not in item.lower()):
                unique_mails.append(item.lower().replace(' ', ''))
        first_email = ''
        if unique_mails:
            first_email = unique_mails[0]
        else:
            unique_mails = ''

        req_url = response.meta.get('req_url', False)
        if not req_url:
            req_url = response.request.url

        if first_email:
            item = FinderItem()
            item['req_url'] = req_url
            item['res_url'] = response.url
            item['status'] = response.status
            item['first_email'] = first_email
            item['emails'] = unique_mails
            item['detected_cms'] = detected_cms
            item['social_links'] = social_links
            yield item

        else:
            contact_links = response.xpath('//a[contains(@href, "contact")]/@href').getall()
            contact_links_text = response.xpath(
                "//a[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONTACT')]/@href").getall()
            unique_contact_links = []
            for item in contact_links:
                if item.lower() not in unique_contact_links:
                    unique_contact_links.append(item.lower())
            for item in contact_links_text:
                if item.lower() not in unique_contact_links:
                    unique_contact_links.append(item.lower())
            if unique_contact_links and (not response.meta.get('req_url', False)):
                for first_contact_link in unique_contact_links:
                    if not first_contact_link.startswith(("http://", "https://")):
                        first_contact_link = urljoin(response.url, first_contact_link)
                    yield response.follow(first_contact_link, callback=self.parse,
                                          meta={"pyppeteer": True,
                                                'req_url': req_url}
                                          )
            else:
                item = FinderItem()
                item['req_url'] = req_url
                item['res_url'] = response.url
                item['status'] = response.status
                item['first_email'] = ''
                item['emails'] = ''
                item['detected_cms'] = detected_cms
                item['social_links'] = social_links
                yield item