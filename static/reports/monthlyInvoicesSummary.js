
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
        text: TITLE,
      },
    ],
    consultants: [],
    consultant: data.consultant,
  }),

  mounted(){
    this.setDataChoices('dataConsultantChoices', 'consultants');
    this.updateBreadcrumbs();
  },

});