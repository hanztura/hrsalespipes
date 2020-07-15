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
        text: 'Jobs Detail',
      },
    ],
    statusChoices: [],
    status: data.status,
    employeeChoices: [],
    recruiters: data.recruiters
  }),

  methods:{
    clearStatus: function () {
      this.status = '';
    },
    transformDataStringToArray: function(dataVariable, unshiftVariable) {
      // transform status into array
      let variable = this[dataVariable] ? this[dataVariable].split(',') : ["",];
      this[dataVariable] = variable;

      // add all value in choices
      this[unshiftVariable].unshift({ text: 'All', value:''});
    }
  },

  beforeMount() {
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.setDataChoices('dataEmployeeChoices', 'employeeChoices');
    this.transformDataStringToArray('status', 'statusChoices');
    this.transformDataStringToArray('recruiters', 'employeeChoices');
  },

  mounted() {
    this.updateBreadcrumbs();
  }

});