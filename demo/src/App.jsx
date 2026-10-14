import { useState } from "react";

import Counterpanel from "./assets/Components/Counterpanel.jsx";
import SecondCounterpanel from "./assets/Components/SecondCounterpanel.jsx";
import Helppanel from "./assets/Components/Helppanel.jsx";
import Taskmanager from "./assets/Components/Taskmanager.jsx";

import "./App.css";

function App() {
  const [resetSignal, setResetSignal] = useState(0);

  const resetBothCounters = () => {
    setResetSignal((previous) => previous + 1);
  };

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <p className="eyebrow">
          REACT HANDS-ON ASSIGNMENT
        </p>

        <h1>Personal Productivity Dashboard</h1>

        <p>
          Practise reusable logic with React Custom Hooks.
        </p>
      </header>

      <div className="counter-grid">
        <Counterpanel resetSignal={resetSignal} />

        <SecondCounterpanel
          resetSignal={resetSignal}
        />
      </div>

      <div className="global-reset">
        <button
          className="danger"
          onClick={resetBothCounters}
        >
          Reset Both Counters
        </button>
      </div>

      <div className="help-grid">
        <Helppanel
          title="Help Panel"
          message="Custom hooks help us reuse React logic across components."
        />

        <Helppanel
          title="Productivity Tips"
          message="Break large tasks into smaller steps and track your progress."
        />
      </div>

      <Taskmanager />

      <footer className="dashboard-footer">
        Built with React Function Components and Custom Hooks
      </footer>
    </main>
  );
}

export default App;
