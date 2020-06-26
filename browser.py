import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init, Style


argv = 'python browser.py tb_tabs'
storage_dir = '.\\tb_tabs'
history = []
url = 'nytimes.com'


class MyBrowser():

    def check_cache_dir(self, storage_dir):
        if not os.path.exists(storage_dir):
            print("Can't find cache dir...")
            os.mkdir(os.path.join(os.curdir, storage_dir))
            print("Cache dir is created.")

    def print_from_cache(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                print(file.read())
        else:
            print("No path in cache!")

    def check_url(self, addr):
        if self.menu(addr):
            return
        if "." not in addr:
            #  если адрес без точки, проверяем на наличие к кэше
            file_path = f'{storage_dir}\\' + addr
            #  если есть в кэше, выводим кэш
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    print(file.read())
                history.append(addr)
            else:
                print("Wrong URL: error in address and there is no in cache!")
                return False
        else:
            history.append(addr)
            #            print(f"History is: {history}")
            return True

    def history_print(self):
        print(f"History is: {', '.join(history)}")

    def menu(self, addr):
        if addr == "exit":
            sys.exit()
            return True
        elif addr == "back":
            url = history.pop()
            self.print_from_cache(history.pop())
            return True
        elif addr == "history":
            self.history_print()
            return True

    def url_append(self, addr):
        if "http" not in addr:
            return "https://" + addr

    def url_request(self, addr, short_addr):
 #       try:
            url_list = short_addr.split(".")
            url_answer: str = str(requests.get(addr).content)
            url_soup = BeautifulSoup(url_answer, "html.parser")

            url_text = url_soup.prettify()
            #  ["p", "a", "ul", "ol", "li"]
            tags = url_soup.find_all(['title', "header", "p", "a", "ul", "ol", "li"])
            with open(f"{storage_dir}\\{short_addr}", "w") as file:
                file.writelines(url_text)
            for tag in tags:
                if tag.string is not None:
                    if tag.name == "a":
                        print(Fore.BLUE + tag.string + Style.RESET_ALL + '')
                    else:
                        print(tag.string)

            return
#        except:
#            print("Page or file is unreachable!")
 #           return


browser = MyBrowser()

while True:
    print(os.path.join(os.curdir, 'tb_tabs'))
    browser.check_cache_dir(storage_dir)
#    url: str = input()

    if browser.check_url(url):
        url_full = browser.url_append(url)
        browser.url_request(url_full, url)
#    break
