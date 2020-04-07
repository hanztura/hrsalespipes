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
        text: candidateName,
        disabled: false,
        href: jobCandidateUrl,
      },
      {
        text: 'Edit',
        disabled: true,
      }
    ],
    candidates: [],
    candidate: data.candidate,
    statusChoices: [],
    status: data.status,
    employees: [],
    associate: data.associate,
    consultant: data.consultant,
    cvSources: [],
    cvSource: data.cvSource,
  }),

  beforeMount(){
    this.setDataChoices('dataCandidateChoices', 'candidates');
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.setDataChoices('dataCVSourceChoices', 'cvSources');
    this.updateBreadcrumbs();
  },

});