from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from .authHandling import getuserdata

def my_listener(event):
    if event.exception:
        return False
    else:
        return event.JobExecutionEvent()

def task(token):
    spotify = getuserdata()
    scheduler = BackgroundScheduler()
    scheduler.start()
    job = scheduler.add_job(lambda: spotify.userdata(token))
    retval = scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    while True:
        if retval:
            return retval
            break
        else:
            pass

