import scrapy
from scrapy_splash import SplashRequest
from dotenv import load_dotenv
from os import environ as en

class OrderCibSpider(scrapy.Spider):
    load_dotenv()
    URL1 = en['URL1']
    name = 'order_cib'
    allowed_domains = [URL1]
    start_urls = [URL1]
    CIB_USERNAME = en['CIB_USERNAME']
    CIB_PASS = en['CIB_PASS']

    script = '''
        function main(splash,args)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(4))
            splash:set_viewport_full()
            local search_input = splash:select('input[name=txtUsr]')   
            search_input:send_text("{}")
            local search_input = splash:select('input[name=txtPas]')
            search_input:send_text("{}")
            assert(splash:wait(2))
            local submit_button = splash:select('#btnLogin')
            submit_button:click()
            assert(splash:wait(2))
            local last_ord_btn = splash:select('#ctl00_lnkRound7')
            last_ord_btn:click()
            assert(splash:wait(2))
            ord_tab = assert(splash:select_all(".hidFalse"))
            ord_tab[1]:mouse_click()
            assert(splash:wait(2))
            local button = splash:select(".button.send")
            button:mouse_click()
            assert(splash:wait(2))
            splash:set_viewport_full()
            return splash:html()
        end
    '''.format(CIB_USERNAME,CIB_PASS)

    def start_requests(self):
        yield SplashRequest(url=self.URL1,callback=self.parse,endpoint="execute", args={'lua_source':self.script})

    def parse(self, response):
        print(response.body)
