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
    locations: [],
    location: '',
  }),

  beforeMount(){
    this.setDataChoices('dataLocationChoices', 'locations');
    this.updateBreadcrumbs();
  },

});