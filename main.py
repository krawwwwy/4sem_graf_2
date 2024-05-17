import json
import random
from anytree import Node, RenderTree

class TreeNode:
    id_counter = 1

    def __init__(self, value):
        self.id = TreeNode.id_counter
        TreeNode.id_counter += 1
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def generate_n_tree(node_count, max_children):
    if node_count <= 0:
        return None

    root = TreeNode(random.randint(0, 1))
    remaining_nodes = node_count - 1
    nodes = [root]

    while remaining_nodes > 0 and nodes:
        parent = nodes.pop(0)
        num_children = min(remaining_nodes, random.randint(1, max_children))
        for _ in range(num_children):
            if remaining_nodes > 0:
                child = TreeNode(random.randint(0, 1))
                parent.add_child(child)
                nodes.append(child)
                remaining_nodes -= 1

    return root


def tree_to_anytree(node):
    if not node:
        return None
    anytree_node = Node(f"Value: {node.value}")
    for child in node.children:
        child_anytree = tree_to_anytree(child)
        if child_anytree:
            child_anytree.parent = anytree_node
    return anytree_node


def tree_to_dict(node):
    if not node:
        return None
    return {
        "id": node.id,
        "value": node.value,
        "children": [tree_to_dict(child) for child in node.children]
    }


def save_tree_to_json(root, filename):
    tree_dict = tree_to_dict(root)
    with open(filename, 'w') as f:
        json.dump(tree_dict, f, indent=4)


def load_tree_from_json(filename):
    with open(filename, 'r') as f:
        tree_dict = json.load(f)

    def dict_to_tree(d):
        if not d:
            return None
        node = TreeNode(d['value'])
        node.id = d['id']
        for child_dict in d['children']:
            child = dict_to_tree(child_dict)
            if child:
                node.add_child(child)
        return node

    return dict_to_tree(tree_dict)


def find_leaves(node, current_height, leaves, target_height):
    if not node.children:
        leaves.append((node, current_height))
    else:
        for child in node.children:
            find_leaves(child, current_height + 1, leaves, target_height)


def find_subtrees_with_leaves_in_height_range(node, min_height, max_height):
    result = []

    def helper(node, current_height):
        leaves = []
        find_leaves(node, current_height, leaves, current_height)
        if all(min_height <= height - current_height <= max_height for _, height in leaves):
            result.append(node)
        for child in node.children:
            helper(child, current_height + 1)

    helper(node, 0)
    return result


node_count = int(input("Введите количество узлов дерева: "))
max_children = int(input("Введите максимальное количество потомков узла: "))
min_height = int(input("Введите минимальную высоту: "))
max_height = int(input("Введите максимальную высоту: "))

root = generate_n_tree(node_count, max_children)
save_tree_to_json(root, 'n_tree.json')

root = load_tree_from_json('n_tree.json')

root_anytree = tree_to_anytree(root)

subtrees = find_subtrees_with_leaves_in_height_range(root, min_height, max_height)

print("Original Tree Structure:")
for pre, _, node in RenderTree(root_anytree):
    print("%s%s" % (pre, node.name))

print()

for i, subtree in enumerate(subtrees):
    print(f"Subtree {i + 1}:")
    subtree_anytree = tree_to_anytree(subtree)
    for pre, _, node in RenderTree(subtree_anytree):
        print("%s%s" % (pre, node.name))
    print()
