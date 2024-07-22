export const debounce = (delay, func) => {
  let inDebounce;

  return args => {
    clearTimeout(inDebounce);
    inDebounce = setTimeout(func, delay, args);
  }
}
