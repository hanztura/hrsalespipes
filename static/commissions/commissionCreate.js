let fields = [

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
        v => (v != '' && !!v) || 'Employee is required',
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
        text: 'New',
        disabled: true,
      }
    ],
    fields: fields,
    employees: [],
    employee: data.employee,
    rateRoleTypes: data.rateRoleTypes,
    rateRoleType: data.rateRoleType,
    rateUsed: data.rateUsed,
    amount: data.amount,
  }),

  beforeMount(){
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.updateBreadcrumbs();
  },

});