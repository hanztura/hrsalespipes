function setDataChoices(sourceId, setDataVariable) {
    let data = document.getElementById(sourceId).value;
    this.$set(this, setDataVariable, JSON.parse(data));
}
