
import { useEffect, useState } from "react";

export default function useCounter(initialValue = 0) {
  const getValidInitialValue = () => {
    const value = Number(initialValue);

    if (!Number.isFinite(value) || value < 0) {
      return 0;
    }

    return value;
  };

  


  const [count, setCount] = useState(getValidInitialValue);
    

  const increment = () => {
    
    setCount((previousCount) => previousCount + 1);
  };

  const decrement = () => {
    
    setCount((previousCount) =>
      Math.max(0, previousCount - 1)
    );
  };

  const reset = () => {
    
    setCount(0);
  };

  return {
    count,
    increment,
    decrement,
    reset,
  };
}
