new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Commissions',
        disabled: false,
        href: URLS.COMMISSIONS,
      },
      {
        text: objectText,
        disabled: false,
        href: objectUrl,
      },
      {
        text: 'Delete',
      }
    ],
  }),

  beforeMount(){
    this.updateBreadcrumbs();
  },

});