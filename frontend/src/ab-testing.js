// ab-testing.js – Implements AB‑test variant logic and event tracking for the exit‑intent popup.
// This file is loaded globally (e.g., via a <script> tag) and exposes helper functions on the window object.

(function () {
  const VARIANT_COOKIE = 'exit_intent_variant';
  const VARIANT_TTL_DAYS = 30;
  const EVENT_STORAGE_KEY = 'exit_intent_events';

  /**
   * Reads a cookie value.
   * @param {string} name
   * @returns {string|null}
   */
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  /**
   * Writes a cookie.
   * @param {string} name
   * @param {string} value
   * @param {number} days
   */
  function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
  }

  /**
   * Returns the AB test variant for the current visitor.
   * Possible values: 'control' | 'treatment'.
   */
  function getVariant() {
    const existing = getCookie(VARIANT_COOKIE);
    if (existing) return existing;
    const variant = Math.random() < 0.5 ? 'control' : 'treatment';
    setCookie(VARIANT_COOKIE, variant, VARIANT_TTL_DAYS);
    return variant;
  }

  /**
   * Persists an event to localStorage.
   * @param {string} name - Event name (e.g., 'impression', 'popup_shown', 'cta_click', 'demo_booked').
   * @param {object} [details]
   */
  function trackEvent(name, details = {}) {
    const payload = { name, timestamp: new Date().toISOString(), details };
    const existing = JSON.parse(localStorage.getItem(EVENT_STORAGE_KEY) || '[]');
    existing.push(payload);
    localStorage.setItem(EVENT_STORAGE_KEY, JSON.stringify(existing));
  }

  /**
   * Checks if the current user is a paid customer.
   * Placeholder implementation – looks for a 'paid_user' cookie.
   */
  function isPaidUser() {
    return !!getCookie('paid_user');
  }

  /**
   * Checks if the user has already booked a demo in this session.
   * We store a flag in localStorage named 'demo_booked'.
   */
  function hasBookedDemo() {
    return localStorage.getItem('demo_booked') === 'true';
  }

  // Expose helpers globally so other scripts (exit‑intent.js, popup‑component.js) can use them.
  window.getDemoVariant = getVariant;
  window.trackDemoEvent = trackEvent;
  window.isPaidUser = isPaidUser;
  window.hasBookedDemo = hasBookedDemo;
})();