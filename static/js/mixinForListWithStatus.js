Vue.mixin({
    data: () => ({
        statusChoices: [],
        status: data.status,
    }),

      methods:{
        setStatus: function() {
          // transform status into array
          let status = this.status ? this.status.split(',') : ["",];
          this.status = status;

          // add all value in choices
          this.statusChoices.unshift({ text: 'All', value:''});
        },
      },

      beforeMount() {
        this.setDataChoices('dataStatusChoices', 'statusChoices');
        this.setStatus();
      },
});