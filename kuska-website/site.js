(function () {
  var toggle = document.querySelector(".nav-toggle");
  var body = document.body;
  var year = document.getElementById("year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  if (!toggle) {
    return;
  }

  toggle.addEventListener("click", function () {
    var open = body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(open));
  });

  document.addEventListener("click", function (event) {
    if (!body.classList.contains("nav-open")) {
      return;
    }

    var nav = document.getElementById("site-nav");
    if (!nav) {
      return;
    }

    if (nav.contains(event.target) || toggle.contains(event.target)) {
      return;
    }

    body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
  });
})();
