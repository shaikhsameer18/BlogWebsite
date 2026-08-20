document.addEventListener('DOMContentLoaded', function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile nav toggle
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', open);
    });
  }

  // Category dropdown
  document.querySelectorAll('.nav-dropdown').forEach(function (dropdown) {
    var trigger = dropdown.querySelector('.nav-dropdown__trigger');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var open = dropdown.classList.toggle('is-open');
      trigger.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.nav-dropdown.is-open').forEach(function (dropdown) {
      if (!dropdown.contains(e.target)) dropdown.classList.remove('is-open');
    });
  });

  // Scroll reveal for cards
  var revealTargets = document.querySelectorAll('.tabcard, .postcard');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    revealTargets.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i * 60, 360) + 'ms';
      observer.observe(el);
    });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Hero console: tail -f style log of recent posts
  var consoleBody = document.querySelector('[data-console-body]');
  var linesEl = document.getElementById('console-lines');
  if (consoleBody && linesEl) {
    var lines = JSON.parse(linesEl.textContent || '[]');
    consoleBody.innerHTML = '';
    if (reduceMotion) {
      lines.forEach(function (text, i) { consoleBody.appendChild(makeLine(text, i, false)); });
    } else {
      lines.forEach(function (text, i) {
        setTimeout(function () {
          var line = makeLine(text, i, false);
          line.style.animationDelay = '0ms';
          consoleBody.appendChild(line);
          if (i === lines.length - 1) {
            var cursorLine = document.createElement('div');
            cursorLine.className = 'console__line';
            cursorLine.style.opacity = '1';
            cursorLine.innerHTML = '<span class="console__prefix">$</span><span class="console__cursor"></span>';
            consoleBody.appendChild(cursorLine);
          }
        }, i * 260);
      });
    }
  }

  function makeLine(text, i, withCursor) {
    var line = document.createElement('div');
    line.className = 'console__line';
    var num = String(i + 1).padStart(2, '0');
    line.innerHTML = '<span class="console__num">' + num + '</span><span class="console__prefix">$</span> ' + text;
    return line;
  }
});
