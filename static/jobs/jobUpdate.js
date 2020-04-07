new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

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
        disabled: false,
        href: objectUrl,
      },
      {
        text: 'Edit',
        disabled: true,
      }
    ],
    clients: [],
    client: data.client,
    locations: [],
    location: data.location,
    statusChoices: [],
    initialStatus: data.initialStatus,
    status: data.status,
    hasConfirmed: data.hasConfirmed,
    date: data.date,
  }),

  computed: {
    statusIsOpen: function() {
      let status = this.status;
      if (!status) { return true; }

      status = _.find(this.statusChoices, (s) => { return s.id == status; });
      return status.is_job_open;
    },
    statusIsClose: function () {
      return !this.statusIsOpen;
    },
    initialStatusIsOpen: function(){
      let initialStatus = this.initialStatus;
      if (!initialStatus) { return true; }

      initialStatus = _.find(this.statusChoices, (s) => { return s.id == initialStatus; });
      return initialStatus.is_job_open;
    },
    needToConfirm: function () {
      let close = this.statusIsClose;
      let hasNotConfirmed = !this.hasConfirmed;
      let initialStatusIsOpen = this.initialStatusIsOpen;

      return close && hasNotConfirmed && initialStatusIsOpen;
    }
  },
  beforeMount(){
    this.setDataChoices('dataClientChoices', 'clients');
    this.setDataChoices('dataLocationChoices', 'locations');
    this.setDataChoices('dataStatusChoices', 'statusChoices');
    this.updateBreadcrumbs();
  },

});