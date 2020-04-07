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
        text: 'Successful Jobs',
      },
    ],
    consultants: [],
    consultant: data.consultant,
    industry: data.industry,
    industries: [],
  }),
  
  mounted(){
    this.setDataChoices('dataConsultantChoices', 'consultants');
    this.setDataChoices('dataIndustryChoices', 'industries');
    this.updateBreadcrumbs();
  },

});