let fields = [

    {
      name: 'date',
      label: 'date',
      model: 'date',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: [
        v => !!v || 'Date is required',
      ]
    },

    {
      name: 'employee',
      label: 'Employee',
      items: 'employees',
      itemText: 'text',
      itemValue: 'value',
      model: 'employee',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Employee is required',
      ]
    },

    {
      name: 'rate_role_type',
      label: 'Rate Role Type',
      items: 'rateRoleTypes',
      itemText: 'text',
      itemValue: 'value',
      model: 'rateRoleType',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Rate Role Type is required',
      ]
    },

    {
      name: 'rate_used',
      label: 'Rate Used',
      model: 'rateUsed',
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: [
        v => !!v || 'Rate Used is required',
      ]
    },

    {
      name: 'amount',
      label: 'Amount',
      model: 'amount',
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: [
        v => !!v || 'Amount is required',
      ]
    },

    {
      name: 'is_paid',
      label: 'Is Paid?',
      model: 'isPaid',
      fieldType: {
        value: 'checkbox',
      },
      outlined: true,
      rules: []
    },

];

new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Commissions',
        disabled: false,
        href: URLS.COMMISSIONS,
      },
      {
        text: objectText,
        disabled: false,
        href: objectUrl,
      },
      {
        text: 'Edit',
      }
    ],
    fields: fields,
    employees: [],
    employee: data.employee,
    rateRoleTypes: data.rateRoleTypes,
    rateRoleType: data.rateRoleType,
    isPaid: data.isPaid,
    date: data.date,
    rateUsed: data.rateUsed,
    amount: data.amount,
  }),

  beforeMount(){
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.updateBreadcrumbs();
  },

});