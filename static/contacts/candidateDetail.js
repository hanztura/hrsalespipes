new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),
  delimiters: ['[[', ']]'],

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
        text: 'Candidates',
        disabled: false,
        href: URLS.CANDIDATES,
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
      {
        tab: 'Personal',
        icon: 'mdi-account',  
      },
      {
        tab: 'Current/Previous Work',
        icon: 'mdi-undo',  
      },
      {
        tab: 'Others',
        icon: 'mdi-information',  
      },
      {
        tab: 'Medical',
        icon: 'mdi-medical-bag',  
      },
    ],
    isMedical: data.isMedical,
  }),

  mounted(){
    this.updateBreadcrumbs();
  }

});