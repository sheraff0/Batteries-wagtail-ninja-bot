<script>
  import Generation from "./Generation.svelte";
  import LinkOrUnfold from "./LinkOrUnfold.svelte";
  import { withFullName } from "../utils/text";
  // Props
  export let data = {};
</script>

<div class="pick-up--container">
  <LinkOrUnfold {data} className="model">
    <div class="generations">
      {#each data.generations || [] as generation}
        <Generation data={withFullName(data, generation)} />
      {/each}
    </div>
  </LinkOrUnfold>
</div>

<style>
  :global(.pick-up--container button) {
    background-color: transparent;
    display: block;
    color: var(--title-color);
  }

  :global(.pick-up--container button.model) {
    font-weight: 600;
  }

  :global(.pick-up--container button.link) {
    color: var(--first-color);
  }

  :global(.pick-up--container .generations) {
    margin-left: 1rem;
    font-size: 90%;
  }

  :global(.pick-up--container .engines) {
    margin-left: 1rem;
  }

  :global(button.engine) {
    display: inline-block;
  }

  :global(button.engine:before) {
    content: "• ";
    margin-left: 0.5rem;
  }
</style>
