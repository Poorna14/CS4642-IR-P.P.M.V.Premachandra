import scrapy
import json
from w3lib.html import remove_tags

class PostesSpider(scrapy.Spider):
    name = "posts"
    
    def start_requests(self):
        url='https://www.ebay.com/sch/i.html?_from=R40&_nkw=phones&_sacat=0&LH_TitleDesc=0&_pgn='
        search_urls = []
        for x in range(1,2):
            search_urls.append(url+str(x))
        
        for url in search_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        for post in response.css('li.s-item'):
            title=str(remove_tags(post.css('h3.s-item__title').extract_first()))
            if('.' in title):
                title=title.replace('.',',')
            if(':' in title):
                title=title.replace(':',';')    
            if('/' in title):
                title=title.replace('/','_')
            if('"' in title):
                title=title.replace('"', '^')
            if('*' in title):
                title=title.replace('*', ' ')   
            with open('Output/'+title+'.json','w')as file:
                data={'title':remove_tags(post.css('h3.s-item__title').extract_first()),
                      'image':post.css('img.s-item__image-img::attr(src)').extract_first(),
                      'subtitle': post.css('div.s-item__subtitle::text').extract_first(),
                      'condition':post.css('span.SECONDARY_INFO::text').extract_first(),
                      'price':post.css('span.s-item__price::text').extract_first(),
                      'quantity_sold':post.css('span.NEGATIVE::text').extract_first(),
                      'seller_quality':post.css('span.s-item__etrs-text::text').extract_first(),
                      'seller_country':post.css('span.s-item__location::text').extract_first(),
                      }
                json.dump(data,file)


        
