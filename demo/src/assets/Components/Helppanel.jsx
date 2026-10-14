
import useToggle  from "../hooks/useToggele";

export default function Helppanel({
  title = "Help Panel",
  message = "Custom hooks help us reuse React logic across components.",
}) {
  const { isVisible, toggle } = useToggle(false);

  return (
    <section className="panel">
      <h2>{title}</h2>

      <button onClick={toggle}>
        {isVisible ? "Hide Help" : "Show Help"}
      </button>

      {isVisible && (
        <p className="help-message">{message}</p>
      )}
    </section>
  );
}
