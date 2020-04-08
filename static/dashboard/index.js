
new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [],
  }),

  mounted() {
    this.updateBreadcrumbs();
  }

});