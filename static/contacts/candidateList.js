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
        text: 'Candidates',
        disabled: true,
        href: URLS.CANDIDATES,
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
    owners: [],
    owner: data.owner,
  }),

  methods:{
    transformDataStringToArray: function(dataVariable) {
      // transform status into array
      let variable = this[dataVariable] ? this[dataVariable].split(',') : [];
      this[dataVariable] = variable;
    },
  },

  beforeMount() {
    this.setDataChoices('ownersChoices', 'owners');
    this.transformDataStringToArray('owner');
  },

  mounted(){
    this.updateBreadcrumbs();
  }

});