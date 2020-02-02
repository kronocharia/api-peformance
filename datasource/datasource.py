import copy
import csv
import os
from math import floor
from random import randint

from prodict import Prodict

dirname = os.path.dirname(os.path.abspath(__file__))


def get_file_path(filename: str) -> str:
    file_path = os.path.join(dirname, filename)
    return file_path


def get_input_file_path() -> str:
    return get_file_path("input.csv")


def create_dummy_csv():
    output = []

    for i in range(10):
        lower: int = (i + 1) * 100
        upper: int = (i + 2) * 100

        output.append({"x": i, "y": randint(lower, upper)})
        field_names = ["x", "y"]

        # output.append({"a": i, "b": (i + 1) + 10, "c": "helloooo"})
        # field_names = ["a", "b", "c"]

        with open('temp_out.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writerows(output)


def generate_base_duration(seed: int) -> int:
    return (seed + 1) * 100


def generate_random_duration(seed: int) -> int:
    duration = generate_base_duration(seed) + randint(1, 100)
    return add_outlier_chance_to_duration(duration)


def add_outlier_chance_to_duration(duration: int) -> int:
    final_duration = copy.deepcopy(duration)
    if randint(1, 100) > 75:
        random_offset = randint(300, 400)
        if randint(1, 10) > 5:
            final_duration + random_offset
        else:
            final_duration - random_offset

    return final_duration


def generate_random_duration_with_api_improvements(seed: int, improvement_min, improvement_max) -> int:
    duration = (generate_base_duration(seed) * 0.7) + randint(1, 100)

    # simulate api optimisations that have generally made things faster
    if randint(1, 10) > 3:
        duration - randint(improvement_min, improvement_max)
    else:
        duration + randint(improvement_min, improvement_max)

    return add_outlier_chance_to_duration(duration)


def generator_api_improvements(seed: int):
    # return generate_random_duration_with_api_improvements(seed, floor(seed / 10), floor(seed / 4))
    return generate_random_duration_with_api_improvements(seed, 200, 300)


class ApiProfile(Prodict):
    ticketCount: str
    desiredAccounts: str


class ApiResult(Prodict):
    ticketcount: str
    duration: str


def create_dummy_api_csv_with_generator(generation_fn):
    profile: [ApiProfile] = []

    output = []

    reader = csv.DictReader(open(get_file_path("profile.csv")))
    with open(get_file_path('profile.csv')) as filein:
        reader = csv.DictReader(filein)
        for row in reader:
            tc = row["ticketCount"]
            da = row["desiredAccounts"]
            profile.append(ApiProfile(ticketCount=tc, desiredAccounts=da))

    for profile_entry in profile:  # type ApiProfile
        field_names = ApiResult

        profile_index = profile_entry.ticketCount

        for i in range(int(profile_entry.desiredAccounts)):
            output.append(ApiResult(ticketcount=profile_index,
                                    duration=generation_fn(int(profile_index))))

        with open(get_file_path('temp_out.csv'), 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=ApiResult.attr_names())
            writer.writerows(output)

    return output


def write_to_csv(output: [], filename: str, fieldnames: [str]):
    with open(get_file_path(filename+".csv"), "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output)


def create_dummy_api_csv():
    return create_dummy_api_csv_with_generator(generate_random_duration)


def create_dummy_api_improvement_csv():
    return create_dummy_api_csv_with_generator(generator_api_improvements)


if __name__ == '__main__':
    # create_dummy_csv()
    # create_dummy_api_csv()
    create_dummy_api_improvement_csv()
