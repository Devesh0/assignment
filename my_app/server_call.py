import time
from main import AllocateServer
from db_queries import db_cursor, my_db


class UpdateServer:
    def __init__(self):
        self.retry_servers = AllocateServer().retry_failed_servers()
        self.servers_allocated = AllocateServer().allocate_server()
        self.to_update_queue = []

    def update_call_status(self):
        """Function to upfate the call status and
           call count once the server is allocated."""
        for values in self.servers_allocated:
            self.to_update_queue.append(values[1])
            try:
                sql = "	UPDATE requests, servers \
			SET requests.call_status=0 ,servers.call_running = servers.call_running+1 \
			WHERE requests.client_number='%s' AND servers.server_name=%s "

                db_cursor.execute(sql, (values[0], values[1]))
                print("Database updated...")
            except Exception as e:
                print(e)
                my_db.rollback()
        my_db.commit()
        self.servers_allocated.clear()

    def update_after_minute(self):
    	"""Function to decrease server call count after one minute."""
    	while self.to_update_queue:
    		for values in self.to_update_queue:
	    		time.sleep(5)
	    		try:
	    			sql = "UPDATE servers SET servers.call_running = servers.call_running-1 \
	    				   WHERE servers.server_name=%s "
	    			db_cursor.execute(sql, (values,))
	    			my_db.commit()
	    			self.to_update_queue.remove(values)
	    			print("Value to :" + str(values) + " changed successfully...")
	    		except Exception as e:
	    			print(e)
	    			my_db.rollback()

if __name__ == '__main__':
    update_server = UpdateServer()
    update_server.update_call_status()
    update_server.update_after_minute()
