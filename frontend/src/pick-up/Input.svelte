<script>
  // Props
  export let value = "",
  changeHandler;
</script>

<input
  type="search"
  placeholder="🚘 Мой автомобиль"
  class="newsletter__input"
  bind:value
  on:keyup={changeHandler}
/>
