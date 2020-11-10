const NAVIGATION_DRAWER_ITEMS = [
  {
    action: ICONS.ICON_DASHBOARD,
    title: 'Dashboard',
    href: URLS.DASHBOARD,
    iconColor: 'primary--text',
  },
  {
    action: ICONS.ICON_CONTACTS,
    title: 'Contacts',
    items: [
      { title: 'Candidates',
        href: URLS.CANDIDATES,
        iconColor: 'primary--text',
        action: ICONS.ICON_CANDIDATES,
      },
      { title: 'Clients',
        href: URLS.CLIENTS,
        iconColor: 'primary--text',
        action: ICONS.ICON_CLIENTS,
      },
      { title: 'Suppliers',
        href: URLS.SUPPLIERS,
        iconColor: 'primary--text',
        action: ICONS.ICON_SUPPLIERS,
      },
    ],
  },
  {
    action: ICONS.ICON_JOBS,
    title: 'Jobs',
    href: URLS.JOBS,
    iconColor: 'primary--text',
  },
  {
    action: ICONS.ICON_PIPELINE,
    title: 'Pipeline',
    href: URLS.PIPELINE,
    iconColor: 'primary--text',
  },
  {
    action: ICONS.ICON_REPORTS,
    title: 'Reports',
    href: URLS.REPORTS,
    iconColor: 'primary--text',
  },
];

const DASHBOARD_URL = URLS.DASHBOARD;

Vue.mixin({
  delimiters: ['[[', ']]'],

  data: () => ({
    drawer: null,
    navigationDrawerItems: NAVIGATION_DRAWER_ITEMS,
    navigationDrawerItemsNonAuthenticatedUsers: [
      {
        action: 'mdi-information',
        title: 'About',
        href: URLS.ABOUT,
        iconColor: 'primary--text',
      },
      {
        action: 'mdi-head-question',
        title: 'How to use?',
        href: 'https://www.youtube.com/watch?v=tIAe5LANfM0&list=PLcr7blJ6ArQFeLv5YcLl0EYc2jwNkynZ_',
        iconColor: 'primary--text',
      },
    ],
    breadcrumbs: [
      {
        text: 'Dashboard',
        disabled: false,
        href: DASHBOARD_URL,
      },
    ],
    subBreadcrumbs: [],
    isCommissionAllowed: PERMISSIONS.isCommissionAllowed,
    isBackupAllowed: PERMISSIONS.isBackupAllowed,
  }),

  watch: {
    drawer: function (newValue, oldValue){
      localStorage.setItem('drawer' ,JSON.stringify(newValue));
    }
  },

  methods: {
    updateNavigationDrawerItems() {

    },
    updateBreadcrumbs() {
      this.breadcrumbs = this.breadcrumbs.concat(this.subBreadcrumbs);

      // add commission to navigation drawer
      if (this.isCommissionAllowed) {
        this.navigationDrawerItems.push({
          action: ICONS.ICON_COMMISSIONS,
          title: 'Commissions',
          href: URLS.COMMISSIONS,
        });
      }

      // add backups to navigation drawer
      if (this.isBackupAllowed) {
        this.navigationDrawerItems.push({
          action: ICONS.ICON_BACKUPS,
          title: 'Backups',
          href: URLS.BACKUPS,
        });
      }
    },
    setDataChoices(sourceId, setDataVariable) {
        let data = document.getElementById(sourceId).value;
        this.$set(this, setDataVariable, JSON.parse(data));
    },
    pageGoTo(page) {
        let url = location.href;
        if (url.indexOf('?') < 0){ url += '?' }

        url = `${url}&page=${this.page}`;
        location.href = url;
    },

    setInitialDrawer(){
      let drawer = JSON.parse(localStorage.getItem('drawer'));

      this.$set(this, 'drawer', drawer)
    },

  },

  beforeMount() {
    this.setInitialDrawer();
  }
});