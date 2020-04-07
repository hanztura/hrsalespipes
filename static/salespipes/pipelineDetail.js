
new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Pipeline',
        disabled: false,
        href: URLS.PIPELINE,
      },
      {
        text: objectText,
      },
    ],
    tab: null,
    tabs: [
      {
        tab: 'Pipeline Detail',
        icon: ICONS.ICON_PIPELINE,  
      },
      {
        tab: 'Job Candidate',
        icon: ICONS.CANDIDATES,  
      },
    ],
  }),

  mounted(){
    this.updateBreadcrumbs();
  },

});