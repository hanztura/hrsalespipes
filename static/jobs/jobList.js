new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Jobs',
        disabled: true,
        href: URLS.JOBS,
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
    employees: [],
    employee: data.employee,
  }),

  beforeMount() {
    this.setDataChoices('dataEmployees', 'employees');
  },

  mounted() {
    this.updateBreadcrumbs();
  }

});