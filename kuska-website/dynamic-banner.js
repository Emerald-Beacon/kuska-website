(function () {
  var bannerSection = document.querySelector(".dipl_marquee_text_0_tb_header");
  var bannerText = document.querySelector(".dipl_marquee_text_0_tb_header .dipl-mt-text");
  var menuSection = document.querySelector(".et_pb_section_1_tb_header");

  if (!bannerSection || !bannerText) {
    return;
  }

  var style = document.createElement("style");
  style.textContent = [
    ".dipl_marquee_text_0_tb_header{position:fixed!important;top:0;left:0;right:0;z-index:99999;background:#3989c9;box-shadow:0 2px 10px rgba(0,0,0,.12);height:44px;display:flex;align-items:center}",
    ".dipl_marquee_text_0_tb_header .et_pb_module_inner,.dipl_marquee_text_0_tb_header .dipl-marquee-text-wrap{width:100%;height:100%}",
    ".dipl_marquee_text_0_tb_header .dipl-marquee-text-wrap{overflow:hidden;white-space:nowrap;display:flex;align-items:center;justify-content:center}",
    ".dipl_marquee_text_0_tb_header .dipl-marquee-text-inner{width:80%;max-width:1080px;overflow:hidden;display:block;margin:0 auto}",
    ".dipl_marquee_text_0_tb_header,.dipl_marquee_text_0_tb_header *{color:#ffffff!important;-webkit-text-fill-color:#ffffff!important}",
    ".dipl_marquee_text_0_tb_header .dipl-mt-text{display:inline-flex;white-space:nowrap;font-weight:600;color:#ffffff!important;-webkit-text-fill-color:#ffffff!important;line-height:44px;transform:translateX(0);will-change:transform}",
    ".dipl_marquee_text_0_tb_header .dipl-mt-text .kuska-segment{display:inline-block;padding-right:48px;color:#ffffff!important;-webkit-text-fill-color:#ffffff!important}",
    ".dipl_marquee_text_0_tb_header .dipl-mt-text.is-scrolling{animation:kuskaBannerScroll 34s linear infinite}",
    ".dipl_marquee_text_0_tb_header .dipl-mt-text:hover{animation-play-state:paused}",
    "@keyframes kuskaBannerScroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}",
    "@media (max-width:980px){.dipl_marquee_text_0_tb_header .dipl-marquee-text-inner{width:92%;max-width:none}}"
  ].join("");
  document.head.appendChild(style);

  function updateOffsets() {
    var bannerHeight = bannerSection.offsetHeight || 44;
    if (menuSection) {
      menuSection.style.top = bannerHeight + "px";
    }
    document.body.style.paddingTop = bannerHeight + "px";
  }

  function buildSeamlessTrack() {
    var baseText = (bannerText.textContent || "").trim();
    if (!baseText) {
      baseText = "Currently accepting new clients for ABA Therapy during morning and daytime hours with no waitlist at our Bountiful location!";
    }
    var message = baseText + "  •  ";
    bannerText.classList.remove("is-scrolling");
    bannerText.innerHTML =
      '<span class="kuska-segment">' + message + "</span>" +
      '<span class="kuska-segment" aria-hidden="true">' + message + "</span>";
    bannerText.style.color = "#ffffff";
    bannerText.style.setProperty("color", "#ffffff", "important");
    bannerText.style.setProperty("-webkit-text-fill-color", "#ffffff", "important");
  }

  buildSeamlessTrack();
  updateOffsets();

  window.addEventListener("resize", updateOffsets);
  window.addEventListener("load", function () {
    // Let users read the full line first, then start a seamless loop.
    setTimeout(function () {
      bannerText.classList.add("is-scrolling");
    }, 1200);
  });
})();
