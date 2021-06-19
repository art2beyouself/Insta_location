import webbrowser
import base64
from pathlib import Path
from folium import IFrame, folium, Popup, Marker, Icon
import os
import requests
from instascrape import Location
from auth import login, password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, random
import tkinter
from PIL import Image

master = tkinter.Tk()

class Remove_Button_Widget():
    def __init__(self, var1):
        variable_to_pass = var1
        self.Remove_Button = tkinter.Button(master, text="Удалить метку", height=2, width=12, command=lambda :remove_button().remove_functionality(variable_to_pass))
        self.Remove_Button.place(x=362,y=350)

def search_by_hashtag(hashtag):
    global browser
    browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")

    for i in range(1,4):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(random.randrange(2, 5))
    global photos
    hrefs = browser.find_elements_by_tag_name('a')
    photos = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
    global metki
    metki = []
    print("Собираю метки")
    item = []
    for url in photos:
        browser.get(url)
        element = browser.find_elements_by_class_name("JF9hh>a")
        if element:
            for hrefs in element:
                id = hrefs.get_attribute("href")
                metki.append(id)
                print(id)
            img_src = '/html/body/div[1]/section/main/div/div/article/div[2]/div/div/div[1]/img'
            img = browser.find_element_by_xpath(img_src).get_attribute('src')
            if img:
                item.append(img)
                get_img = requests.get(img)
                with open(f'{random.randrange(1, 10000)}_img.jpg', 'wb') as file:
                    file.write(get_img.content)
        else:
            print("Отсутствует метка у фотографии," + " ищу другие метки")
            continue
    if metki == []:
        print("По данному хештегу нет меток")
        exit()
    print("открываю Админку для премодерации")

    filelist = []
    for photos in os.listdir(os.curdir):
        if photos.endswith(".jpg"):
            filelist.append(photos)
            tatras = Image.open(f"{photos}")
            tatras.resize((400, 350), Image.ANTIALIAS)
            tatras.save(photos)

    master.title("Instagram Map")
    master.geometry("500x500")
    master.resizable(width=False, height=False)
    Robot_Files_Found_Widgets()
    master.mainloop()

    with open("savefile.txt", "r") as savefile:
        content = savefile.readlines()

    print("Метки собраны, наношу на карту фото ")
    map = folium.Map(location=[52.75816065, 54.6340587],
                     zoom_start=5,
                     tiles="https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYXJ0MmJleW91c2VsZiIsImEiOiJja3ByYmNoa2IwNHVvMnB0ODZuNHRjc25jIn0.ATQcPeBBgtf2Pz7yeznE3g",
                     attr='Парсер Инстаграм')
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
        "cookie": "sessionid=47964349465%3ALLEyhnjL6aS3Aq%3A22"
    }


    for position_url, photo_url in zip(content, filelist):
        encoded = base64.b64encode(open(f'{photo_url}', 'rb').read())
        html = '<img src="data:image/jpg;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=600, height=550)
        popup = Popup(iframe, max_width=1080)

        position = Location(position_url)
        position.scrape(headers=headers)
        Marker(
            location=[position.latitude, position.longitude],
            popup=popup,
            icon=Icon(color='green')).add_to(map)
# f'<a href="{photo_url}" target="_blank">{photo_url}</a>'
    map.save("map.html")
    print("Карта сохранена")
    for q in filelist:
        for fil in Path(os.curdir).glob(f"{q}"):
            fil.unlink()
    current = os.path.abspath(os.curdir)
    browser.get(current + '/map.html')
    time.sleep(999999)


class Robot_Files_Found_Widgets():
    def __init__(self):
        self.Robot_Files_Ran_Frame = tkinter.Frame(master)
        self.Robot_Files_Ran_Frame.place(bordermode = tkinter.INSIDE, height=30, width=200, y=250, x=35)
        self.Display_Robot_Files_Frame = tkinter.Frame(master, borderwidth=1, highlightthickness=1,
                                              highlightbackground="black", highlightcolor="black")
        self.Display_Robot_Files_Frame.place(bordermode = tkinter.INSIDE, height=200, width=300, y=285, x=50)
        self.ROBOT_FILE_LIST = tkinter.Listbox(self.Display_Robot_Files_Frame,selectmode = tkinter.MULTIPLE)
        self.ROBOT_FILE_LIST.place(bordermode = tkinter.INSIDE, height=196, width=296)

        self.Scroll_Bar_x = tkinter.Scrollbar(self.ROBOT_FILE_LIST, orient = tkinter.HORIZONTAL)
        self.Scroll_Bar_x.config(command=self.ROBOT_FILE_LIST.xview)
        self.Scroll_Bar_x.pack(fill = tkinter.X, side = tkinter.BOTTOM)
        self.ROBOT_FILE_LIST.config(xscrollcommand=self.Scroll_Bar_x.set)
        self.Scroll_Bar_y = tkinter.Scrollbar(self.ROBOT_FILE_LIST, orient = tkinter.VERTICAL)
        self.Scroll_Bar_y.config(command=self.ROBOT_FILE_LIST.yview)
        self.Scroll_Bar_y.pack(fill = tkinter.Y, side = tkinter.RIGHT)
        self.ROBOT_FILE_LIST.config(yscrollcommand=self.Scroll_Bar_y.set)
        some_list = []
        for x in metki:
            some_list.append(x)
        for y in some_list:
            self.ROBOT_FILE_LIST.insert(0, y)
        Remove_Button_Widget(self.ROBOT_FILE_LIST)
        Go_Button_Widget(self.ROBOT_FILE_LIST)
        View_Button_Widget(self.ROBOT_FILE_LIST)

class Go_Button_Widget():
    def __init__(self, var3):
        variableq = var3
        self.Go_Button = tkinter.Button(master, text="Посмотреть метку", height=2, width=14, command=lambda :view_button().view_functionality(variableq))
        self.Go_Button.place(x=362,y=300)


class View_Button_Widget():
    def __init__(self, var2):
        variable = var2
        self.Go_Button = tkinter.Button(master, text="Показать карту", height=2, width=12, command=lambda :go_button().go_functionality(variable))
        self.Go_Button.place(x=362,y=400)


class view_button():
    def view_functionality(self, ROBOT_FILE_LIST):
        for i in ROBOT_FILE_LIST.curselection():
            webbrowser.open(ROBOT_FILE_LIST.get(i))

class remove_button():
    def remove_functionality(self, ROBOT_FILE_LIST):
        sel = ROBOT_FILE_LIST.curselection()
        for index in reversed(sel):
            ROBOT_FILE_LIST.delete(index)


class go_button():
    def go_functionality(self, ROBOT_FILE_LIST):
        lb = ROBOT_FILE_LIST
        iscontain = list(lb.get(0, tkinter.END))
        with open("savefile.txt", "w") as savefile:
            for i in iscontain:
                savefile.write(f'{i}\n')
        master.destroy()

def login_firefox_chrome(_browser, login, password):
    global browser
    chrome = os.path.abspath(os.curdir)
    options = Options()
    options.binary_location = chrome + "\App\Chrome-bin\chrome.exe"
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-header")
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com')
    time.sleep(random.randrange(1, 2))

    _login = browser.find_element(By.NAME, "username")
    _login.clear()
    _login.send_keys(login)

    time.sleep(random.randrange(1, 2))

    _password = browser.find_element(By.NAME, "password")
    _password.clear()
    _password.send_keys(password)

    time.sleep(random.randrange(1, 2))

    _password.send_keys(Keys.ENTER)


def close_browser():
    global browser
    browser.close()
    browser.quit()
    login_firefox_chrome("Chrome", login, password)


login_firefox_chrome("Chrome", login, password)
time.sleep(5)
search_by_hashtag(input("Введите хештег для поиска (например: счастьедримвуд):   "))
time.sleep(200)
close_browser()
