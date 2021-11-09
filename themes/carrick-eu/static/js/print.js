window.addEventListener("beforeprint", (event) => {
  for (element of document.querySelectorAll("details")) {
    element.open = true;
  }
});
