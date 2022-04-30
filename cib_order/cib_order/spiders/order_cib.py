import scrapy
from scrapy_splash import SplashRequest
import os



class OrderCibSpider(scrapy.Spider):
    URL1 = os.environ(['URL1'])
    name = 'order_cib'
    allowed_domains = [URL1]
    start_urls = ['http://{}/'.format(URL1)]
    CIB_USERNAME = os.environ(['CIB_USERNAME'])
    CIB_PASS = os.environ(['CIB_PASS'])

    script = '''
        function main(splash,args)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(4))
                splash:set_viewport_full()
                local search_input = splash:select('input[name=txtUsr]')   
                search_input:send_text("")
                local search_input = splash:select('input[name=txtPas]')
                search_input:send_text("")
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
                splash:set_viewport_full()
                local last_ord_btn = splash:select('.button send')
                last_ord_btn:click()
                assert(splash:wait(2))
            return {
                    html = splash:html(),
                    png = splash:png(),
            }
        end
    '''.format(CIB_USERNAME,CIB_PASS)

    def start_requests(self):
        return SplashRequest(url=self.URL1,callback=self.parse,endpoint="execute", args={'lua_source':self.script})

    def parse(self, response):
        print(response.body)
