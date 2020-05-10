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
        text: reportText,
      },
    ],
    employees: [],
    owner: data.owner,
  }),
  mounted(){
    this.setDataChoices('dataEmployeeChoices', 'employees');
    this.updateBreadcrumbs();
  },

});