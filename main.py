import logging
import os
import sqlite3
import time

from apscheduler.scheduler import Scheduler
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

s = Scheduler()

def run_sql(database, sql):
    try:
        conn = sqlite3.connect(database)
        #sql = 'CREATE TABLE ' + self.factor_name + ' AS ' + self.factor_data
        cursor = conn.execute(sql)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        logging.info('%s, commited', results)
    except Exception as ex:
        print(str(ex))
        logging.error('Error retreiveing data for Factor %s:  %s',  self.factor_name, str(ex))

def on_created(event):
    print(f"{event.src_path} has been created")
    if ("start" in event.src_path):
        s.start()
    else:
        if (".sql" in event.src_path):
            #get files in /queue/1, /queue/2, ..,/queue/n-1, /queue/n
            for subdir, dirs, files in os.walk('.'):
                for file in files:
                    print(os.path.join(subdir, file))
                    f = open(os.path.join(subdir, file), 'r')
                    contents = f.read()
                    print(contents)
                    s.add_cron_job(run_sql, args=['factors.db', contents])

def on_deleted(event):
    print(f"deleted {event.src_path}")

def on_modified(event):
    print(f"{event.src_path} has been modified")

def on_moved(event):
    print(f"{event.src_path} moved to {event.dest_path}")

if __name__ == "__main__":
    #set up watchdog file system watcher in the root directory
    patterns = "*.sql"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
