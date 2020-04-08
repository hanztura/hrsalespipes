
new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Backups',
        disabled: false,
        href: URLS.BACKUPS,
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
  }),

  beforeMount(){
    this.updateBreadcrumbs();
  },

});