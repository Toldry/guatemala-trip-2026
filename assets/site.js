(function () {
  var body = document.body;
  var prefix = body.dataset.prefix || "";
  var current = parseInt(body.dataset.version || "0", 10);
  var latest = parseInt(body.dataset.latest || "0", 10);
  var params = new URLSearchParams(location.search);
  if (params.get("embed") === "1") body.classList.add("embed");

  fetch(prefix + "assets/versions.json").then(function (r) { return r.json(); })
    .then(function (versions) {
      var select = document.getElementById("version-select");
      if (!select) return;
      versions.slice().reverse().forEach(function (v) {
        var option = document.createElement("option");
        option.value = v.id;
        option.textContent = "v" + v.id + " · " + v.date + " · " + v.label +
          (v.id === latest ? " (latest)" : "");
        if (v.id === current) option.selected = true;
        select.appendChild(option);
      });
      if (!current) {
        var placeholder = document.createElement("option");
        placeholder.textContent = "Choose…";
        placeholder.selected = true;
        placeholder.disabled = true;
        select.insertBefore(placeholder, select.firstChild);
      }
      select.addEventListener("change", function () {
        var id = parseInt(select.value, 10);
        location.href = id === latest ? prefix : prefix + "v" + id + "/";
      });
      if (current && current !== latest) {
        var banner = document.getElementById("old-version-banner");
        banner.hidden = false;
        banner.innerHTML = "You're viewing <strong>version " + current +
          "</strong>, an older version. <a href='" + prefix +
          "'>Go to the latest (v" + latest + ")</a> · <a href='" + prefix +
          "compare/?a=" + current + "&b=" + latest + "'>Compare with latest</a>";
      }
    });
})();

// ---- sidebar table of contents: scroll tracking ----
(function () {
  var toc = document.getElementById("toc");
  if (!toc) return;
  var marker = document.getElementById("toc-marker");
  var progress = document.getElementById("toc-progress-bar");
  var links = Array.prototype.slice.call(toc.querySelectorAll("a[href^='#']"));
  var targets = links.map(function (a) {
    return document.getElementById(decodeURIComponent(a.hash.slice(1)));
  });
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var activeIndex = -1;

  function headerOffset() {
    var header = document.querySelector(".site-header");
    return (header ? header.offsetHeight : 0) + 24;
  }

  function placeMarker(link) {
    if (!link) { marker.style.opacity = 0; return; }
    var navBox = toc.getBoundingClientRect();
    var box = link.getBoundingClientRect();
    var top = box.top - navBox.top + toc.scrollTop;
    marker.style.transform = "translateY(" + top + "px)";
    marker.style.height = box.height + "px";
    marker.style.opacity = 1;
  }

  function keepVisible(link) {
    var navBox = toc.getBoundingClientRect();
    var box = link.getBoundingClientRect();
    var margin = navBox.height * 0.3;
    var delta = 0;
    if (box.top < navBox.top + margin) delta = box.top - navBox.top - margin;
    else if (box.bottom > navBox.bottom - margin)
      delta = box.bottom - navBox.bottom + margin;
    if (delta) toc.scrollBy({ top: delta, behavior: reduced ? "auto" : "smooth" });
  }

  function setActive(index) {
    if (index === activeIndex) return;
    activeIndex = index;
    links.forEach(function (a) { a.classList.remove("active", "in-path"); });
    toc.querySelectorAll("li.open").forEach(function (li) { li.classList.remove("open"); });
    if (index < 0) { placeMarker(null); return; }
    var link = links[index];
    link.classList.add("active");
    // open the chapter that holds the active entry, and mark its ancestors
    var li = link.parentElement;
    var level = link.dataset.level;
    var chapter = level === "4" ? li.parentElement.closest("li") : li;
    if (chapter && chapter.querySelector(":scope > .toc-l4")) chapter.classList.add("open");
    var ancestor = li.parentElement.closest("li");
    while (ancestor && toc.contains(ancestor)) {
      var a = ancestor.querySelector(":scope > a");
      if (a) a.classList.add("in-path");
      ancestor = ancestor.parentElement.closest("li");
    }
    // wait for the fold animation before measuring
    placeMarker(link);
    setTimeout(function () { placeMarker(link); keepVisible(link); }, 420);
  }

  var ticking = false;
  function update() {
    ticking = false;
    var line = headerOffset() + 8;
    var index = -1;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i] && targets[i].getBoundingClientRect().top <= line) index = i;
      else if (targets[i]) break;
    }
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (max > 0 && window.scrollY >= max - 2) index = targets.length - 1;
    setActive(index);
    var fraction = max > 0 ? Math.min(1, window.scrollY / max) : 0;
    progress.style.width = (fraction * 100).toFixed(1) + "%";
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener("resize", function () {
    placeMarker(links[activeIndex]);
  });
  update();

  // flash the heading you jump to, from the sidebar or any in-page link
  document.addEventListener("click", function (event) {
    var a = event.target.closest("a[href^='#']");
    if (!a) return;
    var target = document.getElementById(decodeURIComponent(a.hash.slice(1)));
    if (!target) return;
    target.classList.remove("flash");
    void target.offsetWidth;
    target.classList.add("flash");
  });
})();
