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
    ageRange: data.ageRange,
    isMale: data.isMale,
    visaStatusChoices: [],
    visaStatus: data.visaStatus,
  }),

  computed: {
    ageRangeString: function() {
      let range = this.ageRange;
      return `${range[0]},${range[1]}`;
    }
  },
  methods:{
    transformAgeRange: function(){
      let range = this.ageRange ? this.ageRange: '0,100' ;
      range = range.split(',');
      this.ageRange = [Number(range[0]), Number(range[1])];
    }
  },

  beforeMount() {
    this.setDataChoices('ownersChoices', 'owners');
    this.setDataChoices('visaStatusChoices', 'visaStatusChoices');
    this.transformAgeRange();
  },

  mounted(){
    this.updateBreadcrumbs();
  }

});