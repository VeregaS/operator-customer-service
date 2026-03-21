from models import Record
from typing import Optional, List


class ListNode:
    def __init__(self, record: Record):
        self.record = record
        self.next: Optional['ListNode'] = None 


class CircularLinkedList:
    def __init__(self):
        self.head: Optional[ListNode] = None
        self.tail: Optional[ListNode] = None

    def search_by_passport(self, target_passport: str) -> List[Record]:
        ans: List[Record] = [] 
        if self.head is None:
            return ans
        current: ListNode = self.head
        while True:
            if current.record.passport_num == target_passport:
                ans.append(current.record)
            if current.next is None or current.next == self.head:
                break
            current = current.next
        return ans
    
    def search_by_sim(self, target_sim: str) -> List[Record]:
        ans: List[Record] = [] 
        if self.head is None:
            return ans
        current: ListNode = self.head
        while True:
            if current.record.passport_num == target_sim:
                ans.append(current.record)
            if current.next is None or current.next == self.head:
                break
            current = current.next
        return ans
    
    def find_tail(self) -> Optional['ListNode']:
        if not self.head:
            return None
        current: ListNode = self.head
        while current.next and current.next != self.head:
            current = current.next
        return current
        
    def delete_by_passport(self, passport_target: str) -> None:
        if not self.head:
            return
        current: ListNode = self.head
        previous: 'ListNode' = self.find_tail() # type: ignore
        while True:
            next_node: Optional['ListNode'] = current.next
            if next_node is None:
                break
            if current.record.passport_num == passport_target:
                if current == current.next:
                    self.head = None
                    break 
                previous.next = next_node
                if current == self.head:
                    self.head = next_node
                current = next_node
            else:
                previous = current
                current = next_node
            if current == self.head or not self.head:
                break
    
    def delete_by_sim(self, sim_target: str) -> None:
        if not self.head:
            return
        current: ListNode = self.head
        previous: 'ListNode' = self.find_tail() # type: ignore
        while True:
            next_node: Optional['ListNode'] = current.next
            if next_node is None:
                break
            if current.record.passport_num == sim_target:
                if current == current.next:
                    self.head = None
                    break 
                previous.next = next_node
                if current == self.head:
                    self.head = next_node
                current = next_node
            else:
                previous = current
                current = next_node
            if current == self.head or not self.head:
                break
    
    def insert(self, data: Record) -> None:
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current: ListNode = self.head
            while True:
                if current.next is None or current.next == self.head:
                    break
                current = current.next
            current.next = new_node
            new_node.next = self.head
