
new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Backups',
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
  }),

  mounted() {
    this.updateBreadcrumbs();
  }

});