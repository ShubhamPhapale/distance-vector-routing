import threading
import time
from queue import Queue
import datetime

class Router:
    def __init__(self, name, adjacent_routers):
        self.name = name
        self.routing_table = {name: 0}  # Initialize with self as destination with cost 0
        self.adjacent_routers = adjacent_routers
        self.queue = Queue()

    def add_link(self, destination, cost):
        self.routing_table[destination] = cost

    def display_routing_table(self, iteration):
        print(f"Iteration {iteration}: Routing table for Router {self.name}:")
        for destination, cost in self.routing_table.items():
            print(f"Destination: {destination}, Cost: {cost}")

    def send_routing_table(self):
        time.sleep(2)  # Wait for 2 seconds before sending
        for neighbor in self.adjacent_routers:
            # print("Sending table:", self.name, self.routing_table, "to", neighbor.name)  # line for debugging
            neighbor.queue.put({self.name: self.routing_table})  # Send routing table with router name

    def receive_routing_tables(self):
        received_tables = []
        while len(received_tables) < len(self.adjacent_routers):
            received_table = self.queue.get()
            router_name, table = list(received_table.items())[0]
            # print(self.name, "Received table:", router_name, table, "", )  # line for debugging
            received_tables.append({router_name: table})
        return received_tables

    def update_routing_table(self, received_tables):
        updated = False
        for received_table in received_tables:
            router_name, table = list(received_table.items())[0]  # Extract router name and table
            for destination, cost in table.items():
                if destination not in self.routing_table or self.routing_table[destination] > cost + self.routing_table[router_name]:
                    self.routing_table[destination] = cost + self.routing_table[router_name]
                    updated = True
            # print("Updated table:", router_name, table)  # line for debugging
        return updated


def parse_input(input_data):
    lines = input_data.split('\n')
    num_routers = int(lines[0])
    router_names = lines[1].split()
    links = lines[2:]
    return num_routers, router_names, links

def parse_changes(change_data):
    changes = []
    lines = change_data.split('\n')
    for line in lines:
        if line.strip():
            data = line.split()
            if len(data) == 4:
                src, dest, cost, timestamp = data
                changes.append((src, dest, int(cost), int(timestamp)))
            else:
                print("Invalid format for change:", line)
    return changes

# Function to monitor changes in the network
def monitor_changes(routers, changes, start_time):
    if changes:
        while True:
            current_time = time.time()
            for src, dest, cost, timestamp in changes:
                if current_time - start_time >= timestamp:
                    # print(current_time)
                    if current_time - start_time >= timestamp and current_time - start_time - 2 < timestamp: 
                        print(f"Change detected: {src} -> {dest}, cost: {cost}, timestamp: {timestamp}")
                        routers[src].add_link(dest, cost)
                        routers[dest].add_link(src, cost)
            time.sleep(2)  # Check for changes every 2 second
    else:
        print("No changes to monitor.")

def main():
    # Record the start time
    start_time = time.time()

    # Read input data from a file
    topology_file = "input.txt"
    change_file = "change.txt" #can be an empty file!
    try:
        with open(topology_file, 'r') as file:
            input_data = file.read()
        with open(change_file, 'r') as file:
            change_data = file.read()
    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}")
        return
    except Exception as e:
        print(f"Error occurred: {e}")
        return

    num_routers, router_names, links = parse_input(input_data)
    changes = parse_changes(change_data)

    routers = {}
    for name in router_names:
        routers[name] = Router(name, [])

    for link in links:
        if link == "EOF":
            break
        src, dest, cost = link.split()
        routers[src].add_link(dest, int(cost))
        routers[dest].add_link(src, int(cost))  # Bidirectional link
        routers[src].adjacent_routers.append(routers[dest])
        routers[dest].adjacent_routers.append(routers[src])

    for router in routers.values():
        router.display_routing_table(0)

    # Start threads for each router
    threads = []
    for router in routers.values():
        thread = threading.Thread(target=router.send_routing_table)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Start background thread to monitor changes
    change_monitor_thread = threading.Thread(target=monitor_changes, args=(routers, changes, start_time))
    change_monitor_thread.daemon = True  # Set as daemon so it doesn't block program termination
    change_monitor_thread.start()

    iteration = 1
    try:
        while True:
            print(f"\nStarting iteration {iteration}...")
            current_time = time.time()
            print(f"Time Passed : {current_time - start_time} seconds\n")
            updated_routers = []
            for router in routers.values():
                received_tables = router.receive_routing_tables()
                updated = router.update_routing_table(received_tables)
                if updated:
                    updated_routers.append(router.name)

            if len(updated_routers):
                print("Updated routers:", updated_routers)
            else:
                print("No Router Updated")
            iteration += 1

            # Start new threads for sending routing tables
            threads = []
            for router in routers.values():
                thread = threading.Thread(target=router.send_routing_table)
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            # Display final routing tables
            print("\nCurrent Routing Tables:")
            for router in routers.values():
                router.display_routing_table(iteration)

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")

if __name__ == "__main__":
    main()
