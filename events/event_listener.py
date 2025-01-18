import time 

class EventListener:
    def __init__(self, web3, contract):
        self.web3 = web3
        self.contract = contract 

    def listen_for_events(self):
        print("Listening for events....")
        event_filter = self.contract.events.MyEvent.createFilter(fromBlock="latest")

        while True:
            for event in event_filter.get_new_entries():
                print(f"New event detected: {event}")
            time.sleep(2) 