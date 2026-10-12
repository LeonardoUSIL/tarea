// Los ejemplos rellenan (o agregan líneas a) el cuadro de códigos.
document.querySelectorAll("[data-ejemplo]").forEach(function (boton) {
  boton.addEventListener("click", function () {
    var area = document.getElementById("codigos");
    area.value = area.value.trim() ? area.value.replace(/\s+$/, "") + "\n" + boton.dataset.ejemplo : boton.dataset.ejemplo;
    area.focus();
  });
});
