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
    statusChoices: [],
    status: data.status,
    employees: [],
    employee: data.employee,
  }),

  methods:{
    setStatus: function() {
      // transform status into array
      let status = this.status ? this.status.split(',') : ["",];
      this.status = status;

      // add all value in choices
      this.statusChoices.unshift({ text: 'All', value:''});
    },
  },

  beforeMount() {
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.setDataChoices('dataEmployees', 'employees');
    this.setStatus();
  },

  mounted() {
    this.updateBreadcrumbs();
  }

});