let fields = [

    {
      name: 'job',
      label: 'Job',
      items: 'jobs',
      itemText: 'text',
      itemValue: 'value',
      model: 'job',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Job is required',
      ]
    },

    {
      name: 'job_candidate',
      label: 'Job Candidate',
      items: 'jobCandidates',
      itemText: 'text',
      itemValue: 'value',
      model: 'jobCandidate',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Job Candidate is required',
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
        text: 'Pipeline',
        disabled: false,
        href: URLS.PIPELINE,
      },
      {
        text: 'New',
      }
    ],
    fields: fields,
    jobs: [],
    job: data.job,
    jobCandidates: [],
    jobCandidate: data.jobCandidate,
  }),

  watch: {
    job: function (){
      this.fetchJobCandidates();
    }
  },

  methods: {
    fetchJobCandidates: function(){
      if (this.job){
        let url = `/api/job-candidates/?job=${this.job}`;
        let _this = this;
        axios.get(url)
          .then(function(response){
            data = response.data;
            // map data
            _this.jobCandidates = _.map(data, (value) => {
              return {
                'text': value.candidate.name,
                'value': value.id
              }
            })
          })
          .catch(function(error){
            console.log(error);
          });
      }
    },
  },

  beforeMount(){
    this.setDataChoices('dataJobsChoices', 'jobs');
    this.updateBreadcrumbs();
  },

  mounted(){
    this.fetchJobCandidates();
  }

});