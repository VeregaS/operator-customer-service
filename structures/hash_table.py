from models import SimCard
from typing import Optional, List


class HashEntry:
    def __init__(self, key: str, value: SimCard):
        self.key: str = key
        self.value: SimCard = value
        self.is_deleted: bool = False


class HashTable:
    def __init__(self, initial_capacity: int = 101):
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.table: List[Optional[HashEntry]] = [None] * self.capacity
        self.load_factor_threshold: float = 0.7

    def _hash(self, key: str) -> int:
        """
        Полиномиальная хеш-функция для строкового ключа.
        Дефисы игнорируются для повышения равномерности распределения.
        """
        hash_val = 0
        for char in key:
            if char != '-':
                hash_val = (hash_val * 31 + ord(char)) % self.capacity
        return hash_val

    def _resize(self) -> None:
        """Увеличение размера таблицы и перехеширование (Rehashing)."""
        old_table = self.table
        self.capacity = self.capacity * 2 + 1  
        self.table = [None] * self.capacity
        self.size = 0

        for entry in old_table:
            if entry is not None and not entry.is_deleted:
                self.insert(entry.value)


    def insert(self, sim_card: SimCard) -> bool:
        """
        Вставка новой SIM-карты. Разрешение коллизий линейным опробованием.
        Возвращает False, если ключ уже существует.
        """
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        key = sim_card.sim_num
        index = self._hash(key)
        first_deleted_index = -1
        while self.table[index] is not None:
            entry = self.table[index]
            assert entry is not None
            if entry.key == key:
                if entry.is_deleted:
                    entry.value = sim_card
                    entry.is_deleted = False
                    self.size += 1
                    return True
                else:
                    return False
            if entry.is_deleted and first_deleted_index == -1:
                first_deleted_index = index
            index = (index + 1) % self.capacity
        insert_index = first_deleted_index if first_deleted_index != -1 else index
        self.table[insert_index] = HashEntry(key, sim_card)
        self.size += 1
        return True

    def search(self, sim_number: str) -> Optional[SimCard]:
        """Точный поиск по номеру SIM-карты ($O(1)$ в среднем)."""
        index = self._hash(sim_number)
        while self.table[index] is not None:
            entry = self.table[index]
            assert entry is not None
            if entry.key == sim_number:
                if not entry.is_deleted:
                    return entry.value
                else:
                    return None
            index = (index + 1) % self.capacity
        return None 

    def delete(self, sim_number: str) -> bool:
        """
        Удаление SIM-карты с использованием маркера (Tombstone).
        Возвращает True при успешном удалении, False если не найдено.
        """
        index = self._hash(sim_number)
        while self.table[index] is not None:
            entry = self.table[index]
            assert entry is not None
            if entry.key == sim_number and not entry.is_deleted:
                entry.is_deleted = True
                self.size -= 1
                return True
            index = (index + 1) % self.capacity
        return False

    def search_by_tariff(self, target_tariff: str) -> List[SimCard]:
        """
        Поиск по тарифу (п. 9.6.10).
        Выполняет линейный проход по всем бакетам таблицы.
        Временная сложность: $O(N)$.
        """
        results: List[SimCard] = []
        for entry in self.table:
            if entry is not None and not entry.is_deleted:
                if entry.value.tariff.lower() == target_tariff.lower():
                    results.append(entry.value)
        return results

    def get_all(self) -> List[SimCard]:
        """Просмотр всех имеющихся SIM-карт."""
        return [
            entry.value for entry in self.table 
            if entry is not None and not entry.is_deleted
        ]

    def clear(self) -> None:
        """Очистка данных о SIM-картах."""
        self.table = [None] * self.capacity
        self.size = 0
