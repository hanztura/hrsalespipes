Vue.mixin({
    data: () => ({
      isDisplayExpansionPanel: true,
    }),

    computed: {
      displayIcon: function() {
        return this.isDisplayExpansionPanel ? 'mdi-view-list' : 'mdi-view-parallel';
      }
    },
});