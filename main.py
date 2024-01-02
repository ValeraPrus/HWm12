from classbook import AddressBook, Record
exit_list = ['good bye', 'close', 'exit']

command_list = '  Command list: \n-hello \
          \n-commands \n-add_name \
"enter name and birthday (optional)" \
    name and birthday=None (yyyy-mm-dd)\
          \n-add_phone "enter recorded name and new phone"\
    name and phone 1234567890\
          \n-show_all \n-birthday "enter recorded name"\
          \n-good bye \n-close \n-exit\
          \n-find_phone "enter recorded name" \
          \n-remove_phone "enter recorded name\
 and phone which you want to remove"\
          \n-delete "enter recorded name"\
          \n-search_contact ...'


phone_book = AddressBook()


def main():
    phone_book.load_book('testbook.bin')
    handlers = {
        'hello': hello_func,
        'commands': commands_func,
        'add': add_func,
        'add_name': add_func,
        'add_phone': add_phone_func,
        'find_phone': phone_func,
        'remove_phone': remove_phone_func,
        'edit_phone': edit_phone_func,
        'show_all': show_all_func,
        'birthday': birthday_func,
        'delete': delete_func,
        'search': search_func
               }

    while True:
        user = input('>>> ').lower()
        user_date = user.split(' ')
        command_handler = user_date.pop(0)
        if user in exit_list:
            print(exit_func())
            break
        elif command_handler in handlers:
            print(handlers[command_handler](user_date))
        else:
            print('- Wrong command')


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IndexError:
            return '- incorrect data (IndexError)'
        except KeyError:
            return '- incorrect data (KeyError)'
        except ValueError:
            return '- incorrect data (ValueError)'

    return inner


@input_error
def add_func(user_date):  # name and birthday=None (yyyy-mm-dd)
    if len(user_date) == 1:
        record = Record(user_date[0])
        phone_book.add_record(record)
    elif len(user_date) == 2:
        record = Record(user_date[0], user_date[1])
        phone_book.add_record(record)
    else:
        return '- Enter name and birthday'
    return f'- New contact "{user_date[0]}" added'


@input_error
def add_phone_func(user_date):  # name and phone
    record = phone_book.find(user_date[0])
    record.add_phone(user_date[1])
    return f"- Phone number {user_date[1]} for name {user_date[0]} added"


@input_error
def edit_phone_func(user_date):  # name, old_phone, new_phone
    record = phone_book.find(user_date[0])
    record.edit_phone(user_date[1], user_date[2])
    return f"- Phone number for {user_date[0]} changed"


@input_error
def phone_func(user_date):  # name
    record = phone_book.find(user_date[0])
    return str(record)


def exit_func():
    phone_book.save_book('testbook.bin')
    return '- Good bye!'


def show_all_func(arg):
    if not phone_book:
        return 'Empty'
    line = [str(record) for record in phone_book.data.values()]
    return "\n".join(line)


@input_error
def remove_phone_func(user_date):  # name and phone
    record = phone_book.find(user_date[0])
    record.remove_phone(user_date[1])
    return f"- Phone number {user_date[1]} for name {user_date[0]} removed"


@input_error
def birthday_func(user_date):  # name
    record = phone_book.find(user_date[0])
    to_birth = record.days_to_birthday()
    if to_birth:
        return f'- {record.birthday}\n- {to_birth} days to birthday'
    else:
        return '- Need date of birthday'


@input_error
def delete_func(user_date):  # name
    phone_book.delete(user_date[0])
    return f'{user_date[0]} phone number removed'


def search_func(user_date):  # search
    result = phone_book.search_contact(user_date[0])
    return f'{result}'


def commands_func(arg):
    return f'{command_list}'


def hello_func(arg):
    return '- How can I help you?'


if __name__ == '__main__':
    print(f'- Hello :)\n\n{command_list}')
    main()
