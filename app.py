from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current, value):
        if value < current.value:
            if current.left:
                self._insert_recursive(current.left, value)
            else:
                current.left = Node(value)
        else:
            if current.right:
                self._insert_recursive(current.right, value)
            else:
                current.right = Node(value)

    def to_dict(self, node):
        """Convert the binary tree to a nested dictionary suitable for D3.js."""
        if not node:
            return None
        return {
            "name": node.value,
            "children": list(filter(None, [self.to_dict(node.left), self.to_dict(node.right)])),
        }

    def build_balanced_tree(self, values):
        """Build a balanced binary tree by recursively picking the middle element."""
        sorted_values = sorted(values)
        self.root = self._build_balanced_tree_recursive(sorted_values)

    def _build_balanced_tree_recursive(self, sorted_values):
        if not sorted_values:
            return None

        mid_idx = len(sorted_values) // 2
        node = Node(sorted_values[mid_idx])
        
        node.left = self._build_balanced_tree_recursive(sorted_values[:mid_idx])
        node.right = self._build_balanced_tree_recursive(sorted_values[mid_idx+1:])
        
        return node


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    tree_values = request.form['tree_values']
    values = [int(v.strip()) for v in tree_values.split(',')]

    tree = BinaryTree()

    # Create a balanced binary tree
    tree.build_balanced_tree(values)

    tree_data = tree.to_dict(tree.root)
    return render_template('result.html', tree_data=tree_data)


if __name__ == '__main__':
    app.run(debug=True)
