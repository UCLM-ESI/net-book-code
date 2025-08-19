import heapq


def dijkstra(graph, source, destination=None):
    # Initialize costs as inf and source cost to 0
    costs = {node: float('inf') for node in graph}
    costs[source] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, source)]  # Priority queue with tentative costs
    visited = []

    while priority_queue:
        # Select node with the smallest tentative cost
        current_cost, current_node = heapq.heappop(priority_queue)

        # Ignore if it's not better than tentative
        if current_cost > costs[current_node]:
            continue

        visited.append(current_node)
        if destination and current_node == destination:
            break

        # Update neighbors tentative labels
        for neighbor, weight in graph[current_node].items():
            cost = current_cost + weight

            if cost < costs[neighbor]:  # If shorter path is found, update it
                costs[neighbor] = cost
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (cost, neighbor))

    return costs, previous_nodes, visited


class Network:
    def __init__(self, links):
        self.graph = links

    def get_path(self, source, destination):
        costs, previous_nodes, visited = dijkstra(self.graph, source)
        path = []
        current_node = destination
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]

        return list(reversed(path))

    def get_paths(self, source):
        nodes = self.graph.keys()
        paths = {}
        for dest in nodes:
            paths[dest] = self.get_path(source, dest)
        return paths

    def routing_table(self, source):
        routing_table = {}
        paths = self.get_paths(source)

        for node, path in paths.items():
            next_hop = path[1] if len(path) > 1 else '-'
            routing_table[node] = next_hop

        return routing_table
