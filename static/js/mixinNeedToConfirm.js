Vue.mixin({
    data: () => ({
      hasConfirmed: data.hasConfirmed,
      initialNeedToConfirm: data.needToConfirm,
    }),

    computed: {
      needToConfirm: function(){
        return this.initialNeedToConfirm && !this.hasConfirmed;
      }
    },
});