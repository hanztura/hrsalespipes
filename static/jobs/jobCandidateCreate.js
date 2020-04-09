let fields = [
    {
      name: 'candidate',
      label: 'Candidate',
      items: 'candidates',
      itemText: 'text',
      itemValue: 'value',
      disabled: false,
      model: 'candidate',
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Candidate is required',
      ]
    },

];

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
    fields: fields,
    candidates: [],
    candidate: data.candidate,
  }),

  beforeMount(){
    this.setDataChoices('dataCandidateChoices', 'candidates');
    this.updateBreadcrumbs();
  },

});