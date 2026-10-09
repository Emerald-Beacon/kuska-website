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

  // WCAG 2.2.2: touch users can't hover, so the logo marquee gets a real pause control.
  var marquee = document.querySelector(".logo-marquee");
  var marqueeToggle = document.querySelector(".logo-marquee__toggle");
  // Each track slides left by its own width, so the copies behind it must cover
  // the whole viewport or wide screens see the row run out before it loops.
  // Add hidden copies until they do, then restart every track so they stay in step.
  if (marquee && !reduceMotion) {
    var fillMarquee = function () {
      var tracks = marquee.querySelectorAll(".logo-marquee__track");
      var trackWidth = tracks[0].offsetWidth;
      if (!trackWidth) {
        return;
      }
      var needed = Math.ceil(marquee.offsetWidth / trackWidth) + 1;
      if (tracks.length >= needed) {
        return;
      }
      for (var i = tracks.length; i < needed; i++) {
        marquee.appendChild(tracks[tracks.length - 1].cloneNode(true));
      }
      tracks = marquee.querySelectorAll(".logo-marquee__track");
      tracks.forEach(function (track) { track.style.animation = "none"; });
      void marquee.offsetWidth;
      tracks.forEach(function (track) { track.style.animation = ""; });
    };
    fillMarquee();
    window.addEventListener("resize", fillMarquee);
  }

  if (marquee && marqueeToggle) {
    marqueeToggle.addEventListener("click", function () {
      var paused = marquee.classList.toggle("is-paused");
      marqueeToggle.textContent = paused ? "Play logos" : "Pause logos";
    });
  }

  if (!toggle) {
    return;
  }

  // While the full-screen menu is open, everything behind it is inert so
  // keyboard focus can't wander onto content the menu is covering.
  var behindMenu = document.querySelectorAll(".announcement-bar, main, .site-footer");

  function setMenuOpen(open) {
    body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    behindMenu.forEach(function (el) {
      if (open) {
        el.setAttribute("inert", "");
      } else {
        el.removeAttribute("inert");
      }
    });
  }

  toggle.addEventListener("click", function () {
    setMenuOpen(!body.classList.contains("nav-open"));
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && body.classList.contains("nav-open")) {
      setMenuOpen(false);
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

    setMenuOpen(false);
  });

  // Growing past the mobile breakpoint hides the menu; don't leave the page inert.
  window.matchMedia("(min-width: 821px)").addEventListener("change", function (event) {
    if (event.matches && body.classList.contains("nav-open")) {
      setMenuOpen(false);
    }
  });
})();
