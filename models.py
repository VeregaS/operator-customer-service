from dataclasses import dataclass

@dataclass(frozen=True)
class Client:
    passport_num: str   # Формат: NNNN-NNNNNN
    passport_give: str
    full_name: str
    year_of_birth: int
    address: str
    

@dataclass
class SimCard:
    sim_num: str    # Формат: NNN-NNNNNNN
    tariff: str
    year_start: int
    is_available: bool
    
@dataclass
class Record:
    passport_num: str   # Формат: NNNN-NNNNNN
    sim_num: str    # Формат: NNN-NNNNNNN
    date_start: str
    date_end: str
