import PickUp from "./pick-up/PickUp.svelte"

const app = [
  "-header",
  "-body-1",
  "-body-2",
  "-body-3",
].map(
  suffix => document.getElementById(`node-pick-up${suffix}`)
).filter(
  target => !!target
).map(target => new PickUp({ target }))

export default app
