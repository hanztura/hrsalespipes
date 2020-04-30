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
        disabled: true,
      },
    ],
    page: currentPage,
    pageLength: currentPageLength,
    employees: [],
    bdPerson: data.bdPerson
  }),

  beforeMount() {
    this.setDataChoices('employeesChoices', 'employees');
  },

  mounted(){
    this.updateBreadcrumbs();
  }
});
