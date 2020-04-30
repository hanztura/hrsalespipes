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
      name: 'has_confirmed',
      label: 'Please confirm to continue saving.',
      model: 'hasConfirmed',
      needToConfirmModel: 'needToConfirm',
      fieldType: {
        value: 'confirmCheckbox',
      },
      outlined: true,
      rules: [
        v => !!v || 'Confirmation is required'
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

    {
      name: 'current_previous_position',
      label: 'Current Previous Position',
      value: data.currentPreviousPosition,
      fieldType: {
        value: 'textarea',
        type: 'text'
      },
      outlined: true,
      rules: []
    },
    {
      name: 'highest_educational_qualification',
      label: 'Education',
      value: data.highestEducationalQualification,
      fieldType: {
        value: 'textarea',
        type: 'text'
      },
      outlined: true,
      rules: []
    },
    {
      name: 'notes',
      label: 'Notes',
      value: data.notes,
      fieldType: {
        value: 'textarea',
        type: 'text'
      },
      outlined: true,
      rules: []
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
        href: URLS.CONTACTS,
      },
      {
        text: 'Candidates',
        disabled: false,
        href: URLS.CANDIDATES,
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
    fields: fields,
    locations: [],
    location: data.location,
  }),

  beforeMount(){
    this.setDataChoices('dataLocationChoices', 'locations');
    this.updateBreadcrumbs();
  },

});