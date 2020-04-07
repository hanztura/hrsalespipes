
new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Contacts',
      },
    ],
  }),

  mounted(){
    this.updateBreadcrumbs();
  }
});