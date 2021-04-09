import io
import csv


def json2csv(records, firstrowdata):
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(firstrowdata)
    data = []
    for record in records:
        sub_data = []
        for data_name in firstrowdata:
            sub_data.append(record.get(data_name, " "))
        data.append(sub_data)
    cw.writerows(data)
    return si.getvalue().strip('\r\n')
