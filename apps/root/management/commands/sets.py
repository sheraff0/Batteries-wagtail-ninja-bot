from math import ceil


def select_option_input(options, subject="вариант"):
    def options_list(indexed_options):
        return '\n'.join([
            f"{i}) {option}" for i, option in indexed_options])

    indexed_options = [*enumerate(options, start=1)]
    indices = [str(i) for i, _ in indexed_options]
    selected = None
    while selected not in indices:
        selected = input(f"""
Выберите {subject}:
{options_list(indexed_options)}
[{'/'.join(indices)}]: """)
    return options[int(selected)-1]


def divide_columns(list_):
    left = ceil(len(list_) / 2)
    return [
        list_[:left],
        list_[left:]
    ]


def shift_or_append_to_head(item, list_):
    return [item, *filter(lambda x: x != item, list_)]
