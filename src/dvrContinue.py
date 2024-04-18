import threading
import time
from queue import Queue

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
            print("Sending table:", self.name, self.routing_table, "to", neighbor.name)  # line for debugging
            neighbor.queue.put({self.name: self.routing_table})  # Send routing table with router name

    def receive_routing_tables(self):
        received_tables = []
        while len(received_tables) < len(self.adjacent_routers):
            received_table = self.queue.get()
            router_name, table = list(received_table.items())[0]
            print(self.name, "Received table:", router_name, table, "", )  # line for debugging
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
            print("Updated table:", router_name, table)  # line for debugging
        return updated


def parse_input(input_data):
    lines = input_data.split('\n')
    num_routers = int(lines[0])
    router_names = lines[1].split()
    links = lines[2:]
    return num_routers, router_names, links

def main():
    # Read input data from a file
    file_path = "input2.txt" 
    try:
        with open(file_path, 'r') as file:
            input_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error occurred while reading the file: {e}")
        return

    num_routers, router_names, links = parse_input(input_data)

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

    iteration = 1
    try:
        while True:
            print(f"\nStarting iteration {iteration}...")
            updated_routers = []
            for router in routers.values():
                received_tables = router.receive_routing_tables()
                updated = router.update_routing_table(received_tables)
                if updated:
                    updated_routers.append(router.name)
            
            else:
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

            # Display Current routing tables
            print("\nCurrent Routing Tables:")
            for router in routers.values():
                router.display_routing_table(iteration)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")

if __name__ == "__main__":
    main()
