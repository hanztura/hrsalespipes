new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  props: {
    source: String,
  },

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Jobs',
        disabled: false,
        href: URLS.JOBS,
      },
      {
        text: objectText,
      },
    ],
    tab: null,
    tabs: [
      {
        tab: 'Details',
        icon: ICONS.ICON_JOBS,  
      },
      {
        tab: 'Candidates',
        icon: ICONS.ICON_CANDIDATES,  
      },
      {
        tab: 'Pipelines',
        icon: ICONS.ICON_PIPELINE,  
      },
    ],
  }),

  mounted() {
    this.updateBreadcrumbs();
  }

});