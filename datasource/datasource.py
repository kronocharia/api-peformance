import csv
import os
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


def generate_random_duration(seed: int) -> int:
    base_duration = (seed + 1) * 100
    duration = base_duration + randint(1, 100)

    if randint(1, 100) > 75:
        duration + randint(300, 400)

    return duration


class ApiProfile(Prodict):
    ticketCount: str
    desiredAccounts: str


class ApiResult(Prodict):
    count: str
    duration: str


def create_dummy_api_csv():
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
            output.append(ApiResult(count=profile_index,
                                    duration=generate_random_duration(int(profile_index))))

        with open(get_file_path('temp_out.csv'), 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=ApiResult.attr_names())
            writer.writerows(output)

    return output


if __name__ == '__main__':
    # create_dummy_csv()
    create_dummy_api_csv()
