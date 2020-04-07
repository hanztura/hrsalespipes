
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
          text: contactName,
          disabled: false,
          href: urlClient,
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
          icon: iconContacts,  
        },
        {
          tab: 'Others',
          icon: 'mdi-information',  
        },
      ],
      locations: [],
      location: data.location,
      industries: [],
      industry: data.industry,
      agreementTerm: data.agreementTerm,
      agreementFee: data.agreementFee,
      pointOfContacts: [],
      employees: [],
      businessDevelopmentPerson: data.businessDevelopmentPerson,
    }),

    computed: {
      stringPointOfContacts: function () {
        // clean first
        let defaultPoc = {
          name: '',
          number: '',
          email: '',
          notes: '',
        }
        let pointOfContacts = this.pointOfContacts;
        let poc = _.filter(pointOfContacts, (poc) => {
          return poc.name.length;
        });
        return JSON.stringify(poc);
      }
    },

    methods: {
      setPointOfContacts: function() {
        let poc = this.$refs.pointOfContacts.value;
        poc = poc ? JSON.parse(poc) : [];
        this.pointOfContacts = poc;
      },
      newPointOfContact: function () {
        this.pointOfContacts.push({
          name: '',
          number: '',
          email: '',
          notes: '',
        });
      },
      removePoc: function (index) {
        this.pointOfContacts.splice(index, 1);
      }
    },

    beforeMount(){
      this.setDataChoices('dataLocationChoices', 'locations');
      this.setDataChoices('dataIndustryChoices', 'industries');
      this.setDataChoices('dataCandidateOwnerChoices', 'employees');
      this.updateBreadcrumbs();
    },
    mounted(){
      this.setPointOfContacts();
    }

  });