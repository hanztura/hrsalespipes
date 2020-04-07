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
        text: objectText,
        disabled: false,
        href: objectUrl,
      },
      {
        text: 'Edit',
      }
    ],
    jobs: [],
    job: data.job,
    jobCandidates: [],
    jobCandidate: data.jobCandidate,
    statusChoices: [],
    status: data.status,
    recruitmentTerm: data.recruitmentTerm,
    recruitmentFee: data.recruitmentFee,
    baseAmount: data.baseAmount,
    potentialIncome: data.potentialIncome,
    vatRate: data.vatRate,
    vat: data.vat,
    invoiceAmount: data.invoiceAmount,
  }),

  watch: {
    recruitmentTerm: function (val, oldVal){
      this.potentialIncome = this.computedPotentialIncome;
    },
    recruitmentFee: function (val, oldVal){
      this.potentialIncome = this.computedPotentialIncome;
    },
    baseAmount: function (val, oldVal){
      this.potentialIncome = this.computedPotentialIncome;
    },
    potentialIncome: function () {
      this.vat = this.computedVat;
      this.invoiceAmount = this.computedInvoiceAmount;
    },
    job: function (){
      this.fetchJobCandidates();
    }
  },

  computed: {
    computedPotentialIncome: function () {
      amount = this.baseAmount * this.recruitmentTerm * this.recruitmentFee;
      return _.round(amount, 2);
    },
    computedInvoiceAmount: function() {
      amount = Number(this.potentialIncome) + Number(this.vat);
      return _.round(amount, 2);
    },
    computedVat: function() {
      amount = Number(this.potentialIncome) * Number(this.vatRate);
      return _.round(amount, 2);
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
    }
  },

  beforeMount(){
    this.setDataChoices('dataJobsChoices', 'jobs');
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.updateBreadcrumbs();
    this.fetchJobCandidates();
  },

});