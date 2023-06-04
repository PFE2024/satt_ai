from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import tiktok_model
import twitter_model

def run_task():
    tiktok_model.tiktokrerun()
    twitter_model.twitterrerun()
    # Code exécuté chaque jour
    print("les modeles sont re entrainer chaque jour à {}".format(datetime.datetime.now()))

scheduler = BlockingScheduler()
scheduler.add_job(run_task, 'cron', hour=8)
print('start task')
scheduler.start()