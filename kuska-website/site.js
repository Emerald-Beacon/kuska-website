(function () {
  var toggle = document.querySelector(".nav-toggle");
  var body = document.body;
  var year = document.getElementById("year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  var dropdown = document.querySelector(".nav-dropdown");
  if (dropdown) {
    var dropdownToggle = dropdown.querySelector(".nav-dropdown__toggle");

    dropdownToggle.addEventListener("click", function () {
      var open = dropdown.classList.toggle("is-open");
      dropdownToggle.setAttribute("aria-expanded", String(open));
    });

    document.addEventListener("click", function (event) {
      if (!dropdown.contains(event.target)) {
        dropdown.classList.remove("is-open");
        dropdownToggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && dropdown.classList.contains("is-open")) {
        dropdown.classList.remove("is-open");
        dropdownToggle.setAttribute("aria-expanded", "false");
        dropdownToggle.focus();
      }
    });
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
