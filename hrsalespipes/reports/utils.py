import uuid
import xlwt

from django.db.models import Sum

from system.models import Setting


def generate_excel(heading_title, date_from, date_to, columns, model,
                   select_related, values_list, aggregate_fields,
                   total_label_position):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(heading_title)

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    heading = [
        heading_title,
        Setting.objects.first().company_name,
        'For the period {} to {}'.format(date_from, date_to)
    ]
    for head in heading:
        ws.write(row_num, 0, head, font_style)
        row_num += 1
    row_num += 1  # blank row

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = model.objects.all().select_related(*select_related)

    if date_from and date_to:
        try:
            data = rows.filter(date__gte=date_from, date__lte=date_to)
            rows = data.values_list(*values_list)
        except Exception as e:
            data = None
            rows = model.objects.none()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            val = row[col_num]
            if type(val) == uuid.UUID:
                val = str(val)

            ws.write(row_num, col_num, val, font_style)

    # total row
    row_num += 1
    if data:
        sum_aggregate_fields = []
        text_aggregate_fields = []
        for i, field in aggregate_fields:
            sum_aggregate_fields.append(Sum(field))

            text = '{}__sum'.format(field)
            text_aggregate_fields.append((i, text))

        sums = data.aggregate(*sum_aggregate_fields)
        ws.write(
            row_num,
            total_label_position,
            'TOTAL',
            font_style)

        for i, field in text_aggregate_fields:
            ws.write(
                row_num,
                i,
                sums[field],
                font_style)

    return wb
