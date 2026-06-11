import time


class Throttler:
    def __init__(self, max_calls = 15, per_secs = 61):
        self.MAX_CALLS = max_calls
        self.PER_SECS = per_secs
        self.api_call_times = []

    def time_elapsed(self, query_time):
        return time.time() - query_time >= self.PER_SECS

    def pop_time(self):
        oldest_call = self.api_call_times[0]
        self.api_call_times = self.api_call_times[1:]
        return oldest_call
    
    def get_num_recent_calls(self):
        return len(self.api_call_times)

    def new_call(self):
        self.api_call_times.append(time.time())

    def make_call(self):
        if self.get_num_recent_calls() < self.MAX_CALLS: 
            self.new_call()
        else:
            oldest_call = self.pop_time()
            while(not self.time_elapsed(oldest_call)):
                time.sleep(1)
            self.new_call()

gemini_throttler = Throttler()