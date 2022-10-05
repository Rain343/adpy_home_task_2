import re
import csv
from pprint import pprint


if __name__ == '__main__':
    
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)


    new_contacts_list = [contacts_list[0]]

    for contact in contacts_list:
        main_pattern = r'([А-Я][а-я]+).([А-Я][а-я]+).([А-Я][а-я]+)?,+([А-Яа-я]+)?,+([А-Яа-яa-z\s–]+)?,+([\+0-9 ()-]+[ (доб.0-9)]+)?,+([\w.@]+)?'
        res = re.search(main_pattern, ",".join(contact))

        if res: 
            phone_pattern = r'(\+7|8)\s?\(?(\d{3})[)-]?\s?(\d{3})[ -]?(\d{2})[- ]?(\d{2})\s?(.?доб[. ]+(\d+).?)?'
            if 'доб' in str(res.group(6)):
                nice_phone = re.sub(phone_pattern, r'+7(\2)\3-\4-\5 доб.\7', str(res.group(6)))
            else:
                nice_phone = re.sub(phone_pattern, r'+7(\2)\3-\4-\5', str(res.group(6)))

            # объединяем значения
            for id, exist_contact in enumerate(new_contacts_list):
                if res.group(1) and res.group(2) in exist_contact:
                    
                    for val_id, val in enumerate(exist_contact):
                        if not val: exist_contact[val_id] = res.group(val_id+1)

                    new_contacts_list[id] = [exist_contact[0], exist_contact[1], exist_contact[2], 
                                            exist_contact[3], exist_contact[4], exist_contact[5], exist_contact[6]]
                    break
            else:
                new_contacts_list.append([res.group(1), res.group(2), res.group(3), res.group(4), res.group(5), nice_phone, res.group(7)])
                

    # pprint(new_contacts_list)

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(new_contacts_list)
