Vue.mixin({
    data: () => ({
        valid: false,
    }),
    methods: {
        submit: function(e) {
          this.$refs.form.validate();
          if (!this.valid){
            alert('Kindly check fields with errors.');
            e.preventDefault();
          }
        }
    }
});