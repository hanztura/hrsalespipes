
let fields = [
  {
    name: 'reference_number',
    label: data.referenceNumberLabel,
    value: data.referenceNumber,
    fieldType: {
      value: 'textfield',
      type: 'text'
    },
    outlined: true,
    rules: [
      v => !!v || 'Reference number is required',
    ]
  },

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
      v => !!v || 'Date is required',
    ]
  },

  {
    name: 'status',
    label: 'Status',
    items: 'statusChoices',
    itemText: 'name',
    itemValue: 'id',
    model: 'status',
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
    name: 'has_confirmed',
    label: 'Please confirm to close this Job.',
    model: 'hasConfirmed',
    needToConfirmModel: 'needToConfirm',
    fieldType: {
      value: 'confirmCheckbox',
    },
    outlined: true,
    rules: [
      v => !!v || 'Confirmation is required',
    ]
  },

  {
    name: 'client',
    label: 'Client',
    items: 'clients',
    itemText: 'text',
    itemValue: 'value',
    model: 'client',
    fieldType: {
      value: 'autocomplete',
    },
    dense: true,
    outlined: true,
    rules: [
      v => !!v || 'Client is required',
    ]
  },

  {
    name: 'position',
    label: 'Position',
    value: data.position,
    fieldType: {
      value: 'textfield',
      type: 'text'
    },
    outlined: true,
    rules: [
      v => !!v || 'Position is required',
    ]
  },

  {
    name: 'location',
    label: 'Location',
    items: 'locations',
    itemText: 'text',
    itemValue: 'text',
    model: 'location',
    fieldType: {
      value: 'autocomplete',
    },
    dense: true,
    outlined: true,
    rules: [
      v => !!v || 'Location is required',
    ]
  },

  {
    name: 'potential_income',
    label: data.potentialIncomeLabel,
    value: data.potentialIncome,
    fieldType: {
      value: 'textfield',
      type: 'number'
    },
    outlined: true,
    rules: [
      v => !!v || `${data.potentialIncomeLabel} is required`,
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
        text: objectText,
        disabled: false,
        href: objectUrl,
      },
      {
        text: 'Edit',
        disabled: true,
      }
    ],
    fields: fields,
    clients: [],
    client: data.client,
    locations: [],
    location: data.location,
    statusChoices: [],
    initialStatus: data.initialStatus,
    status: data.status,
    hasConfirmed: data.hasConfirmed,
    date: data.date,
  }),

  computed: {
    statusIsOpen: function() {
      let status = this.status;
      if (!status) { return true; }

      status = _.find(this.statusChoices, (s) => { return s.id == status; });
      return status.is_job_open;
    },
    statusIsClose: function () {
      return !this.statusIsOpen;
    },
    initialStatusIsOpen: function(){
      let initialStatus = this.initialStatus;
      if (!initialStatus) { return true; }

      initialStatus = _.find(this.statusChoices, (s) => { return s.id == initialStatus; });
      return initialStatus.is_job_open;
    },
    needToConfirm: function () {
      let close = this.statusIsClose;
      let hasNotConfirmed = !this.hasConfirmed;
      let initialStatusIsOpen = this.initialStatusIsOpen;

      return close && hasNotConfirmed && initialStatusIsOpen;
    }
  },
  beforeMount(){
    this.setDataChoices('dataClientChoices', 'clients');
    this.setDataChoices('dataLocationChoices', 'locations');
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.updateBreadcrumbs();
  },

});