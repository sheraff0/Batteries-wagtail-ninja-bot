<script>
  // Props
  export let data = {}, className = "";
  $: bp = data.battery_params;
  $: params = new URLSearchParams({
    section: "1",
    ...(bp.type ? {case_format: bp.type} : {}),
    ...(bp.polarity ? {polarity: bp.polarity} : {}),
    capacity__gte: bp.capacity.min,
    capacity__lte: bp.capacity.max,
    current__gte: bp.current.min,
    current__lte: bp.current.max,
    length__gte: bp.length.min,
    length__lte: bp.length.max,
    width__gte: bp.width.min,
    width__lte: bp.width.max,
    height__gte: bp.height.min,
    height__lte: bp.height.max,
    search_for: data.full_name,
  });
  // Handlers
  const redirect = () => window.location.href = "/catalog?" + params;
</script>

<button
  class="link {className}"
  on:click={redirect}
>
  {data.full_name || data.name}
</button>
