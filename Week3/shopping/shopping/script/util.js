
export function initMobileMenuToggle() {
  const menuBtn = document.getElementById("menu-btn");
  const mobileMenu = document.querySelector(".js-mobile-menu");
  console.log(mobileMenu)

  if (!menuBtn || !mobileMenu) return;
  
  menuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("hidden");
  });

  document.addEventListener("click", (e) => {
    if (!menuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
      mobileMenu.classList.add("hidden");
    }
  });
}

