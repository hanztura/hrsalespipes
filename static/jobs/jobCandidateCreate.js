new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Jobs',
        disabled: false,
        href: URLS.JOBS,
      },
      {
        text: jobReferenceNumber,
        disabled: false,
        href: jobUrl,
      },
      {
        text: 'Candidates',
        disabled: false,
        href: '#'
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
    candidates: [],
    candidate: data.candidate,
  }),

  beforeMount(){
    this.setDataChoices('dataCandidateChoices', 'candidates');
    this.updateBreadcrumbs();
  },

});