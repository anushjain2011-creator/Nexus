/*
 * Nexus Dashboard — polls the FastAPI server's /api/world endpoint and
 * renders the live WorldModel: tasks, budget, risks, knowledge, and a
 * scrolling ticker of EventBus activity (the signature element — it's
 * what makes the "cascading, connected system" concept visible instead
 * of just claimed in the pitch).
 */

import { useEffect, useState, useCallback } from 'react';
import './tokens.css';
import './dashboard.css';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const POLL_INTERVAL_MS = 2500;

function useWorldState() {
  const [world, setWorld] = useState(null);
  const [online, setOnline] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/world`);
      if (!res.ok) throw new Error(`status ${res.status}`);
      const data = await res.json();
      setWorld(data);
      setOnline(true);
    } catch {
      setOnline(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [refresh]);

  return { world, online, refresh };
}

function StatRow({ world }) {
  const taskCount = world?.tasks?.length ?? 0;
  const doneCount = world?.tasks?.filter((t) => t.status === 'done').length ?? 0;
  const highRisks = world?.risks?.filter((r) => r.severity === 'high').length ?? 0;
  const spent = world?.budget_spent ?? 0;
  const total = world?.budget_total ?? 0;
  const pct = total > 0 ? Math.min(100, (spent / total) * 100) : 0;
  const over = total > 0 && spent > total;

  return (
    <div className="stat-row">
      <div className="stat">
        <div className="stat-label">Tasks</div>
        <div className="stat-value">{doneCount}/{taskCount}</div>
      </div>
      <div className="stat">
        <div className="stat-label">High-severity risks</div>
        <div className={`stat-value ${highRisks > 0 ? 'risk' : ''}`}>{highRisks}</div>
      </div>
      <div className="stat">
        <div className="stat-label">Budget</div>
        <div className="stat-value">
          ${spent.toFixed(0)}<span style={{ color: 'var(--text-faint)' }}> / ${total.toFixed(0)}</span>
        </div>
        <div className="budget-bar">
          <div
            className={`budget-bar-fill ${over ? 'over' : ''}`}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </div>
  );
}

function TaskList({ tasks }) {
  if (!tasks || tasks.length === 0) {
    return <div className="empty-state">No tasks yet — set a goal above to generate a plan.</div>;
  }
  return (
    <div className="task-list">
      {tasks.map((t) => (
        <div className="task-row" key={t.id}>
          <span className={`task-status-dot ${t.status}`} title={t.status} />
          <span className="task-title" title={t.title}>{t.title}</span>
          <span className="task-owner">{t.owner || '—'}</span>
          <span className="task-cost">{t.cost ? `$${t.cost}` : ''}</span>
        </div>
      ))}
    </div>
  );
}

function RiskList({ risks }) {
  if (!risks || risks.length === 0) {
    return <div className="empty-state">No risks logged.</div>;
  }
  return (
    <div>
      {risks.map((r) => (
        <div className={`risk-row ${r.severity}`} key={r.id}>
          <div className="risk-body">
            <div className="risk-desc">{r.description}</div>
            {r.mitigation && <div className="risk-mitigation">→ {r.mitigation}</div>}
          </div>
          <span className={`risk-severity ${r.severity}`}>{r.severity}</span>
        </div>
      ))}
    </div>
  );
}

function KnowledgeList({ knowledge }) {
  if (!knowledge || knowledge.length === 0) {
    return <div className="empty-state">No findings recorded.</div>;
  }
  return (
    <div>
      {knowledge.slice().reverse().map((k, i) => (
        <div className="knowledge-row" key={i}>
          <div>{k.note}</div>
          {k.source && <div className="knowledge-source">{k.source}</div>}
        </div>
      ))}
    </div>
  );
}

function Ticker({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="ticker">
        <div className="ticker-empty">Waiting for agent activity…</div>
      </div>
    );
  }
  // duplicate the list so the CSS scroll loop is seamless
  const loop = [...events, ...events];
  return (
    <div className="ticker">
      <div className="ticker-track">
        {loop.map((e, i) => (
          <span className="ticker-item" key={i}>
            <span className="ticker-dot" />
            <span className="ticker-kind">{e.kind}</span>
            <span>{summarizePayload(e.payload)}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

function summarizePayload(payload) {
  if (!payload) return '';
  const entries = Object.entries(payload).slice(0, 2);
  return entries.map(([k, v]) => `${k}=${v}`).join(' ');
}

export default function App() {
  const { world, online, refresh } = useWorldState();
  const [goal, setGoal] = useState('Build a robotics startup with 4 people and a $5,000 budget');
  const [busy, setBusy] = useState(false);
  const [eventInput, setEventInput] = useState('');

  async function handleBootstrap(e) {
    e.preventDefault();
    if (!goal.trim()) return;
    setBusy(true);
    try {
      await fetch(`${API_BASE}/api/bootstrap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, deadline: '30 days', budget: 5000 }),
      });
      await refresh();
    } finally {
      setBusy(false);
    }
  }

  async function handleTriggerEvent() {
    if (!eventInput.trim()) return;
    setBusy(true);
    try {
      await fetch(`${API_BASE}/api/event`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: eventInput }),
      });
      setEventInput('');
      await refresh();
    } finally {
      setBusy(false);
    }
  }

  async function handleReset() {
    setBusy(true);
    try {
      await fetch(`${API_BASE}/api/reset`, { method: 'POST' });
      await refresh();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">NEXUS</span>
          <span className="brand-sub">execution operating system</span>
        </div>

        <form className="goal-form" onSubmit={handleBootstrap}>
          <input
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="Describe a goal to bootstrap a project…"
          />
          <button className="btn primary" type="submit" disabled={busy}>
            {busy ? 'Running…' : 'Run'}
          </button>
        </form>

        <span className="status-pill">
          <span className={`status-dot ${online ? '' : 'offline'}`} />
          {online ? 'connected' : 'server offline'}
        </span>
      </header>

      <main className="main">
        <section className="column">
          <StatRow world={world} />

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Execution graph</span>
              <span className="panel-count">{world?.tasks?.length ?? 0} tasks</span>
            </div>
            <TaskList tasks={world?.tasks} />
          </div>

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Inject a problem</span>
            </div>
            <div className="goal-form" style={{ flexWrap: 'nowrap' }}>
              <input
                value={eventInput}
                onChange={(e) => setEventInput(e.target.value)}
                placeholder="e.g. Our hardware supplier just failed"
              />
              <button className="btn" onClick={handleTriggerEvent} disabled={busy}>
                Trigger
              </button>
            </div>
          </div>
        </section>

        <section className="column">
          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Risks</span>
              <span className="panel-count">{world?.risks?.length ?? 0}</span>
            </div>
            <RiskList risks={world?.risks} />
          </div>

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Knowledge</span>
              <span className="panel-count">{world?.knowledge?.length ?? 0}</span>
            </div>
            <KnowledgeList knowledge={world?.knowledge} />
          </div>

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Session</span>
            </div>
            <button className="btn danger" onClick={handleReset} disabled={busy}>
              Reset project
            </button>
          </div>
        </section>
      </main>

      <Ticker events={world?.events} />
    </div>
  );
}
