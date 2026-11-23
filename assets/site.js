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
