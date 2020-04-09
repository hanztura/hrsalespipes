let fields = {
  common: [
    {
      name: 'date_time',
      label: data.dateTimeLabel,
      model: 'dateTime',
      fieldType: {
        value: 'datetimetextfield',
        type: 'datetime-local',
      },
      outlined: true,
      rules: [
        v => !!v || `${data.dateTimeLabel} is required`,
      ]
    },

    {
      name: 'mode',
      label: 'Mode',
      items: 'modes',
      itemText: 'text',
      itemValue: 'value',
      model: 'mode',
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Mode is required',
      ]
    },

    {
      name: 'status',
      label: 'Status',
      items: 'statusChoices',
      itemText: 'text',
      itemValue: 'value',
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
  ],

  edit: [
    {
      name: 'done_by',
      label: 'Done by',
      items: 'employees',
      itemText: 'text',
      itemValue: 'value',
      model: 'doneBy',
      disabled: true,
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Done by is required',
      ]
    },
  ]
};

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
    fields: fields,
    modes: [],
    mode: data.mode,
    statusChoices: [],
    formMode: formMode,
    status: data.status,
    employees: [],
    dateTime: data.dateTime,
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