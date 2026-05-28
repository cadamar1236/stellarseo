// exit-intent.js
// Detects when the user moves the mouse cursor out of the viewport (towards top)
// Fires once per session and respects paid user / recent demo booking exclusions.

;(function () {
  // Helper to read a cookie value
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  // Session flag to ensure only one popup per session
  const SESSION_SHOWN_KEY = 'exit_intent_shown';

  // Load AB testing utilities (if available)
  // We'll rely on global functions defined by ab-testing.js if present.
  const getVariant = window.getDemoVariant || function () {
    // Fallback: always treat as treatment
    return 'treatment';
  };
  const trackEvent = window.trackDemoEvent || function () {};
  const isPaidUser = window.isPaidUser || function () { return !!getCookie('paid_user'); };
  const hasBookedDemo = window.hasBookedDemo || function () { return !!getCookie('demo_booked'); };

  function shouldShowPopup() {
    if (sessionStorage.getItem(SESSION_SHOWN_KEY)) return false; // already shown this session
    if (isPaidUser()) return false;
    if (hasBookedDemo()) return false;
    if (getVariant() !== 'treatment') return false; // control group
    return true;
  }

  function showPopup() {
    // Create and display the popup via the component
    if (window.createDemoPopup) {
      window.createDemoPopup();
    }
    sessionStorage.setItem(SESSION_SHOWN_KEY, '1');
    trackEvent('popup_shown');
  }

  function onMouseLeave(e) {
    // e.clientY < 0 indicates cursor left the top of the viewport
    if (e.clientY < 0) {
      document.removeEventListener('mousemove', onMouseLeave);
      if (shouldShowPopup()) {
        trackEvent('impression');
        showPopup();
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Only bind if the popup can potentially be shown
    if (getVariant() === 'treatment') {
      document.addEventListener('mousemove', onMouseLeave);
    }
  });
})();