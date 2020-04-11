
new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Reports',
        href: URLS.REPORTS
      },
      {
        text: reportText,
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
  }),

  mounted() {
    this.updateBreadcrumbs();
  }

});