from src.models import Apartment, ApartmentSettlement, Bill, Parameters, Tenant, TenantSettlement, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    def get_apartment_costs(self, apartment_key, year=None, month=None):
        if month is not None and not (1 <= month <= 12):
            raise ValueError("Miesiąc musi być z zakresu od 1 do 12")

        if apartment_key not in self.apartments:
            return None

        total = 0.0
        for bill in self.bills:
            if bill.apartment == apartment_key:
                if year is None or bill.settlement_year == year:
                    if month is None or bill.settlement_month == month:
                        total += bill.amount_pln

        return total

    def get_apartment_settlement(self, apartment_key, year, month):
        if apartment_key not in self.apartments:
            return None

        bills_costs = self.get_apartment_costs(apartment_key, year, month)
        if bills_costs is None:
            return None

        tenants = [t for t in self.tenants.values() if t.apartment == apartment_key]
        total_rent = sum(t.rent_pln for t in tenants)

        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=total_rent,
            total_bills_pln=bills_costs,
            total_due_pln=total_rent + bills_costs
        )

    def get_tenant_settlements(self, apartment_settlement):
        apartment_tenants = [
            tenant for tenant in self.tenants.values()
            if tenant.apartment == apartment_settlement.apartment
        ]

        if not apartment_tenants:
            return []

        bills_per_tenant = apartment_settlement.total_bills_pln / len(apartment_tenants)

        settlements = []
        for tenant in apartment_tenants:
            total_due = tenant.rent_pln + bills_per_tenant
            settlements.append(
                TenantSettlement(
                    tenant=tenant.name,
                    apartment_settlement=apartment_settlement.apartment,
                    month=apartment_settlement.month,
                    year=apartment_settlement.year,
                    rent_pln=tenant.rent_pln,
                    bills_pln=bills_per_tenant,
                    total_due_pln=total_due,
                    balance_pln=-total_due
                )
            )

        return settlements

