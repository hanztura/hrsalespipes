new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),
  delimiters: ['[[', ']]'],

  props: {
    source: String,
  },

  data: () => ({
    drawer: null,
    breadcrumbs: [
      {
        text: 'Dashboard',
        disabled: false,
        href: '/',
      },
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
        disabled: true,
      },
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
    pointOfContacts: [],
  }),

  methods: {
    setPointOfContacts: function() {
      let poc = this.$refs.pointOfContacts.value;
      poc = poc ? JSON.parse(poc) : [];
      this.pointOfContacts = poc;
    },
  },

  mounted(){
    this.setPointOfContacts();
  }

});