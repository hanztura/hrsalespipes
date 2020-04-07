
  new Vue({
    el: '#inspire',
    vuetify: new Vuetify(),

    data: () => ({
      drawer: null,
      subBreadcrumbs: [
        {
          text: 'Contacts',
          disabled: false,
          href: urlContacts,
        },
        {
          text: 'Clients',
          disabled: false,
          href: urlClients,
        },
        {
          text: 'New',
          disabled: true,
        }
      ],
      locations: [],
      location: data.location,
      industries: [],
      industry: data.industry,
    }),

    beforeMount(){
      this.setDataChoices('dataLocationChoices', 'locations');
      this.setDataChoices('dataIndustryChoices', 'industries');
      this.updateBreadcrumbs();
    },
  });