new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Jobs',
        disabled: false,
        href: URLS.JOBS,
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
    clients: [],
    client: data.client,
  }),

  beforeMount(){
    this.setDataChoices('dataClientChoices', 'clients');
    this.updateBreadcrumbs();
  },

});
