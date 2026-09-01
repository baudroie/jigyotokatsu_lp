const LINE_URL = "https://s.lmes.jp/landing-qr/1657893371-rRVdmjzQ?uLand=Pfwucb";

document.querySelectorAll(".line-link").forEach((link) => {
  link.setAttribute("href", LINE_URL);
});

const menuButton = document.querySelector(".menu-button");
const mobileMenu = document.querySelector(".mobile-menu");

menuButton?.addEventListener("click", () => {
  const isOpen = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!isOpen));
  menuButton.setAttribute("aria-label", isOpen ? "メニューを開く" : "メニューを閉じる");
  mobileMenu.hidden = isOpen;
});

mobileMenu?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "メニューを開く");
    mobileMenu.hidden = true;
  });
});

const mobileViewport = window.matchMedia("(max-width: 767px)");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function initPeopleCarousel() {
  const section = document.querySelector(".people");
  const panel = section?.querySelector(".people-panel");
  const track = section?.querySelector(".people-track");
  const slides = [...(track?.querySelectorAll(".person-story") || [])];
  const dots = [...(section?.querySelectorAll(".people-pagination button") || [])];
  const status = section?.querySelector(".people-status");
  if (!panel || !track || slides.length < 2 || dots.length !== slides.length) return;

  let current = 0;
  let gesture = null;
  section.classList.add("carousel-enabled");

  function showSlide(index, announce = true) {
    current = (index + slides.length) % slides.length;
    track.style.setProperty("--people-index", mobileViewport.matches ? current : 0);
    slides.forEach((slide, i) => {
      const hidden = mobileViewport.matches && i !== current;
      slide.inert = hidden;
      if (mobileViewport.matches) {
        slide.setAttribute("aria-hidden", String(hidden));
        slide.setAttribute("role", "group");
        slide.setAttribute("aria-roledescription", "スライド");
        slide.setAttribute("aria-label", `${i + 1} / ${slides.length}`);
      } else {
        ["aria-hidden", "role", "aria-roledescription", "aria-label"].forEach((name) => slide.removeAttribute(name));
      }
      dots[i].setAttribute("aria-current", String(i === current));
    });
    if (status) status.textContent = mobileViewport.matches && announce
      ? `${current + 1} / ${slides.length}：${slides[current].querySelector(".speech").alt}` : "";
  }

  function updateViewport() {
    gesture = null;
    if (mobileViewport.matches) {
      panel.setAttribute("role", "region");
      panel.setAttribute("aria-roledescription", "カルーセル");
      panel.setAttribute("aria-label", "挑戦している先輩たち");
    } else {
      ["role", "aria-roledescription", "aria-label"].forEach((name) => panel.removeAttribute(name));
    }
    showSlide(0, false);
  }

  dots.forEach((dot, index) => dot.addEventListener("click", () => {
    if (mobileViewport.matches) showSlide(index);
  }));
  section.querySelector(".people-pagination").addEventListener("keydown", (event) => {
    if (!mobileViewport.matches || !["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === "Home" ? 0 : event.key === "End" ? slides.length - 1 : current + (event.key === "ArrowRight" ? 1 : -1);
    showSlide(next);
    dots[current].focus();
  });

  // Pointer Events cover touch, pen and mouse. Native vertical scrolling stays
  // enabled; cancelled/multi-touch gestures and movements under 50px do nothing.
  panel.addEventListener("pointerdown", (event) => {
    if (!event.isPrimary) { gesture = null; return; }
    if (!mobileViewport.matches || event.button !== 0) return;
    gesture = { id: event.pointerId, x: event.clientX, y: event.clientY };
    panel.setPointerCapture(event.pointerId);
  });
  panel.addEventListener("pointerup", (event) => {
    if (!gesture || gesture.id !== event.pointerId) return;
    const dx = event.clientX - gesture.x;
    const dy = event.clientY - gesture.y;
    gesture = null;
    if (panel.hasPointerCapture(event.pointerId)) panel.releasePointerCapture(event.pointerId);
    if (Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy) * 1.25) showSlide(current + (dx < 0 ? 1 : -1));
  });
  ["pointercancel", "lostpointercapture"].forEach((type) => panel.addEventListener(type, () => { gesture = null; }));
  mobileViewport.addEventListener("change", updateViewport);
  updateViewport();
}

function initScrollReveals() {
  // If scripting/IntersectionObserver is unavailable, content remains visible.
  if (reducedMotion.matches || !("IntersectionObserver" in window)) return;
  const groups = new Map();
  const allTargets = new Set();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      (groups.get(entry.target) || [entry.target]).forEach((element) => element.classList.add("is-visible"));
      observer.unobserve(entry.target);
      groups.delete(entry.target);
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -4% 0px" });

  function prepare(element, delay = 0, direction = "up") {
    element.classList.add("reveal", `reveal--${direction}`);
    element.style.setProperty("--reveal-delay", `${delay}ms`);
    allTargets.add(element);
  }
  function observe(selector, stagger = 0, direction = "up", delay = 0) {
    document.querySelectorAll(selector).forEach((element, index) => {
      prepare(element, delay + index * stagger, direction);
      observer.observe(element);
    });
  }

  const hero = [...document.querySelectorAll(".brand,.hero-title,.hero-sub,.hero-detail,.hero-actions .image-button")];
  hero.forEach((element, index) => prepare(element, index * 120));
  const showHero = () => requestAnimationFrame(() => requestAnimationFrame(() => {
    let order = 0;
    hero.forEach((element) => {
      element.style.setProperty("--reveal-delay", `${element.getClientRects().length ? order++ * 120 : 0}ms`);
      element.classList.add("is-visible");
    });
  }));
  if (document.readyState === "complete") showHero();
  else window.addEventListener("load", showHero, { once: true });

  observe(".benefit-card", 100);
  observe(".section-image-title");
  // Observe the whole diagram to keep icon/arrow order on both layouts.
  const diagram = document.querySelector(".frontline-diagram");
  if (diagram) {
    const steps = [...diagram.children];
    steps.forEach((element, index) => prepare(element, 100 + index * 100));
    groups.set(diagram, steps);
    observer.observe(diagram);
  }
  observe(".frontline-description-text", 0, "fade", 600);
  observe(".field-grid > img", 90);
  observe(".career-item", 100);
  observe(".career-note", 0, "fade", 400);
  const peoplePanel = document.querySelector(".people-panel");
  if (peoplePanel) {
    const stories = [...peoplePanel.querySelectorAll(".person-story")];
    stories.forEach((element, index) => prepare(element, index * 100, index ? "left" : "right"));
    groups.set(peoplePanel, stories);
    observer.observe(peoplePanel);
  }
  observe(".people-pagination", 0, "fade");
  observe(".flow-card", 100);
  observe(".final-copy h2");
  observe(".final-subtitle,.final-subtext-mobile", 0, "up", 120);
  observe(".final-line", 0, "up", 240);
  observe(".site-footer > *", 0, "fade");

  // Keyboard navigation must never focus an invisible CTA/menu destination.
  document.addEventListener("focusin", (event) => {
    const element = event.target.closest(".reveal");
    if (element) {
      element.style.setProperty("--reveal-delay", "0ms");
      element.classList.add("is-visible");
      observer.unobserve(element);
    }
  });
  reducedMotion.addEventListener("change", (event) => {
    if (!event.matches) return;
    observer.disconnect();
    allTargets.forEach((element) => element.classList.add("is-visible"));
    groups.clear();
  });
}

initPeopleCarousel();
initScrollReveals();
