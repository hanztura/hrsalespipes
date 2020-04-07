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
        text: 'Suppliers',
        disabled: false,
        href: URLS.SUPPLIERS,
      },
      {
        text: 'New',
        disabled: true,
      }
    ],
  }),

  mounted(){
    this.updateBreadcrumbs();
  }

});