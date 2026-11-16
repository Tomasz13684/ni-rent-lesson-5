import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.manager import Manager
from src.models import Parameters, Bill


def test_get_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)

    # Przykładowy rachunek
    manager.bills.append(
        Bill(
            apartment='apart-polanka',
            date_due='2024-11-15',
            settlement_year=2024,
            settlement_month=11,
            amount_pln=450.0,
            type='electricity'
        )
    )

    # Mieszkanie nie istnieje -> zwraca None
    assert manager.get_apartment_costs('nieistniejace-mieszkanie', 2024, 11) is None

    # Mieszkanie istnieje, ale nie ma rachunków w tym miesiącu -> zwraca 0.0
    assert manager.get_apartment_costs('apart-polanka', 2024, 5) == 0.0

    #. Mieszkanie istnieje i ma rachunek w danym miesiącu -> poprawna suma
    assert manager.get_apartment_costs('apart-polanka', 2024, 11) == 450.0

    # Mieszkanie istnieje a rachunki z pliku -> poprawna suma
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0


if __name__ == '__main__':
    test_get_apartment_costs()
    print("Wszystkie asercje przeszły pomyślnie!")

