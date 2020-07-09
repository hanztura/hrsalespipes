let fields = [

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
  // {
  //   name: 'email_address',
  //   label: 'Email Address',
  //   value: data.emailAddress,
  //   fieldType: {
  //     value: 'textfield',
  //     type: 'email'
  //   },
  //   outlined: true,
  //   rules: [
  //     v => v == '' || /.+@.+\..+/.test(v) || 'E-mail must be in a valid format',
  //   ]
  // },
  {
    name: 'website',
    label: 'Website',
    value: data.website,
    fieldType: {
      value: 'textfield',
      type: 'url'
    },
    outlined: true,
    rules: []
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
  {
    name: 'subscription_validity',
    label: 'Subscription Validity',
    model: 'subscriptionValidity',
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
    fieldType: {
      value: 'pointOfContacts',
    },
  },
]

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
        href: URLS.CONTACTS,
      },
      {
        text: 'Suppliers',
        disabled: false,
        href: URLS.SUPPLIERS,
      },
      {
        text: contactName,
        disabled: false,
        href: contactUrl,
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
        icon: ICONS.ICON_CONTACTS,  
      },
    ],
    fields: fields,
    pointOfContacts: [],
    subscriptionValidity: data.subscriptionValidity
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
        notes: '',  // position
      });
    },
    removePoc: function (index) {
      this.pointOfContacts.splice(index, 1);
    }
  },

  mounted(){
    this.updateBreadcrumbs();
    this.setPointOfContacts();
    this.newPointOfContact();
  }

});