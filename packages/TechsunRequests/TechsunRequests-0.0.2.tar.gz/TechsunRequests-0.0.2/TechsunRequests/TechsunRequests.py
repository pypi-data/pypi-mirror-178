from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Requests:

    def __init__(self,show=False,save_response=False):
        self.show = show
        self.save_response = save_response
        self.s = Service(ChromeDriverManager().install())

    def Get(self,url):
        options = Options()
        if not self.show: options.add_argument('--headless')
        driver = webdriver.Chrome(service=self.s,options=options)
        driver.get(url)
        self.sourceHTML = driver.page_source
        if self.save_response:
            with open(f'raw.html', 'w', encoding='utf-8') as f: f.write(self.sourceHTML)
            print('[INFO] Response Saved')


if __name__ == '__main__':
    a = Requests(save_response=True,show=True)
    source = a.Get('https://www.youtube.com/results?search_query=video+editor+software+in+usa')
