Vue.mixin({
    data: () => ({
      stringsToTransform: data.stringsToTransform,
    }),

    methods:{
      transformDataStringToArray: function(dataVariable) {
        // transform status into array
        let variable = this[dataVariable] ? this[dataVariable].split(',') : [];
        this[dataVariable] = variable;
      },
    },

      beforeMount() {
        for (index in this.stringsToTransform) {
          let string = this.stringsToTransform[index];
          this.transformDataStringToArray(string);
        }
      },
});