export function clickOutside(node) {
  const handleClick = e => {
    if (node && !node.contains(e.target) && !e.defaultPrevented) {
      node.dispatchEvent(
        new CustomEvent("click_outside", node)
      )
    }
  }

  document.addEventListener("click", handleClick, true);

  return {
    destroy() {
      document.removeEventListener("click", handleClick, true);
    }
  }
}
