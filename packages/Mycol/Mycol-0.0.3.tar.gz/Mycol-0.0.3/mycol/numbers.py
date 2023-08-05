import typing

def add_one_to(number, print_result: typing.Optional[bool] = False) -> None:
    result = number + 1

    if print_result:
        print(result)

    return result

def check_equation() -> None:
    raise NotImplementedError("Method is work in progress")

add_one_to(6)