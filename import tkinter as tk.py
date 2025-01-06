import tkinter as tk
from tkinter import font
from typing import Optional, List
import random


class Node:
    def __init__(self, value: int):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height = 1
        self.x = 0  # For visualization
        self.y = 0  # For visualization


class BSTVisualizer:
    def __init__(self):
        self.root: Optional[Node] = None
        self.window = tk.Tk()
        self.window.title("Enhanced BST Visualizer")

        # Configure window
        self.window.geometry("1200x800")
        self.window.minsize(800, 600)
        self.window.configure(bg="lightgray")

        # Canvas setup for tree visualization with a gradient background
        self.canvas = tk.Canvas(self.window, bg='white', bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Control panel with buttons and input
        self.control_frame = tk.Frame(self.window, bg="#2c3e50")
        self.control_frame.pack(fill=tk.X, pady=5)

        # Input field with label
        tk.Label(self.control_frame, text="Value:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.value_entry = tk.Entry(self.control_frame, width=10, font=("Arial", 12))
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Button styling
        button_font = font.Font(family="Arial", size=12, weight="bold")
        buttons = [
            ("Insert", self.insert_from_entry),
            ("Delete", self.delete_from_entry),
            ("Search", self.search_from_entry),
            ("Preorder", self.display_preorder),
            ("Inorder", self.display_inorder),
            ("Postorder", self.display_postorder),
            ("Balance", self.balance_tree),
            ("Random", self.insert_random),
            ("Clear", self.clear_tree),
        ]

        for text, command in buttons:
            button = tk.Button(self.control_frame, text=text, font=button_font, command=command, fg="white", bg="#3498db", relief="raised")
            button.pack(side=tk.LEFT, padx=5, pady=2)
            button.bind("<Enter>", lambda event, b=button: b.config(bg="#2980b9"))
            button.bind("<Leave>", lambda event, b=button: b.config(bg="#3498db"))

        # Result label
        self.result_label = tk.Label(self.window, text="", bg="lightgray", wraplength=1100, font=("Arial", 12))
        self.result_label.pack(fill=tk.X, pady=5)

    def insert(self, value: int) -> None:
        """Insert a value into the BST."""
        self.root = self._insert_recursive(self.root, value)
        self.update_display()

    def _insert_recursive(self, node: Optional[Node], value: int) -> Node:
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node

    def delete(self, value: int) -> None:
        """Delete a value from the BST."""
        self.root = self._delete_recursive(self.root, value)
        self.update_display()

    def _delete_recursive(self, node: Optional[Node], value: int) -> Optional[Node]:
        if not node:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node

    def _min_value_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, value: int) -> bool:
        """Search for a value in the BST."""
        path = []
        found = self._search_recursive(self.root, value, path)
        self.update_display(highlight_path=path)
        return found

    def _search_recursive(self, node: Optional[Node], value: int, path: List[Node]) -> bool:
        if not node:
            return False

        path.append(node)
        if node.value == value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value, path)
        return self._search_recursive(node.right, value, path)

    def _get_height(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return node.height

    def _calculate_positions(self, node: Optional[Node], level: int, min_x: float, max_x: float) -> None:
        if not node:
            return

        # Calculate x and y coordinates
        node.x = (min_x + max_x) / 2
        node.y = level * 100 + 50

        # Recursively calculate positions for children
        if node.left:
            self._calculate_positions(node.left, level + 1, min_x, node.x)
        if node.right:
            self._calculate_positions(node.right, level + 1, node.x, max_x)

    def update_display(self, highlight_path: List[Node] = None) -> None:
        """Update the tree visualization."""
        self.canvas.delete("all")
        if not self.root:
            return

        # Draw a gradient background
        self._draw_gradient()

        # Calculate positions
        self._calculate_positions(self.root, 0, 50, self.canvas.winfo_width() - 50)

        # Draw edges with customized colors
        self._draw_edges(self.root)

        # Draw nodes with special colors
        self._draw_nodes(self.root, highlight_path or [])

    def _draw_gradient(self) -> None:
        """Draw a gradient background for the canvas."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        for i in range(height):
            # Gradient color logic: transition from light yellow to light green
            red = 255 - i * 255 // height  # Starts at full red (light yellow)
            green = 255                   # Full green throughout
            blue = 128 + i * 127 // height  # Transitions from light yellow to green
            color = f'#{red:02x}{green:02x}{blue:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def _draw_edges(self, node: Optional[Node]) -> None:
        if not node:
            return

        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill="darkblue", width=2)
            self._draw_edges(node.left)

        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="darkorange", width=2)
            self._draw_edges(node.right)

    def _draw_nodes(self, node: Optional[Node], highlight_path: List[Node]) -> None:
        if not node:
            return

        # Node color logic
        if node in highlight_path:
            fill_color = "yellow"  # Highlighted color (search path)
        elif node.value % 2 == 0:
            fill_color = "lightgreen"  # Even nodes have a green background
        else:
            fill_color = "lightblue"  # Odd nodes have a blue background

        # Draw circle with selected fill color
        radius = 20
        self.canvas.create_oval(node.x - radius, node.y - radius,
                                node.x + radius, node.y + radius,
                                fill=fill_color, outline="black", width=2)

        # Draw value inside node
        self.canvas.create_text(node.x, node.y, text=str(node.value), font=("Arial", 12, "bold", "italic"))

        # Recursively draw left and right child nodes
        self._draw_nodes(node.left, highlight_path)
        self._draw_nodes(node.right, highlight_path)

    def insert_random(self) -> None:
        """Insert a random value."""
        value = random.randint(1, 100)
        self.insert(value)
        self.result_label.config(text=f"Inserted random value {value}")

    def clear_tree(self) -> None:
        """Clear the tree and reset the display."""
        self.root = None
        self.update_display()
        self.result_label.config(text="Tree has been cleared.")

    def insert_from_entry(self) -> None:
        """Insert a value from the entry field."""
        value = int(self.value_entry.get())
        self.insert(value)
        self.result_label.config(text=f"Inserted value {value}")

    def delete_from_entry(self) -> None:
        """Delete a value from the entry field."""
        value = int(self.value_entry.get())
        self.delete(value)
        self.result_label.config(text=f"Deleted value {value}")

    def search_from_entry(self) -> None:
        """Search for a value from the entry field."""
        value = int(self.value_entry.get())
        found = self.search(value)
        self.result_label.config(text=f"Value {value} {'found' if found else 'not found'}")

    def display_preorder(self) -> None:
        """Display the preorder traversal."""
        result = self._preorder_traversal(self.root)
        self.result_label.config(text=f"Preorder: {', '.join(map(str, result))}")

    def display_inorder(self) -> None:
        """Display the inorder traversal."""
        result = self._inorder_traversal(self.root)
        self.result_label.config(text=f"Inorder: {', '.join(map(str, result))}")

    def display_postorder(self) -> None:
        """Display the postorder traversal."""
        result = self._postorder_traversal(self.root)
        self.result_label.config(text=f"Postorder: {', '.join(map(str, result))}")

    def _preorder_traversal(self, node: Optional[Node]) -> List[int]:
        if not node:
            return []
        return [node.value] + self._preorder_traversal(node.left) + self._preorder_traversal(node.right)

    def _inorder_traversal(self, node: Optional[Node]) -> List[int]:
        if not node:
            return []
        return self._inorder_traversal(node.left) + [node.value] + self._inorder_traversal(node.right)

    def _postorder_traversal(self, node: Optional[Node]) -> List[int]:
        if not node:
            return []
        return self._postorder_traversal(node.left) + self._postorder_traversal(node.right) + [node.value]

    def balance_tree(self) -> None:
        """Balance the BST."""
        values = self._inorder_traversal(self.root)
        self.root = self._build_balanced_tree(values)
        self.update_display()
        self.result_label.config(text="Tree has been balanced.")

    def _build_balanced_tree(self, values: List[int]) -> Optional[Node]:
        if not values:
            return None
        mid = len(values) // 2
        root = Node(values[mid])
        root.left = self._build_balanced_tree(values[:mid])
        root.right = self._build_balanced_tree(values[mid + 1:])
        return root

    def run(self) -> None:
        """Run the visualization application."""
        self.update_display()
        self.window.mainloop()


if __name__ == "__main__":
    visualizer = BSTVisualizer()
    visualizer.run()
