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
    employees: [],
    employee: data.employee,
    rateRoleTypes: data.rateRoleTypes,
    rateRoleType: data.rateRoleType,
    isPaid: data.isPaid,
  }),

  beforeMount(){
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.updateBreadcrumbs();
  },

});