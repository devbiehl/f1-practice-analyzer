import os
from driver import Driver
from logging_config import setup_logger
from f1db import connect_db, create_table, insert_session_summary
logger = setup_logger()

class DBHandler:
    def __init__(self, drivers, track_name, session_name, year, session_key):
        self.drivers = drivers
        self.track_name = track_name
        self.session_name = session_name
        self.year = year
        self.session_key = session_key

    def save_to_db(self):
        if not self.session_key:
            logger.warning("No session_key found - skipping database insert.")
            return
        
        logger.info("Saving session summary to database")
        
        conn = connect_db()

        create_table(conn)

        # BUild driver results for database
        driver_results = []
        for driver in self.drivers.values():
            driver.prepare_summary()
            driver_results.append(driver)

        logger.debug(f"Number of drivers to save: {len(driver_results)}")
        insert_session_summary(conn, self.track_name, self.year, self.session_name, self.session_key, driver_results)
        conn.commit()
        conn.close()