def command_help():
    print(f"")


def split_command(command_line: str) -> list:
    return command_line.split(" ")


def is_exit(command: str) -> bool:
    if command == "exit":
        return True
    else:
        return False


def is_valid_command(command_line: str) -> bool:
    command = split_command(command_line)
    if len(command) == 1:
        if command[0] == "help" or command[0] == "show":
            return True
    elif len(command) == 2:
        if command[0] == "read" or command[0] == "delete" or command[0] == "create":
            return True
    elif len(command) == 3:
        if command[0] == "write" or command[0] == "add":
            return True
    elif len(command) == 4:
        if command[0] == "change":
            return True
    else:
        print("Такой команды нет")
        return False


def write_command(user: str) -> None:
    exit_command = False
    while not exit_command:
        command_line = input()
        while not is_valid_command(command_line):
            command_line = input()
            if is_exit(command_line):
                return
        command = split_command(command_line)
        match command[0]:
            case "read":
                await read_file(user=user, object_name=command[1])
            case "write":
                await write_to_file(user=user, object_name=command[1], data=command[2])
            case "create":
                await create_object(user=user, object_name=command[1])
            case "add":
                await add_user(user=command[1], role=command[2])
            case "delete":
                await delete_object(user=user, object_name=command[1])
            case "grand":
                await grand_rights(user=user, target_user=command[1], object_name=command[2], rights=command[3])
            case "help":
                command_help()
            case "rights":
                await get_rights(user=user)
            case "exit":
                exit_command = True

