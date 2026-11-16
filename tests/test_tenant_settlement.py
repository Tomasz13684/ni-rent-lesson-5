import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.manager import Manager
from src.models import Parameters, Apartment, Tenant, Bill, ApartmentSettlement


def test_tenant_settlements():
    parameters = Parameters()
    manager = Manager(parameters)

    # Scenariusz 1: Mieszkanie z 3 najemcami 
    apart_settlement_3 = ApartmentSettlement(
        apartment='apart-polanka',
        month=10,
        year=2024,
        total_rent_pln=4200.0,
        total_bills_pln=600.0,
        total_due_pln=4800.0
    )

    settlements_3 = manager.get_tenant_settlements(apart_settlement_3)

    # Asercje
    assert len(settlements_3) == 3                                 
    assert settlements_3[0].bills_pln == 200.0                         
    assert settlements_3[1].bills_pln == 200.0                         
    assert settlements_3[2].bills_pln == 200.0                         
    assert settlements_3[0].total_due_pln == settlements_3[0].rent_pln + 200.0  
    assert settlements_3[1].total_due_pln == settlements_3[1].rent_pln + 200.0  
    assert settlements_3[2].total_due_pln == settlements_3[2].rent_pln + 200.0  

    # Scenariusz 2: Mieszkanie z tylko 1 najemcą
    manager.apartments['apart-single'] = Apartment(
        key='apart-single',
        name='Mieszkanie Jednoosobowe',
        location='Centrum',
        area_m2=30.0,
        rooms={}
    )
    manager.tenants['tenant-single'] = Tenant(
        name='Piotr Jedynak',
        apartment='apart-single',
        room='room-1',
        rent_pln=2000.0,
        deposit_pln=2000.0,
        date_agreement_from='2024-01-01',
        date_agreement_to='2024-12-31'
    )

    apart_settlement_1 = ApartmentSettlement(
        apartment='apart-single',
        month=10,
        year=2024,
        total_rent_pln=2000.0,
        total_bills_pln=350.0,
        total_due_pln=2350.0
    )

    settlements_1 = manager.get_tenant_settlements(apart_settlement_1)

    # Asercje dla 1 najemc
    assert len(settlements_1) == 1                                     
    assert settlements_1[0].bills_pln == 350.0                         
    assert settlements_1[0].total_due_pln == 2350.0                    
    assert settlements_1[0].tenant == 'Piotr Jedynak'                  

    # Scenariusz 3: Mieszkanie bez żadnych najemców
    manager.apartments['apart-puste'] = Apartment(
        key='apart-puste',
        name='Puste Mieszkanie',
        location='Górczyn',
        area_m2=40.0,
        rooms={}
    )

    apart_settlement_empty = ApartmentSettlement(
        apartment='apart-puste',
        month=10,
        year=2024,
        total_rent_pln=0.0,
        total_bills_pln=500.0,
        total_due_pln=500.0
    )

    settlements_empty = manager.get_tenant_settlements(apart_settlement_empty)

    # Asercje dla braku najemców
    assert len(settlements_empty) == 0                                 
    assert settlements_empty == []                                     


if __name__ == '__main__':
    test_tenant_settlements()
    print("Wszystkie asercje przeszły pomyślnie!")
