new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),
  delimiters: ['[[', ']]'],

  props: {
    source: String,
  },

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
        disabled: false,
        href: URLS.CANDIDATES,
      },
      {
        text: contactName,
        disabled: false,
        href: urlCandidate,
      },
      {
        text: 'Edit',
        disabled: true,
      }
    ],
    tab: null,
    tabs: [
      {
        tab: 'Contact Details',
        icon: ICONS.ICON_CONTACTS,  
      },
      {
        tab: 'Personal',
        icon: 'mdi-account',  
      },
      {
        tab: 'Current/Previous Work',
        icon: 'mdi-undo',  
      },
      {
        tab: 'Others',
        icon: 'mdi-information',  
      },
      {
        tab: 'Medical',
        icon: 'mdi-medical-bag',  
      },
    ],
    locations: [],
    location: data.location,
    nationalities: [],
    nationality: data.nationality,
    civilStatusChoices: [
      {value: 'Single', text: 'Single'},
      {value: 'Married', text: 'Married'},
      {value: 'Widowed', text: 'Widowed'},
      {value: 'Divorced', text: 'Divorced'},
      {value: 'Separated', text: 'Separated'},
    ],
    genders: [
      {value: 'Female', text: 'Female'},
      {value: 'Male', text: 'Male'},
    ],
    visaStatusChoices: [],
    visaStatus: data.visaStatus,
    employees: [],
    candidateOwner: data.candidateOwner,
    isMedical: data.isMedical,
    medicalExperience: data.medicalExperience,
    haadDhaLicenseTypes: [
      {
        text: 'HAAD',
        value: 'HAAD'
      },
      {
        text: 'DHA',
        value: 'DHA'
      },
    ],
    cvTemplates: [],
    cvTemplate: data.cvTemplate,
  }),

  beforeMount(){
    this.setDataChoices('dataVisaStatusChoices', 'visaStatusChoices');
    this.setDataChoices('dataCVTemplatesChoices', 'cvTemplates');
    this.setDataChoices('dataCandidateOwnerChoices', 'employees');
    this.setDataChoices('dataLocationChoices', 'locations');
    this.setDataChoices('dataNationalityChoices', 'nationalities');
    this.updateBreadcrumbs();
  },

});