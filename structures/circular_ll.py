import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Record
from typing import Optional, List
from algorithms import counting_sort_records

class ListNode:
    def __init__(self, record: Record):
        self.record = record
        self.next: Optional['ListNode'] = None 


class CircularLinkedList:
    def __init__(self):
        self.head: Optional[ListNode] = None

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
        
    def delete_by_passport(self, passport_target: str) -> None:
        if not self.head:
            return
        size = 1
        temp = self.head
        while temp.next and temp.next != self.head:
            size += 1
            temp = temp.next
        current: ListNode = self.head
        previous: ListNode = temp
        for _ in range(size):
            next_node: Optional['ListNode'] = current.next
            assert next_node is not None
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

    def delete_by_sim(self, sim_target: str) -> None:
        if not self.head:
            return
        size = 1
        temp = self.head
        while temp.next and temp.next != self.head:
            size += 1
            temp = temp.next
        current: ListNode = self.head
        previous: ListNode = temp 
        for _ in range(size):
            next_node: Optional['ListNode'] = current.next
            assert next_node is not None
            if current.record.sim_num == sim_target:
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
            
    def sort(self) -> None:
        """Сортирует список и перестраивает связи."""
        if self.head is None or self.head.next == self.head:
            return
        records: List[Record] = []
        current: ListNode = self.head
        assert current is not None
        while True:
            records.append(current.record)
            if current.next is None or current.next == self.head:
                break
            current = current.next
        sorted_records = counting_sort_records(records)
        self.head = ListNode(sorted_records[0])
        current = self.head
        for i in range(1, len(sorted_records)):
            new_node = ListNode(sorted_records[i])
            current.next = new_node
            current = new_node
        current.next = self.head

    def get_all(self) -> List[Record]:
        """Возвращает все записи в виде обычного списка."""
        ans: List[Record] = []
        if not self.head:
            return ans
        current: ListNode = self.head
        while True:
            ans.append(current.record)
            if current.next is None or current.next == self.head:
                break
            current = current.next
        return ans
