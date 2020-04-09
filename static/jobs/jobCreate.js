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
        text: 'New',
        disabled: true,
      }
    ],
    fields: fields,
    clients: [],
    client: data.client,
  }),

  beforeMount(){
    this.setDataChoices('dataClientChoices', 'clients');
    this.updateBreadcrumbs();
  },

});
