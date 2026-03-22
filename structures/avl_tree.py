from models import Client
from typing import Optional, Callable, List


class TreeNode:
    def __init__(self, client: Client):
        self.client: Client = client
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        self.height: int = 1


class AVLTree:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    def _get_height(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node: TreeNode) -> None:
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _right_rotate(self, y: TreeNode) -> TreeNode:
        x = y.left
        assert x is not None, "Ошибка структуры: левый потомок отсутствует при правом вращении"
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _left_rotate(self, x: TreeNode) -> TreeNode:
        y = x.right
        assert y is not None, "Ошибка структуры: правый потомок отсутствует при левом вращении"
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, client: Client) -> None:
        """Публичный метод вставки клиента."""
        self.root = self._insert_node(self.root, client)

    def _insert_node(self, node: Optional[TreeNode], client: Client) -> TreeNode:
        if not node:
            return TreeNode(client)
        elif client.passport_num < node.client.passport_num:
            node.left = self._insert_node(node.left, client)
        elif client.passport_num > node.client.passport_num:
            node.right = self._insert_node(node.right, client)
        else:
            return node

        self._update_height(node)

        balance = self._get_balance(node)

        if balance > 1 and node.left and client.passport_num < node.left.client.passport_num:
            return self._right_rotate(node)

        if balance < -1 and node.right and client.passport_num > node.right.client.passport_num:
            return self._left_rotate(node)

        if balance > 1 and node.left and client.passport_num > node.left.client.passport_num:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and node.right and client.passport_num < node.right.client.passport_num:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, passport: str) -> None:
        """Публичный метод удаления клиента по паспорту."""
        self.root = self._delete_node(self.root, passport)

    def _get_min_value_node(self, node: TreeNode) -> TreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_node(self, node: Optional[TreeNode], passport: str) -> Optional[TreeNode]:
        if not node:
            return node

        if passport < node.client.passport_num:
            node.left = self._delete_node(node.left, passport)
        elif passport > node.client.passport_num:
            node.right = self._delete_node(node.right, passport)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self._get_min_value_node(node.right)
            node.client = temp.client
            node.right = self._delete_node(node.right, temp.client.passport_num)

        self._update_height(node)

        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        if balance > 1 and self._get_balance(node.left) < 0:
            assert node.left is not None
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        if balance < -1 and self._get_balance(node.right) > 0:
            assert node.right is not None
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node


    def search(self, passport: str) -> Optional[Client]:
        """Точный поиск по номеру паспорта ($O(\\log N)$)."""
        current = self.root
        while current:
            if passport == current.client.passport_num:
                return current.client
            elif passport < current.client.passport_num:
                current = current.left
            else:
                current = current.right
        return None

    def pre_order_search(self, match_condition: Callable[[Client], bool]) -> List[Client]:
        """
        Прямой обход дерева (Корень -> Левое -> Правое).
        Используется для поиска по фрагментам ФИО или адреса (п. 9.6.11).
        Возвращает список клиентов, удовлетворяющих условию match_condition.
        """
        results: List[Client] = []

        def _traverse(node: Optional[TreeNode]) -> None:
            if not node:
                return
            
            if match_condition(node.client):
                results.append(node.client)
                
            _traverse(node.left)
            
            _traverse(node.right)

        _traverse(self.root)
        return results

    def clear(self) -> None:
        """Очистка данных о клиентах."""
        self.root = None