from escpos.printer import Usb
from datetime import date, datetime
import time
import requests
import random
import textwrap
import argparse

PROJECT_NAME = 'Your Project Name'
EMAIL = 'Your Email'
WEATHER_STATION = 'Your Weather.Gov Station'
WEATHER_X = 0  # Your weather.gov x
WEATHER_Y = 0  # Your weather.gov y
PLEX_EMAIL = 'Your Plex Login Email'
PLEX_PASSWORD = 'You Plex Login Password'


class Printer:

    def __init__(self):
        self.printer = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x03)

    def close(self):
        self.printer.close()

    def horizontal_line(self):
        self.printer.set(align='center')
        self.printer.textln('--------------------')
        self.printer.set()

    def print_title(self, text):
        self.printer.set(align='center', bold=True, double_width=True, double_height=True)
        self.printer.textln(text)
        self.horizontal_line()
        self.printer.set()

    def print_daily_header(self):
        self.print_title('Daily Digest')

        self.printer.set(align='center')
        today = date.today().strftime('%m/%d/%Y')
        self.printer.textln(today)

        self.printer.set()

    def print_weather(self):
        self.printer.set()

        header = {'User-Agent': PROJECT_NAME, 'From': EMAIL}
        url = 'https://api.weather.gov/gridpoints/{}/{},{}/forecast'.format(
            WEATHER_STATION,
            WEATHER_X,
            WEATHER_Y
        )

        success = False
        tries = 0
        r = None
        while not success:
            r = requests.get(url, headers=header)
            if 'properties' not in r.json():
                print('Weather Error')
                print(r.json())
                time.sleep(1)
                tries += 1
                if tries >= 10:
                    print('Max tries: {}'.format(tries))
                    return
            else:
                success = True

        today = r.json()['properties']['periods'][0]
        tonight = r.json()['properties']['periods'][1]

        with open('/home/pi/images/today.png', 'wb') as today_file:
            link = today['icon']
            link = link.replace('medium', '250')
            today_img = requests.get(link, headers=header)
            for chunk in today_img:
                today_file.write(chunk)

        with open('/home/pi/images/tonight.png', 'wb') as tonight_file:
            link = tonight['icon']
            link = link.replace('medium', '250')
            tonight_img = requests.get(link, headers=header)
            for chunk in tonight_img:
                tonight_file.write(chunk)

        self.printer.set(bold=True)
        self.printer.textln("{}'s Forecast:".format(today['name']))
        self.printer.set(align='center')
        self.printer.image('/home/pi/images/today.png')
        self.printer.set()
        today_forecast = textwrap.fill(today['detailedForecast'], 32)
        self.printer.textln(today_forecast)
        self.printer.textln()

        self.printer.set(align='left', bold=True)
        self.printer.textln("{}'s Forecast:".format(tonight['name']))
        self.printer.set(align='center')
        self.printer.image('/home/pi/images/tonight.png')
        self.printer.set()
        tonight_forecast = textwrap.fill(tonight['detailedForecast'], 32)
        self.printer.textln(tonight_forecast)

    def print_weather_hourly(self):
        header = {'User-Agent': PROJECT_NAME, 'From': EMAIL}
        url = 'https://api.weather.gov/gridpoints/{}/{},{}/forecast/hourly'.format(
            WEATHER_STATION,
            WEATHER_X,
            WEATHER_Y
        )

        success = False
        tries = 0
        r = None
        while not success:
            r = requests.get(url, headers=header)
            if 'properties' not in r.json():
                print('Weather Error')
                print(r.json())
                time.sleep(1)
                tries += 1
                if tries >= 10:
                    print('Max tries: {}'.format(tries))
                    return
            else:
                success = True

        weather = r.json()['properties']['periods']

        self.printer.set(align='center')
        today = date.today().strftime('%m/%d/%Y')
        self.printer.textln(today)
        self.printer.set()

        for i in range(12):
            hour = weather[i]
            h = datetime.strptime(hour['startTime'][:-6], '%Y-%m-%dT%H:%M:%S')
            temp = hour['temperature']
            forecast = hour['shortForecast']

            text = textwrap.fill('  {}°F & {}'.format(temp, forecast), 32)

            self.printer.set(bold=True)
            self.printer.textln(h.strftime('%I:%M %p:'))
            self.printer.set()
            self.printer.textln(text)

    def print_til(self):
        r = requests.get('https://www.reddit.com/r/todayilearned/.json',
                         headers={'User-Agent': PROJECT_NAME})
        post = r.json()['data']['children'][0]['data']
        fact = post['title']
        fact = textwrap.fill(fact, 32)
        url = post['url_overridden_by_dest']

        self.printer.set(align='center', underline=True)
        self.printer.textln('Today I Learned')

        self.printer.set()
        self.printer.textln(fact)

        self.printer.set(align='center')
        self.printer.qr(url, size=6)

        self.printer.set()

    def print_two_sentence_horror(self):
        r = requests.get('https://www.reddit.com/r/twosentencehorror/.json',
                         headers={'User-Agent': PROJECT_NAME})
        posts = r.json()['data']['children']

        story = ''
        author = ''
        for post in posts:
            if post['data']['distinguished']:
                continue
            story = post['data']['title']
            story += ' '
            story += post['data']['selftext']
            story = textwrap.fill(story, 32)

            author = post['data']['author']
            break

        self.printer.set()
        self.printer.textln(story)

        self.printer.set(align='right')
        self.printer.textln('By: ' + author)

        self.printer.set()

    def print_joke(self):
        r = requests.get('https://icanhazdadjoke.com',
                         headers={'User-Agent': PROJECT_NAME,
                                  'Accept': 'application/json'})
        joke = r.json()['joke']
        joke = textwrap.fill(joke, 32)

        self.printer.set()
        self.printer.textln(joke)

    def print_pixel_monster(self):
        import cairosvg

        monster_id = random.randint(1, 2147483647)

        r = requests.get('https://app.pixelencounter.com/api/basic/monsters/{}'.format(monster_id))

        svg = r.text
        svg = svg.replace('fill="#00000000"',
                          'fill="#FFFFFFFF"')
        cairosvg.svg2png(svg, write_to='/home/pi/images/monster.png',)

        self.printer.set(align='center')
        self.printer.image('/home/pi/images/monster.png')
        self.printer.textln()
        self.printer.set()
        self.printer.textln('Monster ID: {}'.format(monster_id))

    def print_jeopardy(self):
        r = requests.get('http://jservice.io/api/random')

        question = r.json()[0]['question']
        value = r.json()[0]['value']
        category = r.json()[0]['category']['title']
        answer = r.json()[0]['answer']
        air_date = r.json()[0]['airdate'][:10]
        air_date = datetime.strptime(air_date, '%Y-%m-%d')
        air_date = air_date.strftime('%b %-d, %Y')

        self.printer.set()
        self.printer.textln('Aired:')
        self.printer.textln('    ' + air_date)
        if category:
            self.printer.textln('Category:')
            self.printer.textln(textwrap.fill('    ' + category, 32))
        if value:
            self.printer.textln('Value:')
            self.printer.textln(textwrap.fill('    ' + str(value), 32))
        self.printer.textln('Question:')
        self.printer.textln(textwrap.fill('    ' + question, 32))
        self.printer.textln('Answer:')
        self.printer.textln(textwrap.fill('    ' + answer, 32))

    def print_random_plex(self):
        from plexapi.myplex import MyPlexAccount

        account = MyPlexAccount(PLEX_EMAIL, PLEX_PASSWORD)
        plex = account.resource('PLEXSERVER').connect()  # returns a PlexServer instance
        movies = plex.library.section('Movies')
        to_watch = random.sample(movies.search(unwatched=True), 1)[0]

        title = to_watch.title
        duration = round(to_watch.duration / 1000 / 60 / 60, ndigits=2)
        summary = to_watch.summary

        self.printer.set(align='center', bold=True)
        self.printer.textln(title)
        self.printer.set()
        self.printer.textln('Duration: {} hrs'.format(duration))
        self.printer.textln('Summary:')
        self.printer.textln(textwrap.fill('    ' + summary, 32))

    def print_cat(self):
        cats = [
            r"""|\---/|
| o_o |
 \_^_/""",

            r""" /\_/\
( o.o )
 > ^ <""",

            r"""    |\__/,|   (`\
  _.|o o  |_   ) )
-(((---(((--------""",

            r""" _._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-""",

            r""" /\_/\
( o o )
==_Y_==
  `-'""",

            r""" |\__/,|   (`\
 |_ _  |.--.) )
 ( T   )     /
(((^_(((/(((_/""",

            r"""  /\_/\  (
 ( ^.^ ) _)
   \"/  (
 ( | | )
(__d b__)""",

            r"""   |\__/,|   (`\
   |o o  |__ _)
 _.( T   )  `  /
((_ `^--' /_<  \
`` `-'(((/  (((/""",

            r""" .       .
 |\_---_/|
/   o_o   \
|    U    |
\  ._I_.  /
 `-_____-'""",

            r"""      /\_/\
 /\  / o o \
//\\ \~(*)~/
`  \/   ^ /
   | \|| ||
   \ '|| ||
    \)()-())""",

            r"""    /\_____/\
   /  o   o  \
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)""",

            r"""  ^___^
 " o o "
 ===X===       _
  ' " '_     __\\
 /''''  \___/ __/
|           /
("|")__\   |
"" ""(_____/""",

            r""" ,_     _
 |\\_,-~/
 / _  _ |    ,--.
(  @  @ )   / ,-'
 \  _T_/-._( (
 /         `. \
|         _  \ |
 \ \ ,  /      |
  || |-_\__   /
 ((_/`(____,-'""",

            r""" /\     /\
{  `---'  }
{  O   O  }
~~>  V  <~~
 \  \|/  /
  `-----'____
  /     \    \_
 {       }\  )_\_   _
 |  \_/  |/ /  \_\_/ )
  \__/  /(_/     \__/
    (__/""",

            r"""                        _
                       | \
                       | |
                       | |
  |\                   | |
 /, ~\                / /
X     `-.....-------./ /
 ~-. ~  ~              |
    \             /    |
     \  /_     ___\   /
     | /\ ~~~~~   \ |
     | | \        || |
     | |\ \       || )
    (_/ (_/      ((_/""",

            r"""         /\_/\
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)""",

            r"""      /|/|
     ( @ @)
      ) ^
     / |||
    / )|||_
   (_______)""",

            r"""                    _____
                   /  __  \
  / \ ----/ \     / /    \ \
 (           )    \/      \ \
   < >   < >              | |
 \     ^     /------------| |
   \  -^-  /        ____    |
  |   ---          /    \   |
  |                      |  |
   \--  \         /------|  /
    --------------_________/""",

            r"""         /\__/\
        /`    '\
      === 0  0 ===
        \  --  /
       /        \
      /          \
     |            |
      \  ||  ||  /
       \_oo__oo_/#######o""",

        ]

        self.printer.set()
        cat = random.sample(cats, 1)[0]

        cat = cat.split('\n')
        max_line = max([len(ln) for ln in cat])
        space = (32 - max_line) // 2

        cat = [(' ' * space) + ln for ln in cat]

        cat = '\n'.join(cat)

        self.printer.textln(cat)

    def print_inspiro(self):
        from PIL import Image

        r = requests.get('https://inspirobot.me/api?generate=true')

        im = Image.open(requests.get(r.text, stream=True).raw)

        width, height = im.size
        multiplier = 375 / width

        im = im.resize((int(width * multiplier), int(height * multiplier)))
        im.save('/home/pi/images/inspiro.jpg')

        self.printer.set(align='center')
        self.printer.image('/home/pi/images/inspiro.jpg')

    def print_on_this_day(self):
        today = datetime.today()

        link = 'https://en.wikipedia.org/api/rest_v1/feed/onthisday/selected/{:02}/{:02}'
        link = link.format(today.month, today.day)

        r = requests.get(link,
                         headers={'User-Agent': PROJECT_NAME})

        events = r.json()['selected']

        self.printer.set(align='center')
        today = date.today().strftime('%B %d')
        self.printer.textln(today)

        self.printer.set()
        for e in events:

            self.printer.textln('Year: {}'.format(e['year']))
            self.printer.textln(textwrap.fill(e['text'], 32))
            self.printer.textln()

    def print_daily(self):
        self.print_daily_header()
        self.horizontal_line()
        self.print_weather()
        self.horizontal_line()
        self.print_til()
        # self.horizontal_line()
        # self.print_two_sentence_horror()
        self.horizontal_line()
        self.print_joke()
        # self.horizontal_line()
        # self.print_pixel_monster()
        # self.horizontal_line()
        # self.print_jeopardy()


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Print fun things on thermal.')
    my_parser.add_argument('Kind',
                           metavar='kind',
                           type=str,
                           help='the kind of printout to print')

    args = my_parser.parse_args()
    kind = args.Kind.lower()

    p = Printer()

    if kind == 'daily':
        p.print_daily()
    elif kind == 'cat':
        p.print_title('Cat')
        p.print_cat()
    elif kind == 'movie':
        p.print_title('Movie Choice')
        p.print_random_plex()
    elif kind == 'inspiro':
        p.print_title('Inspiration')
        p.print_inspiro()
    elif kind == 'onthisday':
        p.print_title('On This Day')
        p.print_on_this_day()
    else:
        p.printer.textln('Unknown Kind')

    p.close()
