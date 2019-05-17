import os.path

CONFIG_FILENAME = "vertrag.config.yaml"
ORDERS_DIR = "orders"
CONTRACTS_DIR = "contracts"
CUSTOMERS_DIR = "customers"
POSITIONS_DIR = "positions"
TEMPLATES_DIR = "templates"
ASSETS_DIR = "assets"
DIRECTORIES = [ORDERS_DIR, CONTRACTS_DIR, CUSTOMERS_DIR, POSITIONS_DIR, TEMPLATES_DIR, ASSETS_DIR]
CONTRACT_TEMPLATE_FILENAME = os.path.join(TEMPLATES_DIR, "contract_template.j2.html")
CONTRACT_CSS_FILENAME = os.path.join(ASSETS_DIR, "contract.css")
CONTRACT_MAIL_TEMPLATE_FILENAME = os.path.join(TEMPLATES_DIR, "contract_mail_template.j2")
