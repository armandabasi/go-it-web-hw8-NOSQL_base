from models import Authors, Quotes
import connect


def parser_command(commands_):
    return commands_.strip().split(":")


def handler_command(command_, data_):
    match command_:
        case "name":
            find_author(data_.strip())
        case "tag":
            find_tag(data_.strip())
        case "tags":
            find_tags(data_.strip())
        case _:
            print("I don't know what you mean. Try again.")


def find_author(data_):
    authors = Authors.objects(fullname__icontains=data_)
    if authors:
        for author in authors:
            print(f"{author.fullname}:")
            for q in Quotes.objects.filter(author=author):
                print(q.quote)
    else:
        print(f"{data_} not found")


def find_tag(data_):
    values_ = Quotes.objects(tags__icontains=data_)
    if values_:
        for tag in values_:
            tags = []
            for _ in tag.tags:
                if data_ in _:
                    tags.append(_)
            print(f"tag: {tags}:  {tag.quote}:")
    else:
        print(f"{data_} not found")


def find_tags(data_):
    values_ = data_.strip().split(",")
    for value in values_:
        find_tag(value.strip())


if __name__ == '__main__':
    while True:
        commands = input("Enter the command: ")
        if commands == "exit":
            print("Bye!")
            break
        else:
            try:
                command, data = parser_command(commands)
                handler_command(command, data)
            except ValueError as err:
                print(err)
