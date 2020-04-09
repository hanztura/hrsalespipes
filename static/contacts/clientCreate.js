let fields = {
  contactDetails: [
    {
      name: 'name',
      label: 'Name',
      value: data.name,
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: [
        v => !!v || 'Name is required',
      ]
    },

    {
      name: 'industry',
      label: 'Industry',
      items: 'industries',
      itemText: 'text',
      itemValue: 'text',
      model: 'industry',
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Industry is required',
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
      rules: []
    },

    {
      name: 'contact_number',
      label: 'Contact Number',
      value: data.contactNumber,
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'email_address',
      label: 'Email Address',
      value: data.emailAddress,
      fieldType: {
        value: 'textfield',
        type: 'email'
      },
      outlined: true,
      rules: [
        v => v == '' || /.+@.+\..+/.test(v) || 'E-mail must be in a valid format',
      ]
    },
  ] ,
}

new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Contacts',
        disabled: false,
        href: urlContacts,
      },
      {
        text: 'Clients',
        disabled: false,
        href: urlClients,
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
    fields: fields,
    locations: [],
    location: data.location,
    industries: [],
    industry: data.industry,
  }),

  beforeMount(){
    this.setDataChoices('dataLocationChoices', 'locations');
    this.setDataChoices('dataIndustryChoices', 'industries');
    this.updateBreadcrumbs();
  },
});