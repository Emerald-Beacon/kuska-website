(function () {
  var toggle = document.querySelector(".nav-toggle");
  var body = document.body;
  var year = document.getElementById("year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var revealables = document.querySelectorAll("[data-reveal]");
  if (revealables.length && "IntersectionObserver" in window && !reduceMotion) {
    document.documentElement.classList.add("can-reveal");
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -10% 0px" });
    revealables.forEach(function (el) {
      revealObserver.observe(el);
    });
  }

  var parallaxLayers = document.querySelectorAll("[data-parallax]");
  if (parallaxLayers.length && !reduceMotion) {
    var parallaxQueued = false;
    window.addEventListener("scroll", function () {
      if (parallaxQueued) {
        return;
      }
      parallaxQueued = true;
      window.requestAnimationFrame(function () {
        var y = window.scrollY;
        parallaxLayers.forEach(function (el) {
          var shift = (y * parseFloat(el.getAttribute("data-parallax"))).toFixed(1);
          el.style.transform = "translate3d(0, " + shift + "px, 0)";
        });
        parallaxQueued = false;
      });
    }, { passive: true });
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

    dropdown.addEventListener("focusout", function (event) {
      if (!dropdown.contains(event.relatedTarget)) {
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

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && body.classList.contains("nav-open")) {
      body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    }
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
