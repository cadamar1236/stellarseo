// popup-component.js – Vanilla‑JS implementation of the exit‑intent modal.
// Exposes a global function `createDemoPopup()` which builds the modal, injects it into the DOM,
// and wires up all interactions (CTA, dismiss, close). It uses the CSS classes defined in styles.css.

(function () {
  // Ensure we only create one popup instance.
  let popupEl = null;

  function buildPopup() {
    // Overlay
    const overlay = document.createElement('div');
    overlay.className = 'exit-intent-overlay';

    // Modal container
    const modal = document.createElement('div');
    modal.className = 'exit-intent-modal';

    // Close (X) button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'exit-intent-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.setAttribute('aria-label', 'Close');
    modal.appendChild(closeBtn);

    // Trust badge (placeholder image – replace with real URL later)
    const badge = document.createElement('img');
    badge.className = 'exit-intent-badge';
    badge.src = 'https://www.stellarseo.com/assets/trust-badge.svg'; // assumed path
    badge.alt = 'Trusted by top e‑commerce brands';
    modal.appendChild(badge);

    // Headline
    const h1 = document.createElement('h1');
    h1.className = 'exit-intent-headline';
    h1.textContent = 'Ready to Rank Number 1 on Google? Get a Free Live Demo';
    modal.appendChild(h1);

    // Sub‑headline
    const sub = document.createElement('p');
    sub.className = 'exit-intent-subheadline';
    sub.textContent = 'Our AI instantly builds keyword lists, content briefs and link‑building plans that outrank competitors.';
    modal.appendChild(sub);

    // CTA button
    const cta = document.createElement('a');
    cta.className = 'exit-intent-cta';
    cta.href = '/demo';
    cta.textContent = 'Book My Free Demo';
    // Track CTA click
    cta.addEventListener('click', function (e) {
      if (window.trackDemoEvent) window.trackDemoEvent('cta_click');
      // Mark demo booked – in real world this would be after successful booking.
      localStorage.setItem('demo_booked', 'true');
      if (window.trackDemoEvent) window.trackDemoEvent('demo_booked');
    });
    modal.appendChild(cta);

    // Dismiss link
    const dismiss = document.createElement('button');
    dismiss.className = 'exit-intent-dismiss';
    dismiss.type = 'button';
    dismiss.textContent = 'No thanks, I will stay on my own';
    modal.appendChild(dismiss);

    // Wire up close & dismiss – both simply remove the overlay.
    function removePopup() {
      if (overlay && overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }
    closeBtn.addEventListener('click', removePopup);
    dismiss.addEventListener('click', removePopup);

    overlay.appendChild(modal);
    return overlay;
  }

  // Public API – createDemoPopup()
  window.createDemoPopup = function () {
    if (popupEl) return; // already in DOM
    popupEl = buildPopup();
    document.body.appendChild(popupEl);
  };
})();