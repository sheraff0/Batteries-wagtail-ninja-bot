<script>
  import Engine from "./Engine.svelte";
  import LinkOrUnfold from "./LinkOrUnfold.svelte";
  import { withFullName } from "../utils/text";
  // Props
  export let data = {};
</script>

<LinkOrUnfold {data} className="generation">
  <div class="engines">
    {#each data.engines || [] as engine}
      <Engine data={withFullName(data, engine)} />
    {/each}
  </div>
</LinkOrUnfold>
