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
        logging.error('Error retreiveing data for Factor %s:  %s',  self.factor_name, str(ex))

def on_created(event):
    print(f"{event.src_path} has been created")
        if (".sql" in event.src_path):
            with open(event.src_path, 'r') as file:
                contents = f.read()
                print(contents)
                run_sql('factors.db', contents)

def on_deleted(event):
    print(f"deleted {event.src_path}")

def on_modified(event):
    print(f"modified {event.src_path}")

def on_moved(event):
    print(f"{event.src_path} moved to {event.dest_path}")

def process_queue():
    for subdir, dirs, files in os.walk('queue'):
        for file in files:
            print(os.path.join(subdir, file))
            with open(os.path.join(subdir, file), 'r') as file:
                contents = f.read()
                print(contents)
                run_sql('factors.db',contents)

if __name__ == "__main__":
    #TODO set up a config
    #check queue directory on start
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level='INFO')
    logging.info('Initaling AP scheduler to process...')

    s.add_cron_job(process_queue, day_of_week='mon-fri', hour=9, minute=47)
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
    go_recursively = True
    observer = Observer()
    observer.schedule(event_handler, path, recursive=go_recursively)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        s.shutdown()
    