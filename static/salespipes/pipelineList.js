new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Pipeline',
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
    employees: [],
    employee: data.employee,
  }),

  beforeMount(){
    this.setDataChoices('dataEmployeeChoices', 'employees');
  },

  mounted(){
    this.updateBreadcrumbs();
  },
});