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
        text: jobReferenceNumber,
        disabled: false,
        href: jobUrl,
      },
      {
        text: 'Candidates',
        disabled: false,
        href: '#'
      },
      {
        text: candidateName,
        disabled: true,
      }
    ],
    tab: null,
    tabs: [
      {
        tab: 'Job Candidate Detail',
        icon: ICONS.ICON_CANDIDATES,  
      },
      {
        tab: 'Interviews',
        icon: 'mdi-headphones',  
      },
    ],
  }),

  mounted(){
    this.updateBreadcrumbs();
  },

});