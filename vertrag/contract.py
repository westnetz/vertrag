import datetime
import locale
import os
import os.path
import yaml

from .config import get_config
from .settings import ASSETS_DIR
from .helpers import (
    generate_pdf,
    get_pdf,
    get_template,
    generate_email_with_pdf_attachment,
    send_email,
)
from .storage import (
    OrdersStore,
    AssetsStore,
    ContractsStore,
    TemplatesStore,
    PositionsStore
)

class NoDataLoaded(Exception):
    pass

class Positions:

    def __init__(self, positions_store):
        self.ps = positions_store

    def from_cid(self, cid):
        self.cid = cid
        self._data = self.ps[cid]

    def add_unbilled(self):
        pass

    def get_unbilled(self):
        pass

    def get_billed(self):
        pass

    def bill(self, positions_id, invoice_id, date):
        pass

    def save(self):
        self.ps[cid] = self._data

class Contract:

    def __init__(self, orders_store, contracts_store, positions_store):
        self.os = orders_store
        self.cs = contracts_store
        self.ps = positions_store
        self._data = {}

    @property
    def cid(self):
        if not self._data:
            raise NoDataLoaded("No contract or order loaded.")
        return self._data['connection']['cid']

    @property
    def _customer(self):
        return self._data['customer']

    @property
    def _connection(self):
        return self._data['connection']

    @property
    def _contact_information(self):
        return self._data['contact_information']

    def from_order(self, order_id):
        self.order_id = order_id
        self._data = self.os[self.order_id]
        return self

    def from_contract_file(self, contract_id):
        self.contract_id = contract_id
        pass

    def to_yaml(self):
        self.cs[self.cid] = self._data
        positions = [
            {
                'description': self._connection['product'],
                'price': float(self._connection['price_monthly']) / 1.19,
                'quantity': 1
            },
            {
                'description': "Anschlussgebühr " + self._connection['product'],
                'price': float(self._connection['price_initial']) / 1.19,
                'quantity': 1
            },

        ]
        self.ps[self.cid] = positions
        return self

    def to_pdf(self):
        raise NotImplementedError

class DocumentFactory:

    def __init__(self, config, cwd):
        self.config = config
        self.cwd = cwd

class ContractFactory(DocumentFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.os = OrdersStore(getattr(self.config, OrdersStore.key), self.cwd)
        self.cs = ContractsStore(getattr(self.config, ContractsStore.key), self.cwd)
        self.ps = PositionsStore(getattr(self.config, PositionsStore.key), self.cwd)

    def from_order(self, order_id):
        return Contract(
                    orders_store = self.os,
                    contracts_store = self.cs,
                    positions_store = self.ps,
               ).from_order(order_id)

    def from_contract(self, contract_id):
        return Contract(
                    order_store = self.os,
                    contracts_store = self.cs,
                    positions_store = self.ps,
               ).from_contract(contract_id)

def render_pdf_invoices(directory, template, config):

    logo_path = os.path.join(directory, ASSETS_DIR, "logo.png")

    for customer_invoice_dir, filename in iterate_invoices(config.invoices_dir):
        if not os.path.isfile("{}.pdf".format(os.path.join(customer_invoice_dir,
            filename[:-5]))):
            with open(os.path.join(customer_invoice_dir, filename)) as yaml_file:
                invoice_data, invoice_positions = yaml.load(
                    yaml_file.read(), Loader=yaml.FullLoader
                )
            invoice_data["logo_path"] = logo_path

            print("Rendering invoice pdf for {}".format(invoice_data["id"]))

            # Format data for printing
            for element in ["total_netto", "total_brutto", "total_ust"]:
                invoice_data[element] = locale.format_string(
                    "%.2f", invoice_data[element]
                )
            for position in invoice_positions:
                for key in ["price", "subtotal"]:
                    position[key] = locale.format_string("%.2f", position[key])

            invoice_html = template.render(
                positions=invoice_positions, invoice=invoice_data
            )

            invoice_pdf_filename = os.path.join(
                customer_invoice_dir, "{}.pdf".format(invoice_data["id"])
            )
            generate_pdf(
                invoice_html, config.invoice_css_filename, invoice_pdf_filename
            )


def send_invoice_mails(config, mail_template, year_suffix):

    for d in os.listdir(config.invoices_dir):
        customer_invoice_dir = os.path.join(config.invoices_dir, d)
        if os.path.isdir(customer_invoice_dir):
            for filename in os.listdir(customer_invoice_dir):

                if not filename.endswith(".yaml"):
                    continue

                file_suffix = ".".join(filename.split(".")[-3:-1])

                if file_suffix != year_suffix:
                    continue

                with open(os.path.join(customer_invoice_dir, filename)) as yaml_file:
                    invoice_data, invoice_positions = yaml.load(
                        yaml_file, Loader=yaml.FullLoader
                    )

                if invoice_data["email"] is None:
                    continue

                invoice_pdf_path = os.path.join(
                    customer_invoice_dir, "{}.pdf".format(filename[:-5])
                )
                invoice_pdf_filename = "Westnetz_Rechnung_{}.pdf".format(filename[:-5])
                invoice_mail_text = mail_template.render(invoice=invoice_data)
                invoice_pdf = get_pdf(invoice_pdf_path)

                invoice_receiver = invoice_data["email"]

                invoice_email = generate_email_with_pdf_attachment(
                    invoice_receiver,
                    config.sender,
                    config.invoice_mail_subject,
                    invoice_mail_text,
                    invoice_pdf,
                    invoice_pdf_filename,
                )

                print("Sending invoice {}".format(invoice_data["id"]))

                send_email(
                    invoice_email,
                    config.server,
                    config.username,
                    config.password,
                    config.insecure,
                )

def render_contract(directory):
    config = get_config(directory)
    template = get_template(config.invoice_template_filename)
    render_pdf_invoices(directory, template, config)


def send_contract(directory, year_suffix):
    config = get_config(directory)
    mail_template = get_template(config.invoice_mail_template_filename)
    send_invoice_mails(config, mail_template, year_suffix)
