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
      name: 'alternate_contact_number',
      label: 'Alternate Contact Number',
      value: data.alternateContactNumber,
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
      name: 'skype_id',
      label: 'Skype ID',
      value: data.skypeId,
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'ms_teams_id',
      label: 'MS Teams ID',
      value: data.msTeamsId,
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },
  ] ,

  others: [
    {
      name: 'initial_approach',
      label: 'Initial Approach',
      value: data.initialApproach,
      fieldType: {
        value: 'textfield',
        type: 'text',
      },
      outlined: true,
      rules: []
    },
    {
      name: 'meeting_arranged',
      label: 'Meeting Arranged',
      value: data.meetingArranged,
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'agreement_term',
      label: 'Agreement Term (Months)',
      model: 'agreementTerm',
      disabled: data.agreementTermDisabled,
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.00001'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'agreement_fee',
      label: 'Agreement Fee',
      model: 'agreementFee',
      disabled: data.agreementFeeDisabled,
      fieldType: {
        value: 'textfieldModeled',
        type: 'number',
        step: '0.0000000001'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'refund_scheme',
      label: 'Refund Scheme',
      value: data.refundScheme,
      disabled: data.refundSchemeDisabled,
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'validity',
      label: 'Validity',
      model: 'validity',
      disabled: data.validityDisabled,
      fieldType: {
        value: 'datetextfield',
        type: 'date'
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
      },
      outlined: true,
      rules: []
    },

    {
      name: 'business_development_person',
      label: 'Business Development Person',
      items: 'employees',
      itemText: 'text',
      itemValue: 'value',
      model: 'businessDevelopmentPerson',
      fieldType: {
        value: 'autocomplete',
      },
      clearable: true,
      dense: true,
      outlined: true,
      rules: []
    },

    {
      fieldType: {
        value: 'pointOfContacts',
      },
    },
  ]
}

new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  props: {
    source: String,
  },

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
        text: contactName,
        disabled: false,
        href: urlClient,
      },
      {
        text: 'Edit',
        disabled: true,
      }
    ],
    tab: null,
    tabs: [
      {
        tab: 'Contact Details',
        icon: iconContacts,  
      },
      {
        tab: 'Others',
        icon: 'mdi-information',  
      },
    ],
    fields: fields,
    locations: [],
    location: data.location,
    industries: [],
    industry: data.industry,
    agreementTerm: data.agreementTerm,
    agreementFee: data.agreementFee,
    pointOfContacts: [],
    employees: [],
    businessDevelopmentPerson: data.businessDevelopmentPerson,
    validity: data.validity,
  }),

  computed: {
    stringPointOfContacts: function () {
      // clean first
      let defaultPoc = {
        name: '',
        number: '',
        email: '',
        notes: '',
      }
      let pointOfContacts = this.pointOfContacts;
      let poc = _.filter(pointOfContacts, (poc) => {
        return poc.name.length;
      });
      return JSON.stringify(poc);
    }
  },

  methods: {
    setPointOfContacts: function() {
      let poc = this.$refs.pointOfContacts.value;
      poc = poc ? JSON.parse(poc) : [];
      this.pointOfContacts = poc;
    },
    newPointOfContact: function () {
      this.pointOfContacts.push({
        name: '',
        number: '',
        email: '',
        notes: '',
      });
    },
    removePoc: function (index) {
      this.pointOfContacts.splice(index, 1);
    }
  },

  beforeMount(){
    this.setDataChoices('dataLocationChoices', 'locations');
    this.setDataChoices('dataIndustryChoices', 'industries');
    this.setDataChoices('dataCandidateOwnerChoices', 'employees');
    this.updateBreadcrumbs();
  },
  mounted(){
    this.setPointOfContacts();
  }

});