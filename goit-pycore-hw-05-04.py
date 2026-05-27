
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter user name."
        except IndexError:
            return "Enter the argument for the command."

    return inner

def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args

@input_error
def add_contact(args: list[str], contacts: dict) -> str:
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args: list[str], contacts: dict) -> str:
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args: list[str], contacts: dict) -> str:
    if not args:
        raise IndexError
    name = args[0]
    return contacts[name]

@input_error
def show_all(contacts: dict) -> str:
    if not contacts:
        return "No contacts saved yet."
    return "\n".join(f"{name}: {phone}" for name, phone in sorted(contacts.items()))

def main() -> None:
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ("close", "exit"):
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()