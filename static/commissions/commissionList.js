new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Commissions',
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
  }),

  mounted() {
    this.updateBreadcrumbs();
  }

});