const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Request failed with ${response.status}`);
  }

  return response.json();
}

export const api = {
  health: () => request("/health"),
  ready: () => request("/ready"),
  dashboard: () => request("/dashboard"),
  products: () => request("/products"),
  createProduct: (payload) =>
    request("/products", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  customers: () => request("/customers"),
  createCustomer: (payload) =>
    request("/customers", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  orders: () => request("/orders"),
  createOrder: (payload) =>
    request("/orders", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  seed: () =>
    request("/admin/seed", {
      method: "POST"
    })
};
