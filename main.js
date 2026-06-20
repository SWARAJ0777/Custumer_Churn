/* =========================================================================
   main.js
   Application bootstrap:
     - Smooth-scroll helper used across the page
     - Sticky nav active-link scroll-spy
     - Mobile hamburger menu toggle
     - Animated segment progress bars (IntersectionObserver)
     - Initial render calls for charts, pipeline detail, and customer table
   ========================================================================= */

/**
 * Smoothly scrolls to a section by id. Used by hero CTA buttons.
 * @param {string} id - target element id (without '#')
 */
function smoothTo(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Highlights the nav link matching the section currently in view.
 * Scoped strictly to ids that have a corresponding nav link, so it
 * never accidentally locks onto unrelated elements (form panels,
 * SVG gradients, etc.) that also happen to carry an id attribute.
 */
function initScrollSpy() {
  const navLinks = document.querySelectorAll('.nav-link');
  if (!navLinks.length) return;

  const sectionIds = [...navLinks].map((link) =>
    link.getAttribute('href').replace('#', '')
  );
  const sections = sectionIds
    .map((id) => document.getElementById(id))
    .filter(Boolean);

  if (!sections.length) return;

  const onScroll = () => {
    const scrollPos = window.scrollY + 90;
    let activeId = sections[0].id;

    sections.forEach((section) => {
      if (section.offsetTop <= scrollPos) {
        activeId = section.id;
      }
    });

    navLinks.forEach((link) => {
      const isActive = link.getAttribute('href') === '#' + activeId;
      link.classList.toggle('active', isActive);
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load
}

/**
 * Wires up the mobile hamburger button to toggle the nav-links panel.
 * Includes auto-close on: link tap, outside click, Escape key, and
 * window resize back to desktop width (prevents stale open state).
 */
function initMobileNav() {
  const hamburger = document.getElementById('nav-hamburger');
  const links = document.getElementById('nav-links');
  if (!hamburger || !links) return;

  const MOBILE_BREAKPOINT = 900;

  const closeMenu = () => {
    links.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.innerHTML = '<i class="ti ti-menu-2"></i>';
  };

  const openMenu = () => {
    links.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.innerHTML = '<i class="ti ti-x"></i>';
  };

  hamburger.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = links.classList.contains('open');
    isOpen ? closeMenu() : openMenu();
  });

  // Close the mobile menu after a link is tapped
  links.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  // Close when tapping/clicking anywhere outside the nav
  document.addEventListener('click', (e) => {
    const isOpen = links.classList.contains('open');
    if (isOpen && !links.contains(e.target) && !hamburger.contains(e.target)) {
      closeMenu();
    }
  });

  // Close on Escape key for accessibility
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && links.classList.contains('open')) {
      closeMenu();
      hamburger.focus();
    }
  });

  // Auto-close (and reset icon) if the viewport grows past the mobile
  // breakpoint while the menu happens to be open
  window.addEventListener(
    'resize',
    () => {
      if (window.innerWidth > MOBILE_BREAKPOINT) {
        closeMenu();
      }
    },
    { passive: true }
  );
}

/**
 * Animates the segment progress bars from 0 to their target width
 * once they scroll into view, using IntersectionObserver.
 */
function initSegmentProgressAnimation() {
  const bars = document.querySelectorAll('.seg-prog-fill');
  if (!bars.length) return;

  if (!('IntersectionObserver' in window)) {
    // Fallback: just set widths immediately
    bars.forEach((bar) => {
      bar.style.width = bar.dataset.width + '%';
    });
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.dataset.width + '%';
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.3 }
  );

  bars.forEach((bar) => observer.observe(bar));
}

/**
 * Application entry point — runs once the DOM is fully parsed.
 */
document.addEventListener('DOMContentLoaded', () => {
  initScrollSpy();
  initMobileNav();
  initSegmentProgressAnimation();

  // Charts (charts.js)
  initAllCharts();

  // Pipeline detail panel — default to step index 2 (Model Training)
  // to match the "active" state pre-set in the HTML markup.
  showPipelineStep(2);

  // Customer table (table.js)
  renderTable(CUSTOMERS);
});
