from traffic_simulator.model import Road


class CityMapLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, road_id: int) -> None:
        new_road = Road(id=road_id)

        if self.head is None:
            self.head = new_road
            return

        current_road = self.head

        while current_road.next:
            current_road = current_road.next

        current_road.next = new_road


