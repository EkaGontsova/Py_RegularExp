import re
import csv
from pprint import pprint


def format_name(contacts_list):
    for person in contacts_list:
        if len(person[0].split()) == 3:
            surname = person[0].split()
            person[0], person[1], person[2] = person[0].split()[0], surname[1], surname[2]
        if len(person[1].split()) == 2:
            name = person[1].split()
            person[1], person[2] = name[0], name[1]
        if len(person[0].split()) == 2:
            surname = person[0].split()
            person[0], person[1] = person[0].split()[0], surname[1]

    return contacts_list


def get_numbers(contacts_list):
    pattern = r"(\+7|8)?\s?\(?(\d{3}?)\)?[-\s]?(\d{3})[-\s]?(\d{2})-?(\d{2})(\s?)\(?([доб.]{4})?\s?(\d{4})?\)?"
    sub = r"+7(\2)\3-\4-\5\6\7\8"
    for person in contacts_list:
        person[5] = re.sub(pattern, sub, person[5])

    return contacts_list


def merge_contacts(contacts_list):
    for person in contacts_list:
        for other_person in contacts_list:
            if person[0] in other_person[0]:
                for i in range(7):
                    if person[i] == '':
                        person[i] = other_person[i]

    merged_contacts = []
    for person in contacts_list:
        if len(person) != 7:
            del person[7:]
        if person not in merged_contacts:
            merged_contacts.append(person)

    return merged_contacts


if __name__ == "__main__":
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

        format_name(contacts_list)
        get_numbers(contacts_list)
        merged_contacts = merge_contacts(contacts_list)
        pprint(merged_contacts)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(merged_contacts)
