new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Reports',
        href: '{% url "reports:index" %}'
      },
      {
        text: 'Pipeline Summary',
      },
    ],
    consultants: [],
    consultant: data.consultant,
  }),
  mounted(){
    this.setDataChoices('dataConsultantChoices', 'consultants');
    this.updateBreadcrumbs();
  },

});