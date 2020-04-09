let fields = [

    {
      name: 'date',
      label: data.dateLabel,
      model: 'date',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: [
        v => !!v || `${data.dateLabel} is required`,
      ]
    },

    {
      name: '',
      label: 'Job',
      items: 'jobs',
      itemText: 'text',
      itemValue: 'value',
      model: 'job',
      disabled: true,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: []
    },

    {
      name: 'status',
      label: 'Status',
      items: 'statusChoices',
      itemText: 'text',
      itemValue: 'value',
      model: 'status',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Status is required',
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

    {
      name: 'recruitment_term',
      label: 'Recruitment Term',
      model: 'recruitmentTerm',
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.00001'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'recruitment_rate',
      label: 'Recruitment Rate',
      model: 'recruitmentFee',
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.0000000001'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'base_amount',
      label: 'Base Amount',
      model: 'baseAmount',
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'potential_income',
      label: 'Potential Income',
      model: 'potentialIncome',
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'invoice_date',
      label: 'Invoice Date',
      model: 'invoiceDate',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'invoice_number',
      label: 'Invoice Number',
      value: data.invoiceNumber,
      fieldType: {
        value: 'textfield',
        type: 'text',
      },
      outlined: true,
      rules: []
    },

    {
      name: '',
      label: 'Invoice Amount',
      model: 'invoiceAmount',
      disabled: true,
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: []
    },

    {
      name: '',
      label: 'VAT',
      model: 'vat',
      disabled: true,
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: []
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
        text: objectText,
        disabled: false,
        href: objectUrl,
      },
      {
        text: 'Edit',
      }
    ],
    fields: fields,
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
    date: data.date,
    invoiceDate: data.invoiceDate,
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