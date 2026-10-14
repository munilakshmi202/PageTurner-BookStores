
import { useState } from "react";

export default function useToggle(initialValue = false) {
  const [isVisible, setIsVisible] = useState(initialValue);

  const toggle = () => {
    setIsVisible((previousValue) => !previousValue);
  };

  return {
    isVisible,
    toggle,
  };
}
