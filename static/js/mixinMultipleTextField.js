Vue.mixin({
  methods: {
    setMultipleTextField: function(value, model) {
      const parsedValue = value ? JSON.parse(value) : [];
      this.$set(this, model, parsedValue)
    },
    stringifyMultipleTextField: function(items, fieldToCheck) {
      let output = _.filter(items, (item) => {
        return item[fieldToCheck].length;
      });
      return JSON.stringify(output);
    },
    insertNewItem: function (model, newItem) {
      model.push(newItem);
    },
    removeItem: function (model, index) {
      model.splice(index, 1);
    },
  },
});