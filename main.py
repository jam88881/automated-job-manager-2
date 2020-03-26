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
        cursor = conn.execute(sql)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        logging.info('%s, commited', sql)
    except Exception as ex:
        print(str(ex))
        logging.error(str(ex))

def on_created(event):
    try:
        time.sleep(1)
        print(f"{event.src_path} has been created")
        if (".sql" in event.src_path):
            with open(event.src_path, 'r') as f:
                contents = f.read()
                print(contents)
                run_sql('factors.db', contents)
    except Exception as ex:
        logging.error(str(ex))

def on_deleted(event):
    print(f"deleted {event.src_path}")

def on_modified(event):
    print(f"modified {event.src_path}")

def on_moved(event):
    print(f"{event.src_path} moved to {event.dest_path}")

def process_queue():
    print('walking through process queue')
    for subdir, dirs, files in os.walk('queue'):
        for file in files:
            print(os.path.join(subdir, file))
            with open(os.path.join(subdir, file), 'r') as f:
                contents = f.read()
                print(contents)
                run_sql('factors.db',contents)

if __name__ == "__main__":
    #TODO set up a config
    try:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s', 
            level='INFO',
            handlers=[logging.FileHandler("app.log"),logging.StreamHandler()])
        logging.info('Initaling AP scheduler to process...')
        
        #check queue directory on a set schedule
        s.add_cron_job(process_queue, day_of_week='mon-fri', hour=13, minute=12)
        s.start()

        #set up watchdog file system watcher in the root directory
        patterns = ["*.sql"] 
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        event_handler.on_created = on_created
        event_handler.on_deleted = on_deleted
        event_handler.on_modified = on_modified
        event_handler.on_moved = on_moved
        path = ".\immediate"
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        print("starting observer")
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            s.shutdown()
    except Exception as ex:
        print(str(ex))
        os.system('pause')