document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("input[type='number']").forEach(function (input) {
    input.addEventListener("wheel", function () {
      input.blur();
    });
  });
});
