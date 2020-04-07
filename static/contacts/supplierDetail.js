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
        disabled: true,
      },
    ],
    tab: null,
    tabs: [
      {
        tab: 'Contact Details',
        icon: ICONS.ICON_CONTACTS,  
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
    this.updateBreadcrumbs();
    this.setPointOfContacts();
  }

});