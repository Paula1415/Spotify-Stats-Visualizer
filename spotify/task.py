from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from .authHandling import getuserdata

def my_listener(event):
    if event.exception:
        return False
    else:
        pass

def task(request):
    spotify = getuserdata()
    scheduler = BackgroundScheduler()
    scheduler.start()
    job = scheduler.add_job(lambda : spotify.userdata(request))
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)