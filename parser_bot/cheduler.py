import datetime
import subprocess

from apscheduler.schedulers.twisted import TwistedScheduler

i = 1


def scrap():
    global i
    print(f"Парсинг запустился {i}й раз в")
    i += 1
    print(datetime.datetime.now())
    subprocess.call('scrapy crawl problems', shell=True)


def run():
    # sched = AsyncIOScheduler()
    #
    # sched.add_job(scrap, 'interval', minutes=1)
    # sched.start()
    #
    # sched = BackgroundScheduler()
    #
    # sched.add_job(scrap, 'interval', minutes=1)
    # sched.start()

    sched = TwistedScheduler()

    sched.add_job(scrap, 'interval', minutes=1)
    sched.start()


