(function () {
  document.body.classList.add("kuska-modern");

  function injectOwnerStory() {
    var path = window.location.pathname;
    var isHome = path === "/" || path === "/index.html";
    var isAbout = path.indexOf("/about") === 0;
    if (!isHome && !isAbout) return;
    if (document.querySelector(".kuska-owner-story")) return;

    var main = document.querySelector("#main-content");
    if (!main) return;

    var section = document.createElement("section");
    section.className = "kuska-owner-story";
    section.innerHTML =
      "<h2>Locally Owned. Family Focused. Community Driven.</h2>" +
      "<p>Kuska Autism Services is independently owned and operated by a passionate local leader who believes every child deserves compassionate, personalized support and every parent deserves a trusted partner.</p>" +
      "<p>We combine evidence-based ABA therapy with warm, human-centered care that helps children grow while helping families feel seen, supported, and empowered.</p>" +
      "<div class='kuska-pill-row'>" +
      "<span class='kuska-pill'>No Waitlist Diagnosing</span>" +
      "<span class='kuska-pill'>Parent Partnership</span>" +
      "<span class='kuska-pill'>Bountiful & Draper</span>" +
      "<span class='kuska-pill'>Playful, Individualized Care</span>" +
      "</div>";

    var firstSection = main.querySelector(".et_pb_section");
    if (firstSection && firstSection.parentNode) {
      firstSection.parentNode.insertBefore(section, firstSection.nextSibling);
    } else {
      main.insertBefore(section, main.firstChild);
    }
  }

  injectOwnerStory();
})();
