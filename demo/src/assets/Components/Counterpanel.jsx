
import { useEffect } from "react";
import useCounter from "../hooks/useCounter";

function Counterpanel({ resetSignal, initialValue = 0 }) {
  const { count, increment, decrement, reset } =
    useCounter(initialValue);

  // Reset this counter when the parent requests it
  useEffect(() => {
    reset();
  }, [resetSignal]);

  return (
    <section className="panel">
      <h2>Counter Panel One</h2>

      <p className="counter-value">{count}</p>

      <div className="button-row">
        <button onClick={increment}>
          Increase
        </button>

        <button
          onClick={decrement}
          className="secondary"
        >
          Decrease
        </button>

        <button
          onClick={reset}
          className="danger"
        >
          Reset
        </button>
      </div>
    </section>
  );
}

export default Counterpanel;

