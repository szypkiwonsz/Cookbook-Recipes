let els = document.getElementsByClassName("select-field");
for (let i = 0; i < els.length; i++) {
    els[i].value = els[i].getAttribute('value');
}