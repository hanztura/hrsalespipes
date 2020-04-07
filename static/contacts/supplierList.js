
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
        disabled: true,
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
  }),

  mounted(){
    this.updateBreadcrumbs();
  }

});
