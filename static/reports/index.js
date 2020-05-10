new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),

  data: () => ({
    drawer: null,
    subBreadcrumbs: [
      {
        text: 'Reports',
      },
    ],
    reports: [
      {
        icon: ICONS.ICON_CANDIDATES,
        href: urlCandidatesRegistration,
        title: 'Candidates Registration',
      },
      {
        icon: ICONS.ICON_COMMISSIONS,
        href: urlCommissionEarned,
        title: 'Commissions Earned Summary',
      },
      {
        icon: 'mdi-send-check',
        href: urlCVSent,
        title: 'CV Sent to Clients',
      },
      {
        icon: 'mdi-headphones',
        href: urlInterviews,
        title: 'Interviews Report',
      },
      {
        icon: 'mdi-clipboard-arrow-right',
        href: urlJobToPipeline,
        title: 'Job to Pipeline Analysis',
      },
      {
        icon: ICONS.ICON_JOBS,
        href: urlJobsDetail,
        title: 'Jobs Detail Report',
      },
      {
        icon: ICONS.ICON_JOBS,
        href: urlJobsSummary,
        title: 'Jobs Summary',
      },
      {
        icon: 'mdi-file-percent',
        href: urlMonthlyInvoices,
        title: 'Monthly Invoices Summary',
      },
      {
        icon: ICONS.ICON_CONTACTS,
        href: urlNewlySignedClients,
        title: 'Newly Signed Clients',
      },
      {
        icon: ICONS.ICON_PIPELINE,
        href: urlPipelineSummary,
        title: 'Pipeline Summary'
      },
      {
        icon: ICONS.ICON_JOBS,
        href: urlStartDatePerWeekMonth,
        title: 'Start date per week/month'
      },
      {
        icon: 'mdi-briefcase-check',
        href: urlSuccessfulJob,
        title: 'Successful Jobs'
      },
    ]
  }),

  mounted(){
    this.updateBreadcrumbs();
  }
});