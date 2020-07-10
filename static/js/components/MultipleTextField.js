const MultipleTextfield = {
  props: {
    title: String,
    items: Array,
    newItem: Object,
    model: String
  },

  methods: {
    insertNewItem: function () {
      this.$emit('insertNewItem', this.model, this.newItem);
    },
    removeItem: function (index) {
      this.$emit('removeItem', model, index);
    }
  },

  template: `
    <v-text-field
      :label="field.label"
      :type="field.type"
      outlined
      v-model.lazy="contact.email">
    </v-text-field>
  `
}