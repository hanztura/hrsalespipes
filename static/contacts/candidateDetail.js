Vue.filter('intcomma', function (value) {
  if (!value) return '';
  return value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
})

Vue.filter('date', function (value, format) {
  if (!value) return '';
  return moment(value).format(format);
})

Vue.filter('defaultIfNone', function (value, defaultValue='') {
  if (value === undefined || value === null || value === '') return defaultValue;
  return value;
})

const ContactDetail = {
  props: {
    object: Object,
  },
  computed: {
    whatsAppLink: function() {
      return `https://api.whatsapp.com/send?phone=${this.object.contact_number}`;
    },

    mailtoHref: function() {
      return `mailto:${this.object.email_address}`;
    }
  },
  template: `
    <v-simple-table dense>
      <table>
        <tbody>
          <tr>
            <th>Contact Number:</th>
            <td>[[ object.contact_number ]]</td>
          </tr>
          <tr>
            <th>Alternate Contact Number:</th>
            <td>[[ object.alternate_contact_number ]]</td>
          </tr>
          <tr>
            <th>Email Address:</th>
            <td><a :href="mailtoHref">[[ object.email_address ]]</a></td>
          </tr>
          <tr>
            <th>Whatsapp Link:</th>
            <td>
              <a v-if="object.contact_number" :href="whatsAppLink" target="_blank">Click here to send WhatsApp Message</a>
            </td>
          </tr>
          <tr>
            <th>Skype ID:</th>
            <td>[[ object.skype_id ]]</td>
          </tr>
          <tr>
            <th>MS Teams ID:</th>
            <td>[[ object.ms_teams_id ]]</td>
          </tr>
          <tr>
            <th>Location:</th>
            <td>[[ object.location ]]</td>
          </tr>
        </tbody>
      </table>
    </v-simple-table>
  `
}

const ContactPersonal = {
  props: {
    object: Object
  },
  template: `
    <v-simple-table dense>
      <table>
        <tbody>
          <tr>
            <th>Nationality:</th>
            <td>[[ object.nationality ]]</td>
          </tr>
          <tr>
            <th>Languages:</th>
            <td>[[ object.languages ]]</td>
          </tr>
          <tr>
            <th>Preferred Location:</th>
            <td>[[ object.preferred_location ]]</td>
          </tr>
          <tr>
            <th>Civil Status:</th>
            <td>[[ object.civil_status ]]</td>
          </tr>
          <tr>
            <th>Gender:</th>
            <td>[[ object.gender ]]</td>
          </tr>
          <tr>
            <th>Dependents:</th>
            <td>[[ object.dependents ]]</td>
          </tr>
          <tr>
            <th>Highest Educational Qualificaiton:</th>
            <td>[[ object.highest_educational_qualification ]]</td>
          </tr>
          <tr>
            <th>Date of Birth:</th>
            <td>[[ object.date_of_birth | date('MMM-YYYY') ]]</td>
          </tr>
        </tbody>
      </table>
    </v-simple-table>
  `
}

const ContactWork = {
  props: {
    object: Object
  },
  template: `
    <v-simple-table dense>
      <table>
        <tbody>
          <tr>
            <th>Positiion:</th>
            <td>[[ object.current_previous_position ]]</td>
          </tr>
          <tr>
            <th>Company:</th>
            <td>[[ object.current_previous_company ]]</td>
          </tr>
          <tr>
            <th>Current/Previous Salary:</th>
            <td>[[ object.current_previous_salary | defaultIfNone(0) | intcomma ]]</td>
          </tr>

          <tr>
            <th>Motivation for leaving:</th>
            <td>[[ object.motivation_for_leaving ]]</td>
          </tr>

          <tr>
            <th>Expected Salary:</th>
            <td>[[ object.expected_salary | defaultIfNone(0) | intcomma ]]</td>
          </tr>
        </tbody>
      </table>
    </v-simple-table>
  `
}

const ContactOthers = {
  props: {
    object: Object
  },
  template: `
    <v-simple-table dense>
      <table>
        <tbody>
          <tr>
            <th>Visa Status:</th>
            <td>[[ object.visa_status ]]</td>
          </tr>
          <tr>
            <th>Availablity for Interview:</th>
            <td>[[ object.availability_for_interview ]]</td>
          </tr>
          <tr>
            <th>Notice Period:</th>
            <td>[[ object.notice_period ]]</td>
          </tr>
          <tr>
            <th>Candidate Owner:</th>
            <td>[[ object.candidate_owner ]]</td>
          </tr>
          <tr>
            <th>CV Template:</th>
            <td>[[ object.cv_template ]]</td>
          </tr>
          <tr>
            <th>Notes/Remarks:</th>
            <td>[[ object.notes ]]</td>
          </tr>
        </tbody>
      </table>
    </v-simple-table>
  `
}

const ContactMedical = {
  props: {
    object: Object,
    isMedical: Boolean
  },
  template: `
    <v-simple-table dense>
      <table>
        <tbody v-if="isMedical">
          <tr>
            <th>Medical Experience(years):</th>
            <td>[[ object.medical_experience_in_years ]]</td>
          </tr>
          <tr>
            <th>Specialization:</th>
            <td>[[ object.specialization ]]</td>
          </tr>
          <tr>
            <th>Other Certifications:</th>
            <td>[[ object.other_certifications ]]</td>
          </tr>
          <tr>
            <th>BLS Validity:</th>
            <td>[[ object.bls_validity | date('MM YYYY') ]]</td>
          </tr>
          <tr>
            <th>ACLS Validity:</th>
            <td>[[ object.acls_validity | date('MM YYYY') ]]</td>
          </tr>
          <tr>
            <th>HAAD/DHA Validity:</th>
            <td>[[ object.haad_dha_license_validity | date('MM YYYY') ]]</td>
          </tr>
          <tr>
            <th>HAAD/DHA License Type:</th>
            <td>[[ object.haad_dha_license_type ]]</td>
          </tr>
          <tr>
            <th>Job title on DHA/HAAD:</th>
            <td>[[ object.job_title_on_dha_haad ]]</td>
          </tr>
          <tr>
            <th>Last update on dataflow:</th>
            <td>[[ object.dataflow_last_update ]]</td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td>Non-medical</td>
          </tr>
        </tbody>
      </table>
    </v-simple-table>
  `
}

new Vue({
  el: '#inspire',
  vuetify: new Vuetify(),
  delimiters: ['[[', ']]'],
  components: {
    ContactDetail,
    ContactPersonal,
    ContactWork,
    ContactOthers,
    ContactMedical
  },

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
        disabled: true,
      },
    ],
    panel: [0, 1, 2, 3, 4, 5],
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
      {
        tab: 'Active Jobs',
        icon: 'mdi-briefcase-account',  
      },
    ],
    isDisplayExpansionPanel: true,
    isMedical: data.isMedical,
    candidate: {}
  }),

  computed: {
    displayIcon: function() {
      return this.isDisplayExpansionPanel ? 'mdi-view-list' : 'mdi-view-parallel';
    }
  },

  methods: {
    setCandidate: function() {
      return this.candidate = JSON.parse(this.$refs.objectInJSON.value);
    }
  },

  mounted(){
    this.updateBreadcrumbs();
    this.setCandidate();
  }

});