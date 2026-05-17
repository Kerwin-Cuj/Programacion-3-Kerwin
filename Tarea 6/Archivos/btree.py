class BTreeNode:
    def __init__(self, t_min, t_max, leaf=False):
        self.t_min = t_min
        self.t_max = t_max
        self.keys = []
        self.children = []
        self.leaf = leaf

class BTree:
    def __init__(self, t_min, t_max):
        self.root = BTreeNode(t_min, t_max, True)
        self.t_min = t_min
        self.t_max = t_max

    def search(self, k, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return True
        if node.leaf:
            return False
        return self.search(k, node.children[i])

    def insert(self, k):
        root = self.root
        if len(root.keys) == self.t_max:
            new_root = BTreeNode(self.t_min, self.t_max, False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(k)
            node.keys.sort()
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.t_max:
                self.split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def split_child(self, parent, i):
        t_min = self.t_min
        y = parent.children[i]
        z = BTreeNode(t_min, self.t_max, y.leaf)
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t_min])
        z.keys = y.keys[t_min+1:]
        y.keys = y.keys[:t_min]
        if not y.leaf:
            z.children = y.children[t_min+1:]
            y.children = y.children[:t_min+1]

    def delete(self, k):
        print(f"Función eliminar({k}) aún no implementada.")

    def export_graphviz(self, node=None, dot=None, parent=None):
        import graphviz
        node = node or self.root
        dot = dot or graphviz.Digraph()
        label = "|".join(map(str, node.keys))
        dot.node(str(id(node)), label)
        if parent:
            dot.edge(str(id(parent)), str(id(node)))
        for child in node.children:
            self.export_graphviz(child, dot, node)
        return dot
