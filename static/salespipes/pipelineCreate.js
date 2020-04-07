
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