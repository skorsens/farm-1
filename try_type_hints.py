def print_name_x_times(name: str, times: int) -> None:
    for _ in range(times):
        print(name)


print_name_x_times("name", 3)


def square_numbers(lNumbers: list[int]) -> list[int]:
    return list(map(lambda x: x**2, lNumbers))


assert square_numbers([1, 2, 3]) == [1, 4, 9]

from typing import Literal

literal_var_str: Literal["v1", "v2"] = "v2"
literal_var_str = "v2"
literal_var_int: Literal[1, 2] = 2
literal_var_int = 1
