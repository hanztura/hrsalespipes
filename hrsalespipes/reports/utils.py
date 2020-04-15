import datetime
import uuid
import xlwt

from django.db.models import Sum, Q

from contacts.models import Employee
from system.models import Setting


def filter_queryset_by_employee(
        queryset,
        user,
        model,
        filter_expression=None,
        empty_if_no_filter=False,
        all_permission='salespipes.view_all_pipelines'):

    if not user.has_perm(all_permission):
        employee = getattr(user, 'as_employee', None)
        if employee:
            if not filter_expression:
                if empty_if_no_filter:
                    queryset = model.objects.none()
                else:
                    queryset = queryset.filter(
                        Q(job_candidate__consultant_id=employee.pk) |
                        Q(job_candidate__associate_id=employee.pk))
            else:
                queryset = queryset.filter(filter_expression)
        else:
            # return empty queryset
            queryset = model.objects.none()

    return queryset


def generate_excel(
        heading_title,
        date_from,
        date_to,
        columns,
        model,
        select_related,
        values_list,
        aggregate_fields=None,
        total_label_position=None,
        employee_id=None,
        is_month_filter=False,
        consultant_id=None,
        job_status_pk='',
        user=None,
        filter_expression=None,
        empty_if_no_filter=False,
        is_datetime=False,
        queryset=None,
        date_filter_expression=None):
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
    contact_type = None
    contact_id = None
    if employee_id:
        contact_type = 'Employee'
        contact_id = employee_id

    if consultant_id:
        contact_type = 'Consultant'
        contact_id = consultant_id

    if contact_type:
        contact = Employee.objects.filter(id=contact_id)
        if contact.exists():
            contact = contact.first()
            heading.insert(2, contact.name)
        else:
            heading.insert(2, '')

    # write header
    for head in heading:
        ws.write(row_num, 0, head, font_style)
        row_num += 1
    row_num += 1  # blank row

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    if queryset:
        rows = queryset.select_related(*select_related)
    else:
        rows = model.objects.all().select_related(*select_related)
    # filter rows by user employee
    if user:
        rows = filter_queryset_by_employee(
            rows, user, model, filter_expression, empty_if_no_filter)

    if date_from and date_to:
        try:
            # filter job status
            if job_status_pk:
                rows = rows.filter(
                    status_id=job_status_pk)

            data = rows

            if date_from == 'ALL' and date_to == 'ALL':
                pass
            else:
                # filter date
                if is_month_filter:
                    year, month = date_from.split('-')
                    if not date_filter_expression:
                        date_filter_expression = Q(
                            date__month=month,
                            date__year=year)
                    data = rows.filter(date_filter_expression)
                else:  # two dates
                    if is_datetime:
                        data = rows.filter(
                            date_time__gte=date_from, date_time__lte=date_to)
                    else:
                        if not date_filter_expression:
                            date_filter_expression = Q(
                                date__gte=date_from,
                                date__lte=date_to)
                        data = rows.filter(date_filter_expression)

            # filter contact
            if contact_id:
                if contact_type == 'Employee':
                    # used for aggreg.
                    data = data.filter(employee_id=contact_id)
                else:  # consultant
                    data = data.filter(job_candidate__consultant_id=contact_id)

            rows = data.values_list(*values_list)  # final value of rows
        except Exception as e:
            data = None
            rows = model.objects.none()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            val = row[col_num]
            if type(val) == uuid.UUID:
                val = str(val)

            if type(val) == datetime.datetime:
                val = val.replace(tzinfo=None)

            ws.write(row_num, col_num, val, font_style)

    # total row
    if aggregate_fields:
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


class EmployeeFilterMixin:
    """Filter results of Reports according to employee record.

    Return all if allowed to view all records
    """
    filter_expression = None
    empty_if_no_filter = False
    all_permission = 'salespipes.view_all_pipelines'

    def get_filter_expression(self):
        return self.filter_expression

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = filter_queryset_by_employee(
            queryset,
            self.request.user,
            self.model,
            self.get_filter_expression(),
            self.empty_if_no_filter,
            self.all_permission)

        return queryset
