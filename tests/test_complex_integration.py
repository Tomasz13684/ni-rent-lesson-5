import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
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

    # Mieszkanie istnieje i ma rachunek w danym miesiącu -> poprawna suma
    assert manager.get_apartment_costs('apart-polanka', 2024, 11) == 450.0

    # Mieszkanie istnieje a rachunki z pliku -> poprawna suma
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0

    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0


def test_get_apartment_costs_invalid_month():
    manager = Manager(Parameters())

    with pytest.raises(ValueError):
        manager.get_apartment_costs('apart-polanka', 2024, 13)

    with pytest.raises(ValueError):
        manager.get_apartment_costs('apart-polanka', 2024, 0)


if __name__ == '__main__':
    test_get_apartment_costs()
    test_apartment_costs_with_optional_parameters()
    test_get_apartment_costs_invalid_month()
    print("Wszystkie asercje przeszły pomyślnie!")