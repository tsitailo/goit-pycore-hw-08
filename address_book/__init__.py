"""
Address Book Module - система управління адресною книгою.

Цей модуль надає класи для роботи з адресною книгою,
включаючи управління контактами та їх телефонами.
"""

from .address_book import AddressBook
from .field import Field
from .name import Name
from .phone import Phone
from .record import Record
from .birthday import Birthday

__all__ = ['Field', 'Name', 'Phone', 'Record', 'AddressBook', 'Birthday']
__version__ = '1.0.0'
