from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import AI

def my_task():
    AI.tiktokrerun()
    AI.twitterrerun()
    # Code exécuté chaque jour
    print("les modeles sont re entrainer chaque jour à {}".format(datetime.datetime.now()))

scheduler = BlockingScheduler()
scheduler.add_job(my_task, 'cron', hour=8)
print('start task')
scheduler.start()