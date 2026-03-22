import json
import os
from dataclasses import asdict
from typing import List, Tuple, Optional
from models import Client, SimCard, Record
from structures.avl_tree import AVLTree
from structures.hash_table import HashTable
from structures.circular_ll import CircularLinkedList
from algorithms import naive_string_search

class CellularOperatorSystem:
    def __init__(self):
        self.clients = AVLTree()
        self.sim_cards = HashTable()
        self.records = CircularLinkedList()

    # ==========================================
    # 1. УПРАВЛЕНИЕ КЛИЕНТАМИ
    # ==========================================

    def register_client(self, client: Client) -> Tuple[bool, str]:
        if self.clients.search(client.passport_num):
            return False, "Клиент с таким паспортом уже зарегистрирован."
        self.clients.insert(client)
        return True, "Клиент успешно зарегистрирован."

    def remove_client(self, passport_num: str) -> Tuple[bool, str]:
        client = self.clients.search(passport_num)
        if not client:
            return False, "Клиент не найден."

        client_records = self.records.search_by_passport(passport_num)
        for record in client_records:
            if not record.date_end:
                return False, "Удаление заблокировано: у клиента есть невозвращенные SIM-карты."

        self.clients.delete(passport_num)
        self.records.delete_by_passport(passport_num)
        return True, "Клиент и его история успешно удалены."

    def get_all_clients(self) -> List[Client]:
        return self.clients.pre_order_search(lambda c: True)

    def clear_clients(self) -> None:
        self.clients.clear()

    def search_client_exact(self, passport_num: str) -> Tuple[Optional[Client], List[str]]:
        client = self.clients.search(passport_num)
        if not client:
            return None, []
        
        client_records = self.records.search_by_passport(passport_num)
        active_sims = [rec.sim_num for rec in client_records if not rec.date_end]
        return client, active_sims

    def search_client_partial(self, fragment: str) -> List[Client]:
        def match_func(client: Client) -> bool:
            return (naive_string_search(client.full_name, fragment) or 
                    naive_string_search(client.address, fragment))
        return self.clients.pre_order_search(match_func)

    # ==========================================
    # 2. УПРАВЛЕНИЕ SIM-КАРТАМИ
    # ==========================================

    def add_sim(self, sim: SimCard) -> Tuple[bool, str]:
        success = self.sim_cards.insert(sim)
        if not success:
            return False, "SIM-карта с таким номером уже существует."
        return True, "SIM-карта успешно добавлена."

    def remove_sim(self, sim_num: str) -> Tuple[bool, str]:
        sim = self.sim_cards.search(sim_num)
        if not sim:
            return False, "SIM-карта не найдена."
        if not sim.is_available:
            return False, "Удаление заблокировано: SIM-карта выдана клиенту."

        self.sim_cards.delete(sim_num)
        self.records.delete_by_sim(sim_num)
        return True, "SIM-карта и её история успешно удалены."

    def get_all_sims(self) -> List[SimCard]:
        return self.sim_cards.get_all()

    def clear_sims(self) -> None:
        self.sim_cards.clear()

    def search_sim_exact(self, sim_num: str) -> Tuple[Optional[SimCard], Optional[Client]]:
        sim = self.sim_cards.search(sim_num)
        if not sim:
            return None, None
        
        owner: Optional[Client] = None
        if not sim.is_available:
            sim_records = self.records.search_by_sim(sim_num)
            for rec in sim_records:
                if not rec.date_end:
                    owner = self.clients.search(rec.passport_num)
                    break
                    
        return sim, owner

    def search_sim_by_tariff(self, tariff: str) -> List[SimCard]:
        return self.sim_cards.search_by_tariff(tariff)

    # ==========================================
    # 3. УПРАВЛЕНИЕ ОПЕРАЦИЯМИ
    # ==========================================

    def issue_sim(self, passport_num: str, sim_num: str, date_start: str) -> Tuple[bool, str]:
        client = self.clients.search(passport_num)
        if not client:
            return False, "Клиент не найден."

        sim = self.sim_cards.search(sim_num)
        if not sim:
            return False, "SIM-карта не найдена."
        if not sim.is_available:
            return False, "SIM-карта недоступна (уже выдана)."

        sim.is_available = False
        new_record = Record(passport_num=passport_num, sim_num=sim_num, date_start=date_start, date_end="")
        self.records.insert(new_record)
        
        self.records.sort()
        
        return True, "SIM-карта успешно выдана."

    def return_sim(self, sim_num: str, date_end: str) -> Tuple[bool, str]:
        sim = self.sim_cards.search(sim_num)
        if not sim:
            return False, "SIM-карта не найдена."
        if sim.is_available:
            return False, "SIM-карта числится у оператора (не выдана)."

        sim_records = self.records.search_by_sim(sim_num)
        active_record = None
        for rec in sim_records:
            if not rec.date_end:
                active_record = rec
                break
                
        if not active_record:
            return False, "Критическая ошибка: запись о выдаче не найдена."

        active_record.date_end = date_end
        sim.is_available = True
        return True, "SIM-карта успешно возвращена."

    # ==========================================
    # 4. СОХРАНЕНИЕ И ЗАГРУЗКА ДАННЫХ (JSON)
    # ==========================================

    def save_data(self, directory: str = "data") -> None:
        """Сохранение всех данных в JSON файлы."""
        os.makedirs(directory, exist_ok=True)
        clients_data = [asdict(c) for c in self.get_all_clients()]
        with open(os.path.join(directory, "clients.json"), "w", encoding="utf-8") as f:
            json.dump(clients_data, f, ensure_ascii=False, indent=4)
        sims_data = [asdict(s) for s in self.get_all_sims()]
        with open(os.path.join(directory, "sims.json"), "w", encoding="utf-8") as f:
            json.dump(sims_data, f, ensure_ascii=False, indent=4)
        records_data = [asdict(r) for r in self.records.get_all()]
        with open(os.path.join(directory, "records.json"), "w", encoding="utf-8") as f:
            json.dump(records_data, f, ensure_ascii=False, indent=4)

    def load_data(self, directory: str = "data") -> None:
        """Загрузка данных из JSON файлов и восстановление структур."""
        clients_path = os.path.join(directory, "clients.json")
        if os.path.exists(clients_path):
            with open(clients_path, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    self.clients.insert(Client(**item))
        sims_path = os.path.join(directory, "sims.json")
        if os.path.exists(sims_path):
            with open(sims_path, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    self.sim_cards.insert(SimCard(**item))
        records_path = os.path.join(directory, "records.json")
        if os.path.exists(records_path):
            with open(records_path, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    self.records.insert(Record(**item))
            self.records.sort()
