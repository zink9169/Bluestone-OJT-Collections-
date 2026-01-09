fetch("header.html")
  .then((res) => res.text())
  .then((html) => {
    document.getElementById("header-placeholder").innerHTML = html;

    const path = window.location.pathname.split("/").pop();
    document.querySelectorAll("nav a").forEach((link) => {
      if (link.getAttribute("href") === path) {
        link.style.fontWeight = "bold";
        link.style.color = "blue";
      }
    });
  });
