let fields = {
  contactDetails: [
    {
      name: 'code',
      label: 'Code',
      value: data.code,
      model: 'code',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'contact_number',
      label: 'Contact Number',
      value: data.contactNumber,
      model: 'contactNumber',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'alternate_contact_number',
      label: 'Alternate Contact Number',
      value: data.alternateContactNumber,
      model: 'alternateContactNumber',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'email_address',
      label: 'Email Address',
      value: data.emailAddress,
      model: 'emailAddress',
      fieldType: {
        value: 'textfield',
        type: 'email'
      },
      outlined: true,
      rules: [
        v => v == '' || /.+@.+\..+/.test(v) || 'E-mail must be in a valid format',
      ]
    },

    {
      name: 'skype_id',
      label: 'Skype ID',
      value: data.skypeId,
      model: 'skypeId',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'ms_teams_id',
      label: 'MS Teams ID',
      value: data.msTeamsId,
      model: 'msTeamsId',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      fieldType: {
        value: 'otherOnlineID',
      },
    },

    {
      name: 'location',
      label: 'Location',
      items: 'locations',
      itemText: 'text',
      itemValue: 'text',
      model: 'location',
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: []
    },
  ],

  personal: [
    {
      name: 'name',
      label: 'Name',
      value: data.name,
      model: 'name',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: [
        v => !!v || 'Name is required',
      ]
    },

    {
      name: 'has_confirmed',
      label: 'Please confirm to continue saving.',
      model: 'hasConfirmed',
      needToConfirmModel: 'needToConfirm',
      fieldType: {
        value: 'confirmCheckbox',
      },
      outlined: true,
      rules: [
        v => !!v || 'Confirmation is required'
      ]
    },

    {
      name: 'nationality',
      label: 'Nationality',
      items: 'nationalities',
      itemText: 'text',
      itemValue: 'text',
      model: 'nationality',
      fieldType: {
        value: 'autocomplete',
      },
      dense: true,
      outlined: true,
      rules: []
    },

    {
      name: 'languages',
      label: 'Languages',
      value: data.languages,
      model: 'languages',
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'preferred_location',
      label: 'Preferred Location',
      value: data.preferredLocation,
      model: 'preferredLocation',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'civil_status',
      label: 'Civil Status',
      items: 'civilStatusChoices',
      model: 'civilStatus',
      fieldType: {
        value: 'select',
      },
      dense: true,
      outlined: true,
      rules: []
    },

    {
      name: 'gender',
      label: 'Gender',
      items: 'genders',
      model: 'gender',
      fieldType: {
        value: 'select',
      },
      dense: true,
      outlined: true,
      rules: []
    },

    {
      name: 'dependents',
      label: 'Dependents',
      value: data.dependents,
      model: 'dependents',
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },
    
    {
      name: 'highest_educational_qualification',
      label: 'Highest Educational Qualificaiton',
      value: data.highestEducationalQualification,
      model: 'highestEducationalQualification',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'date_of_birth',
      label: 'Date of Birth',
      model: 'dateOfBirth',
      monthModel: 'dateOfBirthDate',
      fieldType: {
        value: 'datetextfield',
        type: 'month'
      },
      outlined: true,
      rules: []
    },
  ],

  currentPreviousWork: [
    {
      name: 'medical_experience_in_years',
      label: 'Years of Experience',
      model: 'medicalExperience',
      fieldType: {
        value: 'slider',
        min: '0',
        max: '80',
        thumbLabel: 'always',
      },
      outlined: false,
      rules: []
    },
    {
      name: 'current_previous_position',
      label: 'Positiion',
      value: data.currentPreviousPosition,
      model: 'currentPreviousPosition',
      fieldType: {
        value: 'textarea',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'current_previous_company',
      label: 'Company',
      value: data.currentPreviousCompany,
      model: 'currentPreviousCompany',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'current_previous_salary',
      label: 'Current/Previous Salary & Benefits',
      value: data.currentPreviousSalary,
      model: 'currentPreviousSalary',
      fieldType: {
        value: 'textarea',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'motivation_for_leaving',
      label: 'Motivation for leaving',
      value: data.motivationForLeaving,
      model: 'motivationForLeaving',
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'expected_salary',
      label: 'Expected Salary & Benefits',
      value: data.expectedSalary,
      model: 'expectedSalary',
      fieldType: {
        value: 'textarea',
        type: 'text'
      },
      outlined: true,
      rules: []
    },
  ],

  others: [

    {
      name: 'visa_status',
      label: 'Visa Status',
      items: 'visaStatusChoices',
      model: 'visaStatus',
      fieldType: {
        value: 'select',
      },
      dense: true,
      outlined: true,
      rules: []
    },

    {
      name: 'availability_for_interview',
      label: 'Availability for interview',
      value: data.availabilityForInterview,
      model: 'availabilityForInterview',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'notice_period',
      label: 'Notice Period',
      value: data.noticePeriod,
      model: 'noticePeriod',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'cv_template',
      label: 'CV Template',
      items: 'cvTemplates',
      model: 'cvTemplate',
      fieldType: {
        value: 'select',
      },
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'CV Template is required',
      ]
    },

    {
      name: 'candidate_owner',
      label: 'Candidate Owner',
      items: 'employees',
      itemText: 'text',
      itemValue: 'value',
      model: 'candidateOwner',
      fieldType: {
        value: 'autocomplete',
      },
      clearable: true,
      dense: true,
      outlined: true,
      rules: [
        v => !!v || 'Candidate Owner is required',
      ]
    },

    {
      name: 'notes',
      label: 'Notes',
      value: data.notes,
      model: 'notes',
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },
  ],

  medical: [

    {
      name: 'specialization',
      label: 'Specialization',
      value: data.specialization,
      model: 'specialization',
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'other_certifications',
      label: 'Other Certification(s)',
      value: data.otherCertifications,
      model: 'otherCertifications',
      fieldType: {
        value: 'textarea',
      },
      outlined: true,
      rules: []
    },

    {
      name: 'haad_dha_license_type',
      label: 'HAAD/DHA/SCHS Licence Type',
      items: 'haadDhaLicenseTypes',
      model: 'haadDhaLicenseType',
      fieldType: {
        value: 'select',
      },
      dense: true,
      outlined: true,
      rules: []
    },

    {
      name: 'job_title_on_dha_haad',
      label: 'Job Title on DHA/HAAD',
      value: data.jobTitleOnDhaHaad,
      model: 'jobTitleOnDhaHaad',
      fieldType: {
        value: 'textfield',
        type: 'text'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'bls_validity',
      label: 'BLS Validity',
      model: 'blsValidity',
      monthModel: 'blsValidityDate',
      fieldType: {
        value: 'datetextfield',
        type: 'month'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'acls_validity',
      label: 'ACLS Validity',
      model: 'aclsValidity',
      monthModel: 'aclsValidityDate',
      fieldType: {
        value: 'datetextfield',
        type: 'month'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'haad_dha_license_validity',
      label: 'HAAD/DHA Licence Validity',
      model: 'haadDhaLicenseValidity',
      monthModel: 'haadDhaLicenseValidityDate',
      fieldType: {
        value: 'datetextfield',
        type: 'month'
      },
      outlined: true,
      rules: []
    },

    {
      name: 'dataflow_last_update',
      label: 'Last Update of Dataflow',
      model: 'dataflowLastUpdate',
      fieldType: {
        value: 'datetextfield',
        type: 'date'
      },
      outlined: true,
      rules: []
    },
  ]
}

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
    panel: [0, 1, 2, 3, 4],
    fields: fields,
    alternateContactNumber: data.alternateContactNumber,
    code: data.code,
    contactNumber: data.contactNumber,
    emailAddress: data.emailAddress,
    skypeId: data.skypeId,
    msTeamsId: data.msTeamsId,
    name: data.name,
    languages: data.languages,
    preferredLocation: data.preferredLocation,
    dependents: data.dependents,
    highestEducationalQualification: data.highestEducationalQualification,
    currentPreviousPosition: data.currentPreviousPosition,
    currentPreviousCompany: data.currentPreviousCompany,
    currentPreviousSalary: data.currentPreviousSalary,
    motivationForLeaving: data.motivationForLeaving,
    expectedSalary: data.expectedSalary,
    availabilityForInterview: data.availabilityForInterview,
    noticePeriod: data.noticePeriod,
    notes: data.notes,
    specialization: data.specialization,
    otherCertifications: data.otherCertifications,
    jobTitleOnDhaHaad: data.jobTitleOnDhaHaad,
    locations: [],
    location: data.location,
    nationalities: [],
    nationality: data.nationality,
    civilStatus: data.civilStatus,
    civilStatusChoices: [
      {value: 'Single', text: 'Single'},
      {value: 'Married', text: 'Married'},
      {value: 'Widowed', text: 'Widowed'},
      {value: 'Divorced', text: 'Divorced'},
      {value: 'Separated', text: 'Separated'},
    ],
    gender: data.gender,
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
    haadDhaLicenseType: data.haadDhaLicenseType,
    haadDhaLicenseTypes: [
      {
        text: 'HAAD',
        value: 'HAAD'
      },
      {
        text: 'DHA',
        value: 'DHA'
      },
      {
        text: 'SCHS',
        value: 'SCHS'
      },
    ],
    cvTemplates: [],
    cvTemplate: data.cvTemplate,
    dateOfBirth: data.dateOfBirth,
    dateOfBirthDate: '',
    blsValidity: data.blsValidity,
    blsValidityDate: '',
    aclsValidity: data.aclsValidity,
    aclsValidityDate: '',
    haadDhaLicenseValidity: data.haadDhaLicenseValidity,
    haadDhaLicenseValidityDate: '',
    dataflowLastUpdate: data.dataflowLastUpdate,
    otherOnlineIDSource: data.otherOnlineID,
    otherOnlineID: [],

    DATE_SUBMIT_FORMAT: 'YYYY-MM-DD'
  }),

  computed: {
    otherOnlineIDOutput: function () {
      if (this.otherOnlineID.length) {
        return this.stringifyMultipleTextField(this.otherOnlineID, 'platform');
      }

      return '[]';
    }
  },

  watch: {
    blsValidity: function (value) {
      this.blsValidityDate = this.transformDate(this.blsValidity, this.DATE_SUBMIT_FORMAT);
    },
    aclsValidity: function (value) {
      this.aclsValidityDate = this.transformDate(this.aclsValidity, this.DATE_SUBMIT_FORMAT);
    },
    haadDhaLicenseValidity: function (value) {
      this.haadDhaLicenseValidityDate = this.transformDate(this.haadDhaLicenseValidity, this.DATE_SUBMIT_FORMAT);
    },
    dateOfBirth: function (value) {
      this.dateOfBirthDate = this.transformDate(this.dateOfBirth, this.DATE_SUBMIT_FORMAT);
    },
  },

  methods: {
    transformDate: function (date, format="YYYY-MM") {
      let _date = moment(date);
      return _date.isValid() ? _date.format(format) : '';
    }
  },

  beforeMount(){
    this.setDataChoices('dataVisaStatusChoices', 'visaStatusChoices');
    this.setDataChoices('dataCVTemplatesChoices', 'cvTemplates');
    this.setDataChoices('dataCandidateOwnerChoices', 'employees');
    this.setDataChoices('dataLocationChoices', 'locations');
    this.setDataChoices('dataNationalityChoices', 'nationalities');
    this.updateBreadcrumbs();

    this.blsValidity = this.transformDate(this.blsValidity);
    this.aclsValidity = this.transformDate(this.aclsValidity);
    this.haadDhaLicenseValidity = this.transformDate(this.haadDhaLicenseValidity);
    this.dateOfBirth = this.transformDate(this.dateOfBirth);

    this.setMultipleTextField(this.otherOnlineIDSource, 'otherOnlineID');
  },

});