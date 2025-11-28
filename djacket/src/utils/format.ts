export function formatDate(dateString: string | undefined): string {
  // Format a date string (ISO 8601) to "DD/MM/YYYY"
  if (!dateString) {
    return ""
  }
  const date = new Date(dateString)
  const day = String(date.getDate()).padStart(2, "0")
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const year = date.getFullYear()
  return `${day}/${month}/${year}`
}