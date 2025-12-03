class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # ПОИСК
    def search(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def find(self, key):
        return self.search(self.root, key)

    # ВСТАВКА
    def insert_node(self, root, key):
        if root is None:
            return Node(key)
        elif key < root.key:
            root.left = self.insert_node(root.left, key)
        elif key > root.key:
            root.right = self.insert_node(root.right, key)
        return root

    def insert(self, key):
        self.root = self.insert_node(self.root, key)

    # ПОИСК МИНИМУМА И МАКСИМУМА
    def minimum(self, root):
        if root.left is None:
            return root
        return self.minimum(root.left)

    def maximum(self, root):
        if root.right is None:
            return root
        return self.maximum(root.right)

    def find_min(self):
        if self.root is None:
            return None
        return self.minimum(self.root).key

    def find_max(self):
        if self.root is None:
            return None
        return self.maximum(self.root).key

    # УДАЛЕНИЕ
    def delete_node(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is not None and root.right is not None:
                min_right = self.minimum(root.right)
                root.key = min_right.key
                root.right = self.delete_node(root.right, min_right.key)
            elif root.left is not None:
                root = root.left
            elif root.right is not None:
                root = root.right
            else:
                root = None
        return root

    def delete(self, key):
        self.root = self.delete_node(self.root, key)

    # ОБХОДЫ
    def preorder_traversal(self, root, result):
        if root is not None:
            result.append(root.key)
            self.preorder_traversal(root.left, result)
            self.preorder_traversal(root.right, result)

    def preorder(self):
        result = []
        self.preorder_traversal(self.root, result)
        return result

    def inorder_traversal(self, root, result):
        if root is not None:
            self.inorder_traversal(root.left, result)
            result.append(root.key)
            self.inorder_traversal(root.right, result)

    def inorder(self):
        result = []
        self.inorder_traversal(self.root, result)
        return result

    def postorder_traversal(self, root, result):
        if root is not None:
            self.postorder_traversal(root.left, result)
            self.postorder_traversal(root.right, result)
            result.append(root.key)

    def postorder(self):
        result = []
        self.postorder_traversal(self.root, result)
        return result

    # ОБХОД В ШИРИНУ
    def breadth_first_traversal(self):
        if self.root is None:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # ВИЗУАЛИЗАЦИЯ ДЕРЕВА
    def build_tree_lines(self, node, prefix="", is_left=True):
        if node is None:
            return []

        result = []
        result.append(prefix + ("└── " if is_left else "┌── ") + str(node.key))

        if node.left or node.right:
            if node.right:
                result += self.build_tree_lines(
                    node.right,
                    prefix + ("    " if is_left else "│   "),
                    False
                )
            if node.left:
                result += self.build_tree_lines(
                    node.left,
                    prefix + ("    " if is_left else "│   "),
                    True
                )

        return result

    def print_tree(self):
        if self.root is None:
            print("(пусто)")
            return
        for line in self.build_tree_lines(self.root, "", True):
            print(line)


if __name__ == "__main__":
    tree = BST()
    keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]

    for key in keys:
        tree.insert(key)

    print("\n===== ДЕРЕВО ПОСЛЕ ВСТАВКИ =====")
    tree.print_tree()

    print("\nУдаляем 3")
    tree.delete(3)

    print("\n===== ДЕРЕВО ПОСЛЕ УДАЛЕНИЯ 3 =====")
    tree.print_tree()

    print("\nВставляем 5")
    tree.insert(5)

    print("\n===== ДЕРЕВО ПОСЛЕ ВСТАВКИ 5 =====")
    tree.print_tree()

    print("Прямой обход:", tree.preorder())
    print("Центрированный обход:", tree.inorder())
    print("Обратный обход:", tree.postorder())
    print("Обход в ширину:", tree.breadth_first_traversal())

    # Поиск
    print("Поиск 6:", "Найден" if tree.find(6) else "Не найден")
    print("Поиск 99:", "Найден" if tree.find(99) else "Не найден")

    # Минимум и максимум
    print("Минимум:", tree.find_min())
    print("Максимум:", tree.find_max())

