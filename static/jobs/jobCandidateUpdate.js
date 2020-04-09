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

    {
      name: 'registration_date',
      label: data.registrationDateLabel,
      model: 'registrationDate',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: [
        v => !!v || `${data.registrationDateLabel} is required`,
      ]
    },

    {
      name: 'status',
      label: 'Status',
      items: 'statusChoices',
      itemText: 'text',
      itemValue: 'value',
      model: 'status',
      disabled: data.statusDisabled,
      hint: 'Pipeline record exists. Status editing disabled.',
      persistentHint: true,
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
      name: 'cv_source',
      label: 'CV Source',
      items: 'cvSources',
      itemText: 'text',
      itemValue: 'text',
      disabled: false,
      model: 'cvSource',
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'CV Source is required',
      ]
    },

    {
      name: 'cv_date_shared',
      label: 'CV Date Shared',
      model: 'cvDateShared',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'remarks',
      label: 'Remarks',
      value: data.remarks,
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'salary_offered_currency',
      label: 'Salary Offered Currency',
      value: data.salaryOfferedCurrency,
      fieldType: {
        value: 'textfield',
        type: 'text',
      },
      outlined: true,
      rules: []
    },
    {
      name: 'salary_offered',
      label: 'Salary Offered',
      value: data.salaryOffered,
      fieldType: {
        value: 'textfield',
        type: 'number',
        step: '0.01'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'tentative_date_of_joining',
      label: 'Tentative Date of Joining',
      model: 'tentativeDateOfJoining',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'associate',
      label: 'Associate',
      items: 'employees',
      itemText: 'text',
      itemValue: 'value',
      model: 'associate',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Associate is required',
      ]
    },

    {
      name: 'consultant',
      label: 'Consultant',
      items: 'employees',
      itemText: 'text',
      itemValue: 'value',
      model: 'consultant',
      disabled: false,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Consultant is required',
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
        text: candidateName,
        disabled: false,
        href: jobCandidateUrl,
      },
      {
        text: 'Edit',
        disabled: true,
      }
    ],
    fields: fields,
    candidates: [],
    candidate: data.candidate,
    statusChoices: [],
    status: data.status,
    employees: [],
    associate: data.associate,
    consultant: data.consultant,
    cvSources: [],
    cvSource: data.cvSource,
    registrationDate: data.registrationDate,
    cvDateShared: data.cvDateShared,
    tentativeDateOfJoining: data.tentativeDateOfJoining,
  }),

  beforeMount(){
    this.setDataChoices('dataCandidateChoices', 'candidates');
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.setDataChoices('dataEmployeesChoices', 'employees');
    this.setDataChoices('dataCVSourceChoices', 'cvSources');
    this.updateBreadcrumbs();
  },

});