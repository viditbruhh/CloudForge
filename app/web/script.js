(() => {
  document.body.classList.add('dark-mode');

  const links = [...document.querySelectorAll('.navbar nav a[href]')];
  const sections = ['features', 'architecture', 'stack', 'about']
    .map(id => document.getElementById(id))
    .filter(Boolean);

  function setActive(id) {
    links.forEach(link => {
      const target = link.getAttribute('href');
      const active = id === 'home' ? target === '#' : target === `#${id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }

  links.forEach(link => {
    link.addEventListener('click', () => {
      const id = link.getAttribute('href').slice(1) || 'home';
      setActive(id);
    });
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries
        .filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (visible) setActive(visible.target.id);
    }, {
      rootMargin: '-20% 0px -60% 0px',
      threshold: [0, 0.1, 0.25, 0.5]
    });

    sections.forEach(section => observer.observe(section));
  }

  window.addEventListener('hashchange', () => {
    setActive(location.hash.slice(1) || 'home');
  });

  setActive(location.hash.slice(1) || 'home');
})();

document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.querySelector('.mobile-menu-toggle');
  const nav = document.querySelector('#primary-navigation');

  if (!menuButton || !nav) return;

  function closeMenu() {
    nav.classList.remove('mobile-menu-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation menu');
  }

  menuButton.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('mobile-menu-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menuButton.setAttribute(
      'aria-label',
      isOpen ? 'Close navigation menu' : 'Open navigation menu'
    );
  });

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 760) closeMenu();
  });
});
