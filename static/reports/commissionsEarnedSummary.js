new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Reports',
        href: URLS.REPORTS
      },
      {
        text: 'Commissions Earned Summary', 
      },
    ],
    employees: [],
    employee: data.employee,
    isPaid: data.isPaid,
  }),

  mounted(){
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.employees.unshift({ text: 'All', value:''});
    this.updateBreadcrumbs();
  },

});