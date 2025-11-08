import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function HistoryPanel({ refreshTrigger }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadEvents = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getEvents(10);
      setEvents(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, [refreshTrigger]);

  const formatDate = (dateString) => {
    // SQLite returns dates in format: "2025-11-08 22:26:31" (local time, not UTC)
    // We need to parse it correctly
    const date = new Date(dateString.replace(' ', 'T'));
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Przed chwilą';
    if (diffMins < 60) return `${diffMins} min temu`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)} godz. temu`;
    if (diffMins < 10080) return `${Math.floor(diffMins / 1440)} dni temu`;

    return date.toLocaleString('pl-PL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="history-panel">
      <h3>Historia zdarzeń</h3>

      {loading && <div className="loading">Ładowanie</div>}

      {error && <div className="error">Błąd: {error}</div>}

      {!loading && !error && events.length === 0 && (
        <div className="empty-state">Brak zdarzeń w historii</div>
      )}

      {!loading && !error && events.length > 0 && (
        <div>
          {events.map((event) => (
            <div key={event.id} className="event-item">
              <div className="event-time">{formatDate(event.created_at)}</div>
              <div className="event-description">{event.description}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
