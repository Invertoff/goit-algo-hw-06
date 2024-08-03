from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format. It must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return bool(re.match(r'^\d{10}$', value))


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        phone_to_edit = self.find_phone(old_phone_number)
        if phone_to_edit:
            self.remove_phone(old_phone_number)
            self.add_phone(new_phone_number)
        else:
            raise ValueError("Phone number not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())


def input_with_validation(prompt, validation_func, error_message):
    while True:
        value = input(prompt).strip()
        try:
            validation_func(value)
            return value
        except ValueError as e:
            print(f"{error_message}: {e}")


def validate_name(name):
    if not name:
        raise ValueError("Name cannot be empty.")


def validate_phone(phone):
    if not re.match(r'^\d{10}$', phone):
        raise ValueError("Phone number must be exactly 10 digits.")


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command (add, search, delete, add_phone, remove_phone, edit_phone, exit): ").strip().lower()

        if command == 'add':
            name = input_with_validation("Enter name: ", validate_name, "Invalid name")
            phone = input_with_validation("Enter phone: ", validate_phone, "Invalid phone number")
            record = Record(name)
            record.add_phone(phone)
            address_book.add_record(record)
            print(f"Added contact {name} with phone {phone}")

        elif command == 'search':
            name = input_with_validation("Enter name to search: ", validate_name, "Invalid name")
            record = address_book.find(name)
            if record:
                print(record)
            else:
                print(f"Contact {name} not found")

        elif command == 'delete':
            name = input_with_validation("Enter name to delete: ", validate_name, "Invalid name")
            try:
                address_book.delete(name)
                print(f"Deleted contact {name}")
            except KeyError as e:
                print(e)

        elif command == 'add_phone':
            name = input_with_validation("Enter name: ", validate_name, "Invalid name")
            phone = input_with_validation("Enter phone to add: ", validate_phone, "Invalid phone number")
            record = address_book.find(name)
            if record:
                record.add_phone(phone)
                print(f"Added phone {phone} to contact {name}")
            else:
                print(f"Contact {name} not found")

        elif command == 'remove_phone':
            name = input_with_validation("Enter name: ", validate_name, "Invalid name")
            phone = input_with_validation("Enter phone to remove: ", validate_phone, "Invalid phone number")
            record = address_book.find(name)
            if record:
                try:
                    record.remove_phone(phone)
                    print(f"Removed phone {phone} from contact {name}")
                except ValueError as e:
                    print(e)
            else:
                print(f"Contact {name} not found")

        elif command == 'edit_phone':
            name = input_with_validation("Enter name: ", validate_name, "Invalid name")
            old_phone = input_with_validation("Enter old phone: ", validate_phone, "Invalid phone number")
            new_phone = input_with_validation("Enter new phone: ", validate_phone, "Invalid phone number")
            record = address_book.find(name)
            if record:
                try:
                    record.edit_phone(old_phone, new_phone)
                    print(f"Edited phone from {old_phone} to {new_phone} for contact {name}")
                except ValueError as e:
                    print(e)
            else:
                print(f"Contact {name} not found")

        elif command == 'exit':
            print("Exiting program.")
            break

        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
