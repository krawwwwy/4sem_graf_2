import json


class TreeNode:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.children = []


def build_tree(nodes):
    node_dict = {node['id']: TreeNode(node['id'], node['value']) for node in nodes}

    for node in nodes:
        if node['children']:
            for child_id in node['children']:
                node_dict[node['id']].children.append(node_dict[child_id])

    return node_dict[0]  # assuming the root node has id 0


def serialize(node):
    if node is None:
        return None
    return {
        "id": node.id,
        "value": node.value,
        "children": [serialize(child) for child in node.children]
    }


def con():
    nodes = []
    print(
        "Введите узлы дерева в формате: id val children (где children - список id дочерних узлов через запятую или 'None'):")
    while True:
        line = input("Введите узел (или оставьте строку пустой для завершения ввода): ").strip()
        if not line:
            break
        parts = line.split()
        id = int(parts[0])
        value = int(parts[1])
        if parts[2] != 'None':
            children = list(map(int, parts[2].split(',')))
        else:
            children = []
        children.reverse()
        print(children)
        nodes.append({"id": id, "value": value, "children": children})

    root = build_tree(nodes)
    tree_json = serialize(root)
    with open("tree.json", "w", encoding="utf-8") as f:
        json.dump(tree_json, f, ensure_ascii=False, indent=4)
    print("Дерево сохранено в tree.json")

con()

