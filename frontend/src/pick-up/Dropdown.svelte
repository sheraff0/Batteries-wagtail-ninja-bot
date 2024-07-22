<script>
  import CarModel from "./CarModel.svelte";
  // Props
  export let data = [];
</script>

<div class="pick-up__dropdown{!!data ? ' show' : ''}">
  {#each data as carModel}
    <CarModel data={carModel} />
  {/each}
</div>

<style>
  .pick-up__dropdown {
    max-height: 80vh;
    overflow: auto;
  }
</style>