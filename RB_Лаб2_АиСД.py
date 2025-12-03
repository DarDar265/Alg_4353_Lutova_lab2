class Node:
    def __init__(self, key, color='R', parent=None):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = parent

    def __repr__(self):
        return f"{self.key}{self.color}"


class RedBlackTree:
    def __init__(self):
        self.root = None

    def is_red(self, node):
        return node is not None and node.color == 'R'

    def is_black(self, node):
        return node is None or node.color == 'B'

    def minimum(self, node):
        cur = node
        while cur and cur.left:
            cur = cur.left
        return cur

    def maximum(self, node):
        cur = node
        while cur and cur.right:
            cur = cur.right
        return cur

    def find_node(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.find_node(node.left, key)
        else:
            return self.find_node(node.right, key)

    def find(self, key):
        return self.find_node(self.root, key)

    # Вращения
    def rotate_left(self, x):
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x is x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x is x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        y.right = x
        x.parent = y

    # Вставка
    def insert(self, key):
        node = Node(key)
        parent = None
        cur = self.root
        while cur:
            parent = cur
            if node.key < cur.key:
                cur = cur.left
            elif node.key > cur.key:
                cur = cur.right
            else:
                return
        node.parent = parent
        if parent is None:
            self.root = node
        else:
            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node
        self.fix_insert(node)

    def fix_insert(self, z):
        while z.parent is not None and self.is_red(z.parent):
            parent = z.parent
            grand = parent.parent
            if grand is None:
                break
            if parent is grand.left:
                uncle = grand.right
                if self.is_red(uncle):  #дядя красный
                    parent.color = 'B'
                    uncle.color = 'B'
                    grand.color = 'R'
                    z = grand
                else:
                    # дядя чёрный
                    if z is parent.right:
                        z = parent
                        self.rotate_left(z)
                        parent = z.parent
                        grand = parent.parent if parent else None
                    parent.color = 'B'
                    if grand:
                        grand.color = 'R'
                        self.rotate_right(grand)
            else:
                uncle = grand.left
                if self.is_red(uncle):
                    parent.color = 'B'
                    uncle.color = 'B'
                    grand.color = 'R'
                    z = grand
                else:
                    if z is parent.left:
                        z = parent
                        self.rotate_right(z)
                        parent = z.parent
                        grand = parent.parent if parent else None
                    parent.color = 'B'
                    if grand:
                        grand.color = 'R'
                        self.rotate_left(grand)
        if self.root:
            self.root.color = 'B'

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        else:
            if u is u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v:
            v.parent = u.parent

    # Удаление
    def delete(self, key):
        z = self.find(key)
        if z is None:
            return
        y = z
        y_original_color = y.color
        if z.left is None:
            x = z.right
            self.transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent is z:
                if x:
                    x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                if y.right:
                    y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            if y.left:
                y.left.parent = y
            y.color = z.color

        if y_original_color == 'B':
            self.fix_delete(x, z.parent if x is None else x.parent)

    def fix_delete(self, x, start_parent):
        while (x is None or self.is_black(x)) and x is not self.root:
            if x is not None and x.parent:
                parent = x.parent
            else:
                parent = start_parent
            if parent is None:
                break

            if x is parent.left:
                w = parent.right
                if self.is_red(w):
                    w.color = 'B'
                    parent.color = 'R'
                    self.rotate_left(parent)
                    w = parent.right
                if (w is None) or (self.is_black(w.left) and self.is_black(w.right)):
                    if w:
                        w.color = 'R'
                    x = parent
                    start_parent = x.parent
                else:
                    if self.is_black(w.right):
                        if w.left:
                            w.left.color = 'B'
                        w.color = 'R'
                        self.rotate_right(w)
                        w = parent.right
                    if w:
                        w.color = parent.color
                        if w.right:
                            w.right.color = 'B'
                    parent.color = 'B'
                    self.rotate_left(parent)
                    x = self.root
                    break
            else:
                w = parent.left
                if self.is_red(w):
                    w.color = 'B'
                    parent.color = 'R'
                    self.rotate_right(parent)
                    w = parent.left
                if (w is None) or (self.is_black(w.left) and self.is_black(w.right)):
                    if w:
                        w.color = 'R'
                    x = parent
                    start_parent = x.parent
                else:
                    if self.is_black(w.left):
                        if w.right:
                            w.right.color = 'B'
                        w.color = 'R'
                        self.rotate_left(w)
                        w = parent.left
                    if w:
                        w.color = parent.color
                        if w.left:
                            w.left.color = 'B'
                    parent.color = 'B'
                    self.rotate_right(parent)
                    x = self.root
                    break
        if x:
            x.color = 'B'

    # ОБХОДЫ
    def preorder_traversal(self, node, result):
        if node:
            result.append(node.key)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)

    def preorder(self):
        res = []
        self.preorder_traversal(self.root, res)
        return res

    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.key)
            self.inorder_traversal(node.right, result)

    def inorder(self):
        res = []
        self.inorder_traversal(self.root, res)
        return res

    def postorder_traversal(self, node, result):
        if node:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.key)

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

    # ВИЗУАЛИЗАЦИЯ
    def build_tree_lines(self, node, prefix="", is_left=True):
        if node is None:
            return []
        label = f"{node.key}{node.color}"
        result = [prefix + ("└── " if is_left else "┌── ") + label]
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
        if not self.root:
            print("(пусто)")
            return
        for line in self.build_tree_lines(self.root, "", True):
            print(line)

if __name__ == "__main__":
    tree = RedBlackTree()
    keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]

    for k in keys:
        tree.insert(k)

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

    print("Поиск 6:", "Найден" if tree.find(6) else "Не найден")
    print("Поиск 99:", "Найден" if tree.find(99) else "Не найден")

    print("Минимум:", tree.minimum(tree.root).key if tree.root else None)
    max_node = tree.maximum(tree.root) if tree.root else None
    print("Максимум:", max_node.key if max_node else None)
