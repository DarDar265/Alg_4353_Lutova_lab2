class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    # ВРАЩЕНИЯ
    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y
    # ВСТАВКА

    def insert_node(self, node, key):
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self.insert_node(node.left, key)
        elif key > node.key:
            node.right = self.insert_node(node.right, key)
        else:
            return node

        self.update_height(node)

        b = self.balance(node)

        # LL
        if b > 1 and key < node.left.key:
            return self.rotate_right(node)

        # RR
        if b < -1 and key > node.right.key:
            return self.rotate_left(node)

        # LR
        if b > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # RL
        if b < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, key):
        self.root = self.insert_node(self.root, key)

    # УДАЛЕНИЕ
    def min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def delete_node(self, root, key):
        if root is None:
            return None

        # удаление BST
        if key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right, temp.key)

        if root is None:
            return None

        self.update_height(root)

        b = self.balance(root)

        # LL
        if b > 1 and self.balance(root.left) >= 0:
            return self.rotate_right(root)

        # LR
        if b > 1 and self.balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # RR
        if b < -1 and self.balance(root.right) <= 0:
            return self.rotate_left(root)

        #RL
        if b < -1 and self.balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def delete(self, key):
        self.root = self.delete_node(self.root, key)

    # ПОИСК МИН МАКС
    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def find(self, key):
        return self.search(self.root, key)

    def find_min(self):
        return self.min_value_node(self.root).key if self.root else None

    def find_max(self):
        cur = self.root
        while cur and cur.right:
            cur = cur.right
        return cur.key if cur else None

    # ОБХОДЫ
    def preorder_traversal(self, node, res):
        if node:
            res.append(node.key)
            self.preorder_traversal(node.left, res)
            self.preorder_traversal(node.right, res)

    def preorder(self):
        res = []
        self.preorder_traversal(self.root, res)
        return res

    def inorder_traversal(self, node, res):
        if node:
            self.inorder_traversal(node.left, res)
            res.append(node.key)
            self.inorder_traversal(node.right, res)

    def inorder(self):
        res = []
        self.inorder_traversal(self.root, res)
        return res

    def postorder_traversal(self, node, res):
        if node:
            self.postorder_traversal(node.left, res)
            self.postorder_traversal(node.right, res)
            res.append(node.key)

    def postorder(self):
        res = []
        self.postorder_traversal(self.root, res)
        return res

    def breadth_first_traversal(self):
        if self.root is None:
            return []
        q = [self.root]
        res = []
        while q:
            n = q.pop(0)
            res.append(n.key)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        return res

    # ВИЗУАЛИЗАЦИЯ ДЕРЕВА
    def build_tree_lines(self, node, prefix="", is_left=True):
        if node is None:
            return []

        result = []
        result.append(prefix + ("└── " if is_left else "┌── ") + f"{node.key} (h={node.height})")

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
        for line in self.build_tree_lines(self.root):
            print(line)


if __name__ == "__main__":
    tree = AVL()
    keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]

    for k in keys:
        tree.insert(k)

    print("\n===== ДЕРЕВО ПОСЛЕ ВСТАВКИ =====")
    tree.print_tree()

    print("\nУдаляем 3")
    tree.delete(3)

    print("\n===== ДЕРЕВО ПОСЛЕ УДАЛЕНИЯ =====")
    tree.print_tree()

    print("\nВставляем 5")
    tree.insert(5)

    print("\n===== ДЕРЕВО ПОСЛЕ ВСТАВКИ 5 =====")
    tree.print_tree()

    print("Прямой обход:", tree.preorder())
    print("Центрированный обход:", tree.inorder())
    print("Обратный обход:", tree.postorder())
    print("Обход в ширину:", tree.breadth_first_traversal())

    print("Поиск 6:", "Найден" if tree.find(6) else "Не найден")
    print("Поиск 99:", "Найден" if tree.find(99) else "Не найден")

    print("Минимум:", tree.find_min())
    print("Максимум:", tree.find_max())
