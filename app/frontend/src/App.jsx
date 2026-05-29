import { useEffect, useMemo, useState } from "react";
import { api } from "./api";

const tabs = ["Dashboard", "Products", "Customers", "Orders", "Health"];

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <p>{label}</p>
      <h3>{value}</h3>
    </div>
  );
}

function ErrorBanner({ error, onClose }) {
  if (!error) return null;
  return (
    <div className="error-banner">
      <span>{error}</span>
      <button onClick={onClose}>Dismiss</button>
    </div>
  );
}

function Dashboard({ data, onSeed }) {
  return (
    <section>
      <div className="section-heading">
        <div>
          <h2>Operations Dashboard</h2>
          <p>Business summary for retail, inventory, and order operations.</p>
        </div>
        <button onClick={onSeed}>Seed Demo Data</button>
      </div>

      <div className="stats-grid">
        <StatCard label="Products" value={data?.products ?? 0} />
        <StatCard label="Customers" value={data?.customers ?? 0} />
        <StatCard label="Orders" value={data?.orders ?? 0} />
        <StatCard label="Low Stock" value={data?.low_stock_products ?? 0} />
        <StatCard label="Revenue" value={`₹${Number(data?.total_revenue ?? 0).toFixed(2)}`} />
        <StatCard label="Pending Orders" value={data?.pending_orders ?? 0} />
      </div>
    </section>
  );
}

function Products({ products, onCreate }) {
  const [form, setForm] = useState({
    sku: "",
    name: "",
    category: "",
    unit_price: "",
    stock_quantity: ""
  });

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    await onCreate({
      sku: form.sku,
      name: form.name,
      category: form.category || null,
      unit_price: Number(form.unit_price),
      stock_quantity: Number(form.stock_quantity)
    });
    setForm({ sku: "", name: "", category: "", unit_price: "", stock_quantity: "" });
  }

  return (
    <section>
      <div className="section-heading">
        <div>
          <h2>Product Management</h2>
          <p>Add products and track current stock.</p>
        </div>
      </div>

      <form className="form-grid" onSubmit={submit}>
        <input placeholder="SKU" value={form.sku} onChange={(e) => update("sku", e.target.value)} required />
        <input placeholder="Product name" value={form.name} onChange={(e) => update("name", e.target.value)} required />
        <input placeholder="Category" value={form.category} onChange={(e) => update("category", e.target.value)} />
        <input placeholder="Unit price" type="number" min="1" value={form.unit_price} onChange={(e) => update("unit_price", e.target.value)} required />
        <input placeholder="Stock quantity" type="number" min="0" value={form.stock_quantity} onChange={(e) => update("stock_quantity", e.target.value)} required />
        <button type="submit">Add Product</button>
      </form>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.sku}</td>
                <td>{product.name}</td>
                <td>{product.category || "-"}</td>
                <td>₹{Number(product.unit_price).toFixed(2)}</td>
                <td>
                  <span className={product.stock_quantity <= 5 ? "badge danger" : "badge"}>
                    {product.stock_quantity}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Customers({ customers, onCreate }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    address: ""
  });

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    await onCreate({
      name: form.name,
      email: form.email || null,
      phone: form.phone || null,
      address: form.address || null
    });
    setForm({ name: "", email: "", phone: "", address: "" });
  }

  return (
    <section>
      <div className="section-heading">
        <div>
          <h2>Customer Management</h2>
          <p>Create and review customer records.</p>
        </div>
      </div>

      <form className="form-grid" onSubmit={submit}>
        <input placeholder="Customer name" value={form.name} onChange={(e) => update("name", e.target.value)} required />
        <input placeholder="Email" type="email" value={form.email} onChange={(e) => update("email", e.target.value)} />
        <input placeholder="Phone" value={form.phone} onChange={(e) => update("phone", e.target.value)} />
        <input placeholder="Address" value={form.address} onChange={(e) => update("address", e.target.value)} />
        <button type="submit">Add Customer</button>
      </form>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td>{customer.name}</td>
                <td>{customer.email || "-"}</td>
                <td>{customer.phone || "-"}</td>
                <td>{customer.address || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Orders({ orders, customers, products, onCreate }) {
  const [form, setForm] = useState({
    customer_id: "",
    product_id: "",
    quantity: "1"
  });

  const availableProducts = useMemo(
    () => products.filter((product) => product.stock_quantity > 0),
    [products]
  );

  function update(key, value) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    await onCreate({
      customer_id: Number(form.customer_id),
      items: [
        {
          product_id: Number(form.product_id),
          quantity: Number(form.quantity)
        }
      ]
    });
    setForm({ customer_id: "", product_id: "", quantity: "1" });
  }

  return (
    <section>
      <div className="section-heading">
        <div>
          <h2>Order Management</h2>
          <p>Create orders and automatically reduce product stock.</p>
        </div>
      </div>

      <form className="form-grid" onSubmit={submit}>
        <select value={form.customer_id} onChange={(e) => update("customer_id", e.target.value)} required>
          <option value="">Select customer</option>
          {customers.map((customer) => (
            <option key={customer.id} value={customer.id}>{customer.name}</option>
          ))}
        </select>

        <select value={form.product_id} onChange={(e) => update("product_id", e.target.value)} required>
          <option value="">Select product</option>
          {availableProducts.map((product) => (
            <option key={product.id} value={product.id}>
              {product.name} — Stock: {product.stock_quantity}
            </option>
          ))}
        </select>

        <input placeholder="Quantity" type="number" min="1" value={form.quantity} onChange={(e) => update("quantity", e.target.value)} required />
        <button type="submit">Create Order</button>
      </form>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer ID</th>
              <th>Status</th>
              <th>Total</th>
              <th>Items</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td>{order.customer_id}</td>
                <td><span className="badge">{order.status}</span></td>
                <td>₹{Number(order.total_amount).toFixed(2)}</td>
                <td>{order.items?.length ?? 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Health({ health, ready }) {
  return (
    <section>
      <div className="section-heading">
        <div>
          <h2>Platform Health</h2>
          <p>Endpoints useful for Docker health checks, Kubernetes probes, monitoring, and uptime checks.</p>
        </div>
      </div>

      <div className="health-grid">
        <div className="health-card">
          <h3>/health</h3>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </div>
        <div className="health-card">
          <h3>/ready</h3>
          <pre>{JSON.stringify(ready, null, 2)}</pre>
        </div>
      </div>
    </section>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState("Dashboard");
  const [dashboard, setDashboard] = useState(null);
  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [health, setHealth] = useState(null);
  const [ready, setReady] = useState(null);
  const [error, setError] = useState("");

  async function loadAll() {
    try {
      setError("");
      const [dashboardData, productsData, customersData, ordersData, healthData] = await Promise.all([
        api.dashboard(),
        api.products(),
        api.customers(),
        api.orders(),
        api.health()
      ]);

      setDashboard(dashboardData);
      setProducts(productsData);
      setCustomers(customersData);
      setOrders(ordersData);
      setHealth(healthData);

      try {
        setReady(await api.ready());
      } catch (readyError) {
        setReady({ status: "not_ready", detail: readyError.message });
      }
    } catch (loadError) {
      setError(loadError.message);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  async function withRefresh(action) {
    try {
      setError("");
      await action();
      await loadAll();
    } catch (actionError) {
      setError(actionError.message);
    }
  }

  return (
    <main>
      <header className="hero">
        <div>
          <p className="eyebrow">LegacyOps 2026 Workload</p>
          <h1>Legacy Retail Operations System</h1>
          <p className="subtitle">
            A simple retail app for DevOps modernization: deploy it, monitor it, secure it, back it up, and recover it.
          </p>
        </div>
        <button onClick={loadAll}>Refresh</button>
      </header>

      <ErrorBanner error={error} onClose={() => setError("")} />

      <nav className="tabs">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={activeTab === tab ? "active" : ""}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      {activeTab === "Dashboard" && (
        <Dashboard data={dashboard} onSeed={() => withRefresh(api.seed)} />
      )}

      {activeTab === "Products" && (
        <Products products={products} onCreate={(payload) => withRefresh(() => api.createProduct(payload))} />
      )}

      {activeTab === "Customers" && (
        <Customers customers={customers} onCreate={(payload) => withRefresh(() => api.createCustomer(payload))} />
      )}

      {activeTab === "Orders" && (
        <Orders
          orders={orders}
          customers={customers}
          products={products}
          onCreate={(payload) => withRefresh(() => api.createOrder(payload))}
        />
      )}

      {activeTab === "Health" && (
        <Health health={health} ready={ready} />
      )}
    </main>
  );
}
