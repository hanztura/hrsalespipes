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
        icon: ICONS.CONTACTS,  
      },
    ],
    pointOfContacts: [],
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

  mounted(){
    this.updateBreadcrumbs();
    this.setPointOfContacts();
    this.newPointOfContact();
  }

});