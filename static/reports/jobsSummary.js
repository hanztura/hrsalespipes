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
        text: 'Jobs Summary',
      },
    ],
    statusChoices: [],
    status: data.status,
  }),

  methods:{
    clearStatus: function () {
      this.status = '';
      console.log('hellow');
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
    this.transformDataStringToArray('status', 'statusChoices');
  },

  mounted() {
    this.updateBreadcrumbs();
  }

});