export async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!response.ok) {
    let detail = `Request failed (${response.status}). Please try again.`;
    try {
      const body = await response.json();
      detail = Array.isArray(body.detail)
        ? body.detail.map((e) => `${e.loc.at(-1)}: ${e.msg}`).join("; ")
        : body.detail || detail;
    } catch {
      /* Preserve a useful error for non-JSON proxy failures. */
    }
    throw new Error(detail);
  }
  return response.status === 204 ? null : response.json();
}

export async function allProducts() {
  const result = [];
  for (let offset = 0; ; offset += 500) {
    const page = await api(`/products?limit=500&offset=${offset}`);
    result.push(...page);
    if (page.length < 500) return result;
  }
}

export const stockStatus = (p) =>
  p.stock_quantity === 0
    ? "out"
    : p.stock_quantity <= p.reorder_threshold
      ? "low"
      : "healthy";
export const statusText = {
  healthy: "In stock",
  low: "Low stock",
  out: "Out of stock",
};
export const money = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(value));
export const number = (value) => new Intl.NumberFormat("en-IN").format(value);
export function csvCell(value) {
  const text = String(value ?? "");
  // Avoid spreadsheet formula execution when exporting user-controlled strings.
  return `"${(/^[=+@\-\t\r]/.test(text) ? "'" : "") + text.replaceAll('"', '""')}"`;
}
