import random


class SkipList:
    def __init__(self):
        self.head = Node(None, None)

    def insert(self, value):
        node_before_node_to_insert, nodes_along_search_path = self.get_node_where_value_should_be_and_search_path(value)

        # don't add duplicates:
        if node_before_node_to_insert.value == value:
            return

        # create new node to insert
        node_after_node_to_insert = node_before_node_to_insert.next_node
        new_node_to_insert = Node(value, node_after_node_to_insert)
        node_before_node_to_insert.next_node = new_node_to_insert
        new_node_to_insert.previous_node = node_before_node_to_insert
        if new_node_to_insert.next_node:
            new_node_to_insert.next_node.previous_node = new_node_to_insert

        # add levels
        self.add_node_levels(new_node_to_insert, nodes_along_search_path)

    def search(self, value):
        """returns True if value is in SkipList, False if value is not in SkipList"""
        possible_matching_node, nodes_along_search_path = self.get_node_where_value_should_be_and_search_path(value)
        return possible_matching_node is not None and possible_matching_node.value == value

    def delete(self, value):
        possible_matching_node, nodes_along_search_path = self.get_node_where_value_should_be_and_search_path(value)
        if possible_matching_node is None or possible_matching_node.value != value:
            return
        node_to_remove = possible_matching_node
        node_to_remove.previous_node.next_node = node_to_remove.next_node
        if node_to_remove.next_node:
            node_to_remove.next_node.previous_node = node_to_remove.previous_node
        # remove node levels instead of add node levels
        while node_to_remove.above_node:
            # check if previous and next are head and None?
            node_to_remove = node_to_remove.above_node
            node_to_remove.previous_node.next_node = node_to_remove.next_node
            if node_to_remove.next_node:
                node_to_remove.next_node.previous_node = node_to_remove.previous_node

    def add_node_levels(self, node_to_insert, nodes_along_search_path):
        while random.random() < .5:
            if nodes_along_search_path:
                prev_node = nodes_along_search_path.pop()
            else:
                new_head = Node(None, None)
                self.head.above_node = new_head
                new_head.below_node = self.head
                self.head = new_head
                prev_node = new_head
            node_to_insert.add_level(prev_node)
            node_to_insert = node_to_insert.above_node

    def get_node_where_value_should_be_and_search_path(self, value):
        nodes_along_search_path = []
        curr = self.head
        while curr:
            if curr.next_node is None or value < curr.next_node.value:
                # drop down a level
                if curr.below_node:
                    # nodes only added to search path when dropping a level down
                    nodes_along_search_path.append(curr)
                    curr = curr.below_node
                else:
                    break  # we're on the bottom level, and this is where value goes
            else:
                curr = curr.next_node
        # if we're NOT on the bottom level, move to the "curr" node that is on the bottom level
        while curr.below_node is not None:
            nodes_along_search_path.append(curr)
            curr = curr.below_node

        return curr, nodes_along_search_path

    def __str__(self):
        output = ""
        total_values = 0
        max_num_vals_to_print_per_row = 20
        row_start_node = self.head
        while row_start_node:
            row_values = self.get_values_in_row(row_start_node)
            num_vals_in_row = len(row_values)
            total_values += num_vals_in_row
            if num_vals_in_row <= max_num_vals_to_print_per_row:
                output += f"len: {num_vals_in_row} -> {row_values}\n"
            else:
                half = max_num_vals_to_print_per_row//2
                output += f"len: {num_vals_in_row} -> {row_values[:half]} ... {row_values[-half:]}\n"
            row_start_node = row_start_node.below_node
        output += f"total vals: {total_values}"
        return output

    @staticmethod
    def get_values_in_row(row_start_node):
        nodes_in_row = []
        next_node_in_row = row_start_node.next_node
        while next_node_in_row:
            nodes_in_row.append(next_node_in_row.value)
            next_node_in_row = next_node_in_row.next_node
        return nodes_in_row

    def get_all_values(self):
        current_row_start_node = self.head
        while current_row_start_node.below_node:
            current_row_start_node = current_row_start_node.below_node
        return self.get_values_in_row(current_row_start_node)


class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node
        self.below_node = None
        self.above_node = None
        self.previous_node = None  # only needed for bottom level

    def add_level(self, previous_node_on_level):
        above_node = Node(self.value, previous_node_on_level.next_node)
        if previous_node_on_level.next_node:
            previous_node_on_level.next_node.previous_node = above_node
        above_node.below_node = self
        above_node.above_node = None
        previous_node_on_level.next_node = above_node
        above_node.previous_node = previous_node_on_level
        self.above_node = above_node


random.seed(8)
skip_list = SkipList()
rand_vals = random.sample(range(1000), 1000)
for i in rand_vals:
    skip_list.insert(i)

values = skip_list.get_all_values()
assert(values == sorted(rand_vals))

print(skip_list)

# Output when using random seed 8, random.sample(range(1000), 1000)
# len: 1 -> [305]
# len: 2 -> [305, 691]
# len: 7 -> [199, 305, 544, 621, 691, 755, 984]
# len: 12 -> [199, 305, 544, 579, 611, 621, 636, 652, 691, 728, 755, 984]
# len: 30 -> [11, 182, 194, 199, 305, 326, 389, 417, 513, 544] ... [691, 728, 755, 793, 858, 860, 861, 876, 902, 984]
# len: 56 -> [11, 60, 87, 100, 182, 194, 199, 212, 266, 290] ... [829, 858, 860, 861, 876, 902, 937, 959, 971, 984]
# len: 114 -> [6, 11, 22, 60, 73, 84, 87, 100, 129, 137] ... [885, 902, 923, 937, 959, 961, 964, 971, 974, 984]
# len: 232 -> [5, 6, 11, 22, 24, 34, 35, 50, 55, 60] ... [961, 964, 971, 972, 974, 976, 978, 984, 991, 994]
# len: 470 -> [3, 4, 5, 6, 7, 11, 19, 22, 23, 24] ... [974, 976, 977, 978, 983, 984, 988, 990, 991, 994]
# len: 1000 -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] ... [990, 991, 992, 993, 994, 995, 996, 997, 998, 999]
# total vals: 1924
