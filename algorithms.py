from typing import List, Dict
from models import Record

def naive_string_search(text: str, pattern: str) -> bool:
    """Прямой поиск слова в тексте."""
    if not pattern:
        return True
    n = len(text)
    m = len(pattern)
    if m > n:
        return False
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j].lower() != pattern[j].lower():
                match = False
                break
        if match:
            return True
    return False

def counting_sort_records(records: List[Record]) -> List[Record]:
    """Сортировка подсчетом для записей по ключу sim_num."""
    if not records or len(records) == 1:
        return records
    unique_sims: List[str] = list(set(r.sim_num for r in records))
    unique_sims.sort()
    sim_to_index: Dict[str, int] = {sim: i for i, sim in enumerate(unique_sims)}
    k = len(unique_sims)
    count: List[int] = [0] * k
    output: List[Record] = [Record("", "", "", "")] * len(records)
    for r in records:
        idx = sim_to_index[r.sim_num]
        count[idx] += 1
    for i in range(1, k):
        count[i] += count[i - 1]
    for r in reversed(records):
        idx = sim_to_index[r.sim_num]
        pos = count[idx] - 1
        output[pos] = r
        count[idx] -= 1
    return output
