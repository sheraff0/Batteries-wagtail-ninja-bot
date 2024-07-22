export const withFullName = (data, item) => ({
  ...item,
  full_name: [
    data.full_name, item.name
  ].join(" - ")
})
