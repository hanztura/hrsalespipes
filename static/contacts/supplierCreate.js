let fields = [
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
]

new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Contacts',
        disabled: false,
        href: URLS.CONTACTS,
      },
      {
        text: 'Suppliers',
        disabled: false,
        href: URLS.SUPPLIERS,
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
    fields: fields,
  }),

  mounted(){
    this.updateBreadcrumbs();
  }

});