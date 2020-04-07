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
        href:jobUrl,
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
        text: 'Interviews',
        disabled: false,
        href: '#'
      },
      {
        text: formMode,
        disabled: true,
      }
    ],
    modes: [],
    mode: data.mode,
    statusChoices: [],
    formMode: formMode,
    status: data.status,
    employees: [],
    doneBy: data.doneBy,
  }),

  beforeMount(){
    this.setDataChoices('dataModesChoices', 'modes');
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.updateBreadcrumbs();

    if (this.formMode == 'Edit'){
      this.setDataChoices('dataEmployeeChoices', 'employees');
    }
  },

});