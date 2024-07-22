<script>
  import BatteriesLink from "./BatteriesLink.svelte";
  // Props
  export let data = {},
    className = "";
  // Handlers
  const toggleFold = () => (data.fold = !data.fold);
</script>

{#if data.battery_params}
  <BatteriesLink {data} {className} />
{:else}
  <button on:click={toggleFold} class={className}>
    {data.full_name || data.name}
    <span> {data.fold ? '▾' : '▴'}</span>
  </button>
  {#if !data.fold}
    <slot />
  {/if}
{/if}
