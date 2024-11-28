from pprint import pprint

import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

def normalize_phone(phone):
  pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d+))?")
  formatted = pattern.sub(r"+7(\2)\3-\4-\5\6",phone)
  return formatted
contacts_dict = {}
for contact in contacts_list[1:]:
  fio = "".join(contact[:3]).split()
  last_name = fio[0]
  first_name = fio[1] if len(fio) > 1 else ""
  surname = fio[2] if len(fio) > 2 else ""

phone = normalize_phone(contact[5])
key = (last_name, first_name)

if key not in contacts_dict:
  contacts_dict[key] = {
    "last_name":last_name,
    "first_name":first_name,
    "surname":surname,
    "organization":contact[3],
    "position":contact[4],
    "phone":phone,
    "email": contact[6],
  }
else:
  existing = contacts_dict[key]
  existing["surname"] = existing["surname"] or surname
  existing["organization"] = existing["organization"] or contact[3]
  existing["position"] = existing["position"] or contact[4]
  existing["phone"] = existing["phone"] or phone
  existing["email"] = existing["email"] or contact[6]

updated_contact_list = [
  ["last_name", "first_name", "surname", "organization", "position", "phone", "email"]
]

for contact in contacts_dict.values():
  updated_contact_list.append([
    contact["last_name"],
    contact["first_name"],
    contact["surname"],
    contact["organization"],
    contact["position"],
    contact["phone"],
    contact["email"],
  ])

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(updated_contact_list)

pprint(updated_contact_list)