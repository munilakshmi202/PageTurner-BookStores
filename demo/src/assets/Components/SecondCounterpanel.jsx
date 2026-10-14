
import { useEffect } from "react";
import useCounter from "../hooks/useCounter";

export default function SecondCounterpanel({
  resetSignal,
  initialValue = 0,
}) {
  const { count, increment, decrement, reset } =
    useCounter(initialValue);

  useEffect(() => {
    reset();
  }, [resetSignal]);

  return (
    <section className="panel">
      <h2>Counter Panel Two</h2>

      <p className="counter-value">{count}</p>

      <div className="button-row">
        <button onClick={increment}>Increase</button>

        <button onClick={decrement} className="secondary">
          Decrease
        </button>

        <button onClick={reset} className="danger">
          Reset
        </button>
      </div>
    </section>
  );
}
