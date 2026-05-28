// stats-dashboard.js – Shows a tiny widget with conversion metrics from localStorage events.
// The widget is injected at the bottom‑right of the page and updates live when new events are tracked.

(function () {
  const STORAGE_KEY = 'exit_intent_events';
  const WIDGET_ID = 'exit-intent-stats-widget';

  function getEvents() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch (e) {
      return [];
    }
  }

  function calculateMetrics(events) {
    const counts = { impression: 0, popup_shown: 0, cta_click: 0, demo_booked: 0 };
    events.forEach(ev => {
      if (counts.hasOwnProperty(ev.name)) counts[ev.name]++;
    });
    const rates = {};
    if (counts.impression) {
      rates.popupRate = ((counts.popup_shown / counts.impression) * 100).toFixed(1);
      rates.ctaRate = ((counts.cta_click / counts.impression) * 100).toFixed(1);
      rates.demoRate = ((counts.demo_booked / counts.impression) * 100).toFixed(1);
    }
    return { counts, rates };
  }

  function render() {
    const events = getEvents();
    const { counts, rates } = calculateMetrics(events);
    let widget = document.getElementById(WIDGET_ID);
    if (!widget) {
      widget = document.createElement('div');
      widget.id = WIDGET_ID;
      widget.className = 'exit-intent-stats-widget';
      document.body.appendChild(widget);
    }
    widget.innerHTML = `
      <strong>Exit‑Intent Demo Funnel</strong><br/>
      Impressions: ${counts.impression}<br/>
      Popups shown: ${counts.popup_shown} (${rates.popupRate || 0}% )<br/>
      CTA clicks: ${counts.cta_click} (${rates.ctaRate || 0}% )<br/>
      Demo booked: ${counts.demo_booked} (${rates.demoRate || 0}% )`;
  }

  // Re‑render every 5 seconds to catch new events.
  render();
  setInterval(render, 5000);
})();