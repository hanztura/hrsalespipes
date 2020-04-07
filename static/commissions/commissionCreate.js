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
    employees: [],
    employee: data.employee,
    rateRoleTypes: data.rateRoleTypes,
    rateRoleType: data.rateRoleType,
  }),

  beforeMount(){
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.updateBreadcrumbs();
  },

});