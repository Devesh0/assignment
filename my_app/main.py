import get_data


class AllocateServer:
    """Class to allocate the servers efficiently to 
        the request as per the assigned company."""

    def __init__(self):
        self.company_list = get_data.get_company_list()
        self.server_list = get_data.get_server_list()
        self.server_threshold = get_data.get_server_threshold()

        self.retry_queue = []

    def retry_failed_servers(self):
        """Function to retry the server allocation
        to the request failed in first chance. """
        try:
            self.allocate_server(self.retry_queue)
        except Exception as e:
            print(e)
        if len(self.retry_queue) > 1:
            print(self.retry_queue, "Error cannot place call...")
            self.retry_queue.clear()

    def allocate_server(self, *args):
        """Function to allocate servers efficiently according 
            to their threshold."""
        allocated_server_list = []
        for value in self.company_list:
            SERVER_LIST = self.server_list[value[0]]
            min_val = max(self.server_threshold,key=lambda k: self.server_threshold[k])
            try:
                if min_val not in SERVER_LIST and (len(SERVER_LIST) == 1):
                    min_val = SERVER_LIST[0]
                    allocated_server_list.append((value[1], min_val))
                    self.server_threshold[min_val] -= 1
                elif min_val in SERVER_LIST:
                    allocated_server_list.append((value[1], min_val))
                    self.server_threshold[min_val] -= 1
                else:
                    self.retry_queue.append(value)
                    continue
            except Exception as e:
                print(e)
        self.company_list.clear()
        return allocated_server_list
