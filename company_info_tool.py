class CompanyInfoTool:

    def get_customer(self):
        return "Customer: Ram Kishore"

    def get_invoice(self):
        return "Invoice Number: INV-1025"

    def get_product(self):
        return "Product: Laptop"

    def get_leave_policy(self):
        return "Employees can apply for leave according to the company leave policy."


if __name__ == "__main__":

    company = CompanyInfoTool()

    print(company.get_customer())
    print(company.get_invoice())
    print(company.get_product())
    print(company.get_leave_policy())
