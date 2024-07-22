<script>
  import { debounce } from "../utils/async";
  import { clickOutside } from "../utils/events";
  import Input from "./Input.svelte";
  import Dropdown from "./Dropdown.svelte";
  // Props
  export let value = "",
    data = [];
  // Handlers
  const updateList = debounce(250, async () => {
    const res = await fetch(
      "/api/akbmag/search?" +
        new URLSearchParams({
          q: value,
        }),
    );
    try {
      data = await res.json();
    } catch {
      data = [];
    }
  });
  const resetData = e => data = [];
</script>

<div use:clickOutside on:click_outside={resetData}>
  <Input bind:value changeHandler={updateList} />
  <Dropdown {data} />
</div>
