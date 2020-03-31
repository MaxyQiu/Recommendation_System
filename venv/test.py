import csv
def uniq_parks_counts(filename):
    parks_list = []
    with open(filename, newline='', encoding="ISO-8859-1") as f:
        data = csv.DictReader(f)
        for row in data:
            if row['Nom_parc'] != '':
                parks_list.append(row['Nom_parc'])

    parks_list.sort()
    unique_list = {}.fromkeys(parks_list).keys()

    csv_string = ""
    frequent={}
    for element in unique_list:
        num = parks_list.count(element)
        frequent[element]=num

    frequent = sorted(frequent.items(), key=lambda kv: kv[1])

    first_10=dict(list(frequent.item())[0:10])
    for k in first_10.keys():
        csv_string=csv_string+k+','+str(first_10[k])+"\n"
    return csv_string
    raise Exception("Not implemented yet")

print(uniq_parks_counts("/Users/maxyqiu/Desktop/IR&WebSearch/Research_Analysis_System/venv/frenepublicinjection2016.csv"))