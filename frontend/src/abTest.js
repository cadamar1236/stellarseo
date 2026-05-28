// abTest.js – helper for A/B variant handling and event tracking

/**
 * Get the current variant for the user.
 * Uses a cookie named 'demo_position_variant' that persists for 30 days.
 * If the cookie does not exist, a random 50/50 assignment is made.
 * Returns 'control' or 'treatment'.
 */
export function getVariant() {
  const cookieName = 'demo_position_variant';
  const match = document.cookie.match(new RegExp('(?:^|; )' + cookieName + '=([^;]*)'));
  if (match) {
    return decodeURIComponent(match[1]);
  }
  // no cookie – assign randomly
  const variant = Math.random() < 0.5 ? 'control' : 'treatment';
  // set cookie for 30 days
  const expires = new Date();
  expires.setTime(expires.getTime() + 30 * 24 * 60 * 60 * 1000);
  document.cookie = `${cookieName}=${encodeURIComponent(variant)}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
  return variant;
}

/**
 * Track an event for the popup.
 * Events are stored in localStorage under the key 'demo_exit_popup_events'.
 * Each event is an object: { name, timestamp, details }.
 */
export function trackEvent(name, details = {}) {
  const storageKey = 'demo_exit_popup_events';
  const existing = JSON.parse(localStorage.getItem(storageKey) || '[]');
  existing.push({ name, timestamp: new Date().toISOString(), details });
  localStorage.setItem(storageKey, JSON.stringify(existing));
}

/**
 * Helper to check whether the user has already booked a demo.
 * In a real system this would come from backend/user profile.
 * Here we simply look for a flag in localStorage.
 */
export function hasBookedDemo() {
  return localStorage.getItem('demo_booked') === 'true';
}

/**
 * Helper to check whether the user is a paid customer.
 * Placeholder – always returns false for now.
 */
export function isPaidUser() {
  // TODO: replace with real check
  return false;
}