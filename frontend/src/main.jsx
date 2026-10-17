import { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowDownLeft,
  ArrowUpRight,
  ArrowRight,
  ArrowDownUp,
  Package,
  LayoutDashboard,
  History,
  TriangleAlert,
  Plus,
  Search,
  Download,
  RefreshCw,
  ChevronLeft,
  ChevronRight,
  X,
  Pencil,
  Trash2,
  SlidersHorizontal,
  Check,
  Box,
  ExternalLink,
  Menu,
  CircleHelp,
  Layers,
  IndianRupee,
} from "lucide-react";
import {
  api,
  allProducts,
  stockStatus,
  statusText,
  money,
  number,
  csvCell,
} from "./api";
import "./styles.css";

const navigation = [
  { id: "overview", label: "Overview", icon: LayoutDashboard },
  { id: "inventory", label: "All inventory", icon: Package },
  { id: "movements", label: "Stock movements", icon: ArrowDownUp },
  { id: "low", label: "Low stock", icon: TriangleAlert },
];
const stamp = (value) =>
  new Date(
    value.endsWith("Z") || /[+-]\d\d:\d\d$/.test(value) ? value : value + "Z",
  ).toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
const blank = {
  sku: "",
  name: "",
  category: "",
  selling_price: "",
  stock_quantity: 0,
  reorder_threshold: 10,
  description: "",
};

function App() {
  const [page, setPage] = useState("overview");
  const [products, setProducts] = useState([]),
    [stats, setStats] = useState(null),
    [movements, setMovements] = useState([]);
  const [loading, setLoading] = useState(true),
    [error, setError] = useState(""),
    [toast, setToast] = useState("");
  const [search, setSearch] = useState(""),
    [filter, setFilter] = useState("all"),
    [category, setCategory] = useState("all"),
    [tablePage, setTablePage] = useState(1);
  const [modal, setModal] = useState(null),
    [busy, setBusy] = useState(false),
    [formError, setFormError] = useState(""),
    [menu, setMenu] = useState(false);
  const [movementPage, setMovementPage] = useState(0),
    [movementLoading, setMovementLoading] = useState(false);

  const modalOpener = useRef(null);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const [items, summary, activity] = await Promise.all([
        allProducts(),
        api("/inventory/stats"),
        api("/inventory/movements?limit=50"),
      ]);
      setProducts(items);
      setStats(summary);
      setMovements(activity);
      setMovementPage(0);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    load();
  }, []);
  useEffect(() => {
    if (toast) {
      const timer = setTimeout(() => setToast(""), 4500);
      return () => clearTimeout(timer);
    }
  }, [toast]);

  function open(type, product) {
    if (!modal) modalOpener.current = document.activeElement;
    setModal({ type, product });
    setFormError("");
  }
  function close() {
    if (!busy) {
      setModal(null);
      setFormError("");
    }
  }
  function navigate(id) {
    setPage(id);
    setMenu(false);
    setSearch("");
    setFilter("all");
    setCategory("all");
    setTablePage(1);
  }
  async function save(event) {
    event.preventDefault();
    setBusy(true);
    setFormError("");
    const data = Object.fromEntries(new FormData(event.currentTarget));
    try {
      if (modal.type === "delete")
        await api(`/products/${modal.product.id}`, { method: "DELETE" });
      else if (modal.type === "adjust")
        await api("/inventory/adjustments", {
          method: "POST",
          body: JSON.stringify({
            product_id: modal.product.id,
            quantity_change:
              Number(data.quantity) * (data.direction === "out" ? -1 : 1),
            reason: data.reason,
          }),
        });
      else {
        data.selling_price = String(data.selling_price);
        data.reorder_threshold = Number(data.reorder_threshold);
        if (modal.type === "create")
          data.stock_quantity = Number(data.stock_quantity);
        await api(
          `/products${modal.type === "edit" ? "/" + modal.product.id : ""}`,
          {
            method: modal.type === "edit" ? "PUT" : "POST",
            body: JSON.stringify(data),
          },
        );
      }
      setToast(
        modal.type === "delete"
          ? "Product deleted. Stock history retained."
          : modal.type === "adjust"
            ? "Stock adjusted and recorded in the ledger."
            : "Product saved successfully.",
      );
      setModal(null);
      await load();
    } catch (e) {
      setFormError(e.message);
    } finally {
      setBusy(false);
    }
  }
  async function movementNext(direction) {
    const next = Math.max(0, movementPage + direction);
    setMovementLoading(true);
    try {
      setMovements(
        await api(`/inventory/movements?limit=50&offset=${next * 50}`),
      );
      setMovementPage(next);
    } catch (e) {
      setError(e.message);
    } finally {
      setMovementLoading(false);
    }
  }
  function exportInventory() {
    const rows = [
      [
        "SKU",
        "Name",
        "Category",
        "Selling price (INR)",
        "Stock",
        "Reorder threshold",
      ],
      ...products.map((p) => [
        p.sku,
        p.name,
        p.category,
        p.selling_price,
        p.stock_quantity,
        p.reorder_threshold,
      ]),
    ];
    const url = URL.createObjectURL(
      new Blob([rows.map((row) => row.map(csvCell).join(",")).join("\r\n")], {
        type: "text/csv;charset=utf-8;",
      }),
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = `stockpilot-inventory-${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    setToast("Inventory exported.");
  }
  const visible = products.filter((p) => {
    const s = stockStatus(p);
    return (
      (page !== "low" || s !== "healthy") &&
      (filter === "all" || s === filter) &&
      (category === "all" || p.category === category) &&
      `${p.name} ${p.sku} ${p.category}`
        .toLowerCase()
        .includes(search.toLowerCase())
    );
  });
  const pages = Math.max(1, Math.ceil(visible.length / 8)),
    current = Math.min(tablePage, pages);
  const categories = [...new Set(products.map((p) => p.category))].sort();
  const title =
    page === "overview"
      ? "Inventory overview"
      : page === "inventory"
        ? "All inventory"
        : page === "low"
          ? "Reorder watchlist"
          : "Stock movements";

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <aside className={`sidebar ${menu ? "mobile-open" : ""}`}>
        <a
          className="brand"
          href="#"
          onClick={(e) => {
            e.preventDefault();
            navigate("overview");
          }}
        >
          <span className="brand-symbol">
            <Package size={24} />
          </span>
          <span>
            StockPilot<span className="brand-dot">.</span>
          </span>
        </a>
        <div className="workspace">
          <div className="workspace-avatar">S</div>
          <div>
            <strong>StockPilot workspace</strong>
            <span>Inventory operations</span>
          </div>
          <Layers size={15} />
        </div>
        <p className="nav-label">WORKSPACE</p>
        <nav aria-label="Main navigation">
          {navigation.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              aria-current={page === id ? "page" : undefined}
              className={page === id ? "active" : ""}
              onClick={() => navigate(id)}
            >
              <Icon size={18} />
              <span>{label}</span>
              {id === "low" && stats && <small>{stats.low_stock_count}</small>}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="side-note">
            <span className="note-icon">
              <Box size={21} />
            </span>
            <strong>A little clarity. A lot of control.</strong>
            <p>
              Every item accounted for.
              <br />
              Every movement recorded.
            </p>
            <button onClick={() => open("help")}>
              Your quick guide <ArrowRight size={14} />
            </button>
          </div>
          <div className="workspace-footer">
            <span className="avatar">SO</span>
            <div>
              <strong>Store operations</strong>
              <span>StockPilot · v1.0</span>
            </div>
          </div>
        </div>
      </aside>
      {menu && (
        <button
          className="nav-scrim"
          aria-label="Close navigation"
          onClick={() => setMenu(false)}
        />
      )}
      <div className="main-shell">
        <header className="topbar">
          <div className="breadcrumb">
            <button
              className="mobile-toggle icon-button"
              aria-label="Open navigation"
              onClick={() => setMenu(true)}
            >
              <Menu size={20} />
            </button>
            <span>Workspace</span>
            <ChevronRight size={13} />
            <strong>{page === "overview" ? "Overview" : title}</strong>
          </div>
          <div className="topbar-right">
            <span
              className={`connection ${error ? "offline" : loading ? "pending" : ""}`}
            >
              <i />
              {error
                ? "Connection issue"
                : loading
                  ? "Syncing inventory"
                  : "Connected to database"}
            </span>
            <button
              className="icon-button"
              aria-label="Open quick guide"
              onClick={() => open("help")}
            >
              <CircleHelp size={19} />
            </button>
            <span className="avatar small">SO</span>
          </div>
        </header>
        <main id="main">
          <div className="page-heading">
            <div>
              <div className="eyebrow">YOUR INVENTORY, IN FOCUS</div>
              <h1>{title}</h1>
              <p>
                {page === "movements"
                  ? "A reliable record of every unit in and out."
                  : page === "low"
                    ? "Keep your shelves ready for what’s next."
                    : "A clear view of your stock. A better way to keep it moving."}
              </p>
            </div>
            <div className="heading-actions">
              <button
                className="button"
                disabled={loading || !!error}
                aria-label="Export" onClick={exportInventory}
              >
                <Download size={16} />
                <span>Export</span>
              </button>
              <button
                className="button primary"
                disabled={loading || !!error}
                onClick={() => open("create")}
              >
                <Plus size={17} />
                Add product
              </button>
            </div>
          </div>
          {error && (
            <div className="error-banner" role="alert">
              <TriangleAlert size={19} />
              <div>
                <strong>Couldn’t sync your inventory</strong>
                <p>{error} Previously loaded information may be out of date.</p>
              </div>
              <button className="button" onClick={load}>
                Try again
              </button>
            </div>
          )}
          {page !== "movements" && (
            <section className="kpi-grid" aria-label="Inventory summary">
              <Kpi
                label="Total products"
                value={stats ? number(stats.total_products) : "—"}
                icon={Package}
                caption={`${stats ? number(stats.total_units) : "—"} units across all categories`}
                color="green"
                loading={loading}
              />
              <Kpi
                label="Inventory value"
                value={stats ? money(stats.inventory_value) : "—"}
                icon={IndianRupee}
                caption="At current selling prices"
                color="blue"
                loading={loading}
              />
              <Kpi
                label="Low-stock items"
                value={stats ? number(stats.low_stock_count) : "—"}
                icon={TriangleAlert}
                caption={`${stats ? stats.out_of_stock_count : "—"} out of stock · review your watchlist`}
                color="amber"
                loading={loading}
                onClick={() => navigate("low")}
              />
              <Kpi
                label="Stock movements"
                value={
                  stats
                    ? number(stats.inbound_units + stats.outbound_units)
                    : "—"
                }
                icon={ArrowDownUp}
                caption={`${stats ? number(stats.inbound_units) : "—"} in · ${stats ? number(stats.outbound_units) : "—"} out this week`}
                color="purple"
                loading={loading}
              />
            </section>
          )}
          {page === "overview" && (
            <section className="insight-grid">
              <MovementChart trend={stats?.movement_trend || []} />
              <div className="panel category-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Stock by category</h2>
                    <p>Where your inventory lives</p>
                  </div>
                  <span className="subtle-icon">
                    <Layers size={17} />
                  </span>
                </div>
                <CategoryChart categories={stats?.categories || []} />
              </div>
            </section>
          )}
          {page !== "movements" ? (
            <section className="panel inventory-panel">
              <div className="panel-heading">
                <div>
                  <h2>
                    {page === "low"
                      ? "Your reorder watchlist"
                      : "Product inventory"}{" "}
                    <span className="count-pill">{visible.length}</span>
                  </h2>
                  <p>
                    {page === "low"
                      ? "Products at or below their reorder threshold."
                      : "Your catalog, quantities, and stock health in one place."}
                  </p>
                </div>
                <button
                  className="icon-button"
                  onClick={load}
                  aria-label="Refresh inventory"
                  disabled={loading}
                >
                  <RefreshCw size={17} className={loading ? "spinning" : ""} />
                </button>
              </div>
              <div className="table-toolbar">
                <div
                  className="filter-tabs"
                  role="group"
                  aria-label="Stock status"
                >
                  {["all", "healthy", "low", "out"].map((s) => (
                    <button
                      key={s}
                      className={filter === s ? "selected" : ""}
                      onClick={() => {
                        setFilter(s);
                        setTablePage(1);
                      }}
                    >
                      {s === "all" ? "All products" : statusText[s]}
                    </button>
                  ))}
                </div>
                <div className="table-search">
                  <label className="search-input">
                    <Search size={16} />
                    <input
                      aria-label="Search inventory"
                      value={search}
                      onChange={(e) => {
                        setSearch(e.target.value);
                        setTablePage(1);
                      }}
                      placeholder="Search products or SKU…"
                    />
                  </label>
                  <label className="category-select">
                    <SlidersHorizontal size={15} />
                    <select
                      aria-label="Filter category"
                      value={category}
                      onChange={(e) => {
                        setCategory(e.target.value);
                        setTablePage(1);
                      }}
                    >
                      <option value="all">All categories</option>
                      {categories.map((c) => (
                        <option key={c}>{c}</option>
                      ))}
                    </select>
                  </label>
                </div>
              </div>
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Category</th>
                      <th>Price</th>
                      <th>Stock level</th>
                      <th>Status</th>
                      <th>
                        <span className="sr-only">Actions</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {!loading &&
                      visible.slice((current - 1) * 8, current * 8).map((p) => (
                        <tr key={p.id}>
                          <td>
                            <div className="product-cell">
                              <span
                                className={`product-icon tone-${p.category.length % 4}`}
                              >
                                <Package size={20} />
                              </span>
                              <div>
                                <button
                                  className="product-name"
                                  onClick={() => open("view", p)}
                                >
                                  {p.name}
                                </button>
                                <span className="sku">{p.sku}</span>
                              </div>
                            </div>
                          </td>
                          <td>
                            <span className="category-tag">{p.category}</span>
                          </td>
                          <td className="price">{money(p.selling_price)}</td>
                          <td>
                            <strong className="stock-number">
                              {number(p.stock_quantity)} <small>units</small>
                            </strong>
                            <div className="stock-track">
                              <i
                                className={stockStatus(p)}
                                style={{
                                  width: `${Math.min(100, (p.stock_quantity / Math.max(1, p.reorder_threshold * 4)) * 100)}%`,
                                }}
                              />
                            </div>
                          </td>
                          <td>
                            <span className={`badge ${stockStatus(p)}`}>
                              <i />
                              {statusText[stockStatus(p)]}
                            </span>
                          </td>
                          <td>
                            <div className="row-actions">
                              <button
                                aria-label={`Adjust ${p.name}`}
                                title="Adjust stock"
                                className="icon-button"
                                onClick={() => open("adjust", p)}
                              >
                                <ArrowDownUp size={16} />
                              </button>
                              <button
                                aria-label={`Edit ${p.name}`}
                                title="Edit product"
                                className="icon-button"
                                onClick={() => open("edit", p)}
                              >
                                <Pencil size={15} />
                              </button>
                              <button
                                aria-label={`Delete ${p.name}`}
                                title="Delete product"
                                className="icon-button danger-icon"
                                onClick={() => open("delete", p)}
                              >
                                <Trash2 size={15} />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
              {loading ? (
                <div className="empty-state">
                  <RefreshCw className="spinning" size={24} />
                  <h3>Syncing your inventory</h3>
                  <p>Fetching the latest products and stock balances.</p>
                </div>
              ) : !visible.length ? (
                <div className="empty-state">
                  <Package size={30} />
                  <h3>
                    {products.length
                      ? "No matching products"
                      : "Your next chapter starts here"}
                  </h3>
                  <p>
                    {products.length
                      ? "Try a different search or stock filter."
                      : "Add your first product to start tracking inventory."}
                  </p>
                  {!products.length && (
                    <button
                      className="button primary"
                      onClick={() => open("create")}
                    >
                      <Plus size={16} />
                      Add your first product
                    </button>
                  )}
                </div>
              ) : null}
              <div className="table-footer">
                <span>
                  Showing {visible.length ? (current - 1) * 8 + 1 : 0}–
                  {Math.min(current * 8, visible.length)} of {visible.length}{" "}
                  products
                </span>
                <div className="pagination">
                  <button
                    className="icon-button"
                    aria-label="Previous page"
                    disabled={current === 1}
                    onClick={() => setTablePage(current - 1)}
                  >
                    <ChevronLeft size={16} />
                  </button>
                  <span>
                    Page {current} of {pages}
                  </span>
                  <button
                    className="icon-button"
                    aria-label="Next page"
                    disabled={current === pages}
                    onClick={() => setTablePage(current + 1)}
                  >
                    <ChevronRight size={16} />
                  </button>
                </div>
              </div>
            </section>
          ) : (
            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>Inventory ledger</h2>
                  <p>
                    Opening balances and adjustments. History survives product
                    deletion.
                  </p>
                </div>
                <button
                  className="icon-button"
                  aria-label="Refresh movements"
                  onClick={load}
                >
                  <RefreshCw size={17} />
                </button>
              </div>
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Product / SKU</th>
                      <th>Change</th>
                      <th>Balance after</th>
                      <th>Reason</th>
                      <th>Recorded</th>
                    </tr>
                  </thead>
                  <tbody>
                    {movements.map((m) => (
                      <tr key={m.id}>
                        <td>
                          <strong>{m.product_name}</strong>
                          <span className="sku">
                            {m.sku}
                            {m.product_id === null ? " · Deleted product" : ""}
                          </span>
                        </td>
                        <td
                          className={
                            m.quantity_change > 0 ? "positive" : "negative"
                          }
                        >
                          {m.quantity_change > 0 ? "+" : ""}
                          {number(m.quantity_change)}
                        </td>
                        <td>{number(m.quantity_after)} units</td>
                        <td>{m.reason}</td>
                        <td className="nowrap">{stamp(m.created_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {!movements.length && (
                  <div className="empty-state">
                    <History size={28} />
                    <h3>No movements on this page</h3>
                    <p>Stock adjustments will appear here.</p>
                  </div>
                )}
              </div>
              <div className="table-footer">
                <span>Latest first · Page {movementPage + 1}</span>
                <div className="pagination">
                  <button
                    className="button"
                    disabled={!movementPage || movementLoading}
                    onClick={() => movementNext(-1)}
                  >
                    Previous
                  </button>
                  <button
                    className="button"
                    disabled={movements.length < 50 || movementLoading}
                    onClick={() => movementNext(1)}
                  >
                    Next
                  </button>
                </div>
              </div>
            </section>
          )}
          {page === "overview" && (
            <section className="panel activity-panel">
              <div className="panel-heading">
                <div>
                  <h2>Recent stock activity</h2>
                  <p>Every change has a story.</p>
                </div>
                <button
                  className="text-button"
                  onClick={() => navigate("movements")}
                >
                  View all movements <ArrowRight size={15} />
                </button>
              </div>
              <div className="activity-list">
                {movements.slice(0, 4).map((m) => (
                  <div className="activity-item" key={m.id}>
                    <span
                      className={`activity-icon ${m.quantity_change > 0 ? "in" : "out"}`}
                    >
                      {m.quantity_change > 0 ? (
                        <ArrowDownLeft size={18} />
                      ) : (
                        <ArrowUpRight size={18} />
                      )}
                    </span>
                    <div>
                      <strong>{m.product_name}</strong>
                      <p>
                        {m.reason} <span>· {m.sku}</span>
                      </p>
                    </div>
                    <div className="activity-amount">
                      <strong
                        className={
                          m.quantity_change > 0 ? "positive" : "negative"
                        }
                      >
                        {m.quantity_change > 0 ? "+" : ""}
                        {m.quantity_change} units
                      </strong>
                      <small>{stamp(m.created_at)}</small>
                    </div>
                  </div>
                ))}
                {!movements.length && (
                  <p className="empty-inline">
                    No stock movements yet. Add a product or adjust stock to
                    begin.
                  </p>
                )}
              </div>
            </section>
          )}
          <footer className="page-footer">
            <span>
              <Package size={13} />
              StockPilot · Inventory, under control.
            </span>
            <span>
              {new Date().toLocaleDateString("en-IN", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })}
            </span>
          </footer>
        </main>
      </div>
      {toast && (
        <div className="toast" role="status">
          <span>
            <Check size={17} />
          </span>
          {toast}
          <button
            className="icon-button"
            aria-label="Dismiss notification"
            onClick={() => setToast("")}
          >
            <X size={15} />
          </button>
        </div>
      )}
      {modal && (
        <Modal onClose={close} busy={busy} returnFocus={modalOpener.current}>
          <div className="modal-content">
            <div className="modal-heading">
              <div>
                <span className="eyebrow">STOCKPILOT OPERATIONS</span>
                <h2 id="modal-title">
                  {
                    {
                      create: "Add a product",
                      edit: "Edit product",
                      adjust: "Adjust inventory",
                      delete: "Delete product?",
                      view: "Product details",
                      help: "A clearer way to manage stock",
                    }[modal.type]
                  }
                </h2>
              </div>
              <button
                className="icon-button"
                onClick={close}
                disabled={busy}
                aria-label="Close dialog"
              >
                <X size={20} />
              </button>
            </div>
            {modal.type === "help" ? (
              <div className="help-content">
                <p>
                  Start with your products, then let the ledger tell the story.
                </p>
                <ol>
                  <li>
                    <strong>Add your catalog.</strong> Give each product a
                    unique SKU, price, opening balance, and reorder threshold.
                  </li>
                  <li>
                    <strong>Record the movement.</strong> Use the arrows beside
                    any product to receive or remove stock. Add a reason for a
                    useful audit trail. You cannot remove more units than are
                    currently available.
                  </li>
                  <li>
                    <strong>Stay ahead.</strong> Check the watchlist for
                    products at or below their threshold. Export a CSV whenever
                    you need a snapshot.
                  </li>
                </ol>
                <p>
                  All quantities and charts come from your database. Inventory
                  value uses selling prices in INR; it is not an accounting
                  valuation.
                </p>
                <a
                  className="button"
                  href="/docs"
                  target="_blank"
                  rel="noreferrer"
                >
                  Explore the API <ExternalLink size={15} />
                </a>
              </div>
            ) : modal.type === "view" ? (
              <div className="product-details">
                <span className={`badge ${stockStatus(modal.product)}`}>
                  <i />
                  {statusText[stockStatus(modal.product)]}
                </span>
                <h3>{modal.product.name}</h3>
                <p>{modal.product.description || "No description added."}</p>
                <dl>
                  {[
                    ["SKU", modal.product.sku],
                    ["Category", modal.product.category],
                    ["Selling price", money(modal.product.selling_price)],
                    ["On hand", `${modal.product.stock_quantity} units`],
                    ["Reorder at", `${modal.product.reorder_threshold} units`],
                    ["Created", stamp(modal.product.created_at)],
                    ["Last updated", stamp(modal.product.updated_at)],
                  ].map(([k, v]) => (
                    <div key={k}>
                      <dt>{k}</dt>
                      <dd>{v}</dd>
                    </div>
                  ))}
                </dl>
                <div className="modal-actions">
                  <button
                    className="button"
                    onClick={() => open("edit", modal.product)}
                  >
                    <Pencil size={16} />
                    Edit details
                  </button>
                  <button
                    className="button primary"
                    onClick={() => open("adjust", modal.product)}
                  >
                    <ArrowDownUp size={16} />
                    Adjust stock
                  </button>
                </div>
              </div>
            ) : (
              <form
                key={`${modal.type}-${modal.product?.id || "new"}`}
                onSubmit={save}
              >
                {modal.type === "delete" ? (
                  <div className="delete-content">
                    <div className="warning-icon">
                      <Trash2 size={24} />
                    </div>
                    <p>
                      <strong>{modal.product.name}</strong> ({modal.product.sku}
                      ) will be removed from your catalog. This cannot be
                      undone. Its stock history will be retained.
                    </p>
                  </div>
                ) : modal.type === "adjust" ? (
                  <>
                    <div className="adjust-summary">
                      <Package size={23} />
                      <div>
                        <strong>{modal.product.name}</strong>
                        <p>
                          {modal.product.sku} · {modal.product.stock_quantity}{" "}
                          units on hand
                        </p>
                      </div>
                    </div>
                    <div className="form-grid">
                      <label>
                        Movement
                        <select name="direction" aria-label="Movement" defaultValue="in">
                          <option value="in">Receive stock (+)</option>
                          <option value="out">Remove stock (−)</option>
                        </select>
                      </label>
                      <label>
                        Quantity
                        <input
                          name="quantity"
                          type="number"
                          min="1"
                          max="1000000"
                          step="1"
                          required
                          autoFocus
                          defaultValue="1"
                        />
                      </label>
                    </div>
                    <label>
                      Reason
                      <textarea
                        name="reason"
                        minLength="3"
                        maxLength="240"
                        required
                        placeholder="e.g. Supplier delivery, order fulfilled, damaged item"
                      />
                    </label>
                    <p className="form-hint">
                      The balance and ledger update together. Stock cannot go
                      below zero.
                    </p>
                  </>
                ) : (
                  <>
                    <div className="form-grid">
                      <label>
                        Product name
                        <input
                          name="name"
                          required
                          minLength="2"
                          maxLength="160"
                          autoFocus
                          defaultValue={modal.product?.name || blank.name}
                          placeholder="e.g. Arc desk lamp"
                        />
                      </label>
                      <label>
                        SKU
                        <input
                          name="sku"
                          required
                          minLength="2"
                          maxLength="40"
                          pattern="[A-Za-z0-9_\-]+"
                          defaultValue={modal.product?.sku || blank.sku}
                          placeholder="e.g. DSK-001"
                        />
                      </label>
                      <label>
                        Category
                        <input
                          name="category"
                          required
                          minLength="2"
                          maxLength="80"
                          list="categories"
                          defaultValue={
                            modal.product?.category || blank.category
                          }
                          placeholder="e.g. Workspace"
                        />
                        <datalist id="categories">
                          {categories.map((c) => (
                            <option key={c} value={c} />
                          ))}
                        </datalist>
                      </label>
                      <label>
                        Selling price (₹)
                        <input
                          name="selling_price"
                          required
                          type="number"
                          min="0"
                          max="9999999999"
                          step="0.01"
                          defaultValue={
                            modal.product?.selling_price || blank.selling_price
                          }
                          placeholder="0.00"
                        />
                      </label>
                      {modal.type === "create" && (
                        <label>
                          Opening stock
                          <input
                            name="stock_quantity"
                            required
                            type="number"
                            min="0"
                            max="1000000"
                            step="1"
                            defaultValue="0"
                          />
                        </label>
                      )}
                      <label>
                        Reorder threshold
                        <input
                          name="reorder_threshold"
                          required
                          type="number"
                          min="0"
                          max="1000000"
                          step="1"
                          defaultValue={modal.product?.reorder_threshold ?? 10}
                        />
                      </label>
                    </div>
                    <label>
                      Description <span className="optional">(optional)</span>
                      <textarea
                        name="description"
                        maxLength="4000"
                        defaultValue={modal.product?.description || ""}
                        placeholder="Add product details for your team…"
                      />
                    </label>
                    {modal.type === "edit" && (
                      <p className="form-hint">
                        Use Adjust stock to change quantities and retain the
                        audit trail.
                      </p>
                    )}
                  </>
                )}
                {formError && (
                  <div className="form-error" role="alert">
                    {formError}
                  </div>
                )}
                <div className="modal-actions">
                  <button
                    type="button"
                    className="button"
                    onClick={close}
                    disabled={busy}
                  >
                    Cancel
                  </button>
                  <button
                    className={`button ${modal.type === "delete" ? "danger" : "primary"}`}
                    disabled={busy}
                  >
                    {busy
                      ? "Saving…"
                      : modal.type === "delete"
                        ? "Delete product"
                        : modal.type === "adjust"
                          ? "Confirm adjustment"
                          : modal.type === "create"
                            ? "Add product"
                            : "Save changes"}
                  </button>
                </div>
              </form>
            )}
          </div>
        </Modal>
      )}
    </div>
  );
}
function Modal({ children, onClose, busy, returnFocus }) {
  const container = useRef(null);
  useEffect(() => {
    const previous = returnFocus;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const firstInput = container.current.querySelector("input, select, textarea");
    (firstInput || container.current.querySelector("button") || container.current).focus();
    return () => {
      document.body.style.overflow = previousOverflow;
      if (previous?.isConnected) previous.focus();
    };
  }, []);
  function keyDown(event) {
    if (event.key === "Escape") {
      event.preventDefault();
      if (!busy) onClose();
    }
    if (event.key !== "Tab") return;
    const controls = [...container.current.querySelectorAll(
      'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href], [tabindex="0"]'
    )].filter(el => el.getClientRects().length);
    const first = controls[0], last = controls.at(-1);
    if (!first) { event.preventDefault(); container.current.focus(); return; }
    if (event.shiftKey && (document.activeElement === first || !container.current.contains(document.activeElement))) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && (document.activeElement === last || !container.current.contains(document.activeElement))) {
      event.preventDefault(); first.focus();
    }
  }
  return <div className="modal-backdrop" onClick={event => {
    if (event.target === event.currentTarget && !busy) onClose();
  }}><div className="dialog" role="dialog" aria-modal="true" aria-labelledby="modal-title"
    tabIndex={-1} ref={container} onKeyDown={keyDown}>{children}</div></div>;
}

function Kpi({ label, value, icon: Icon, caption, color, loading, onClick }) {
  return (
    <div className={`kpi ${loading ? "loading" : ""}`}>
      <div className="kpi-top">
        <span>{label}</span>
        <span className={`kpi-icon ${color}`}>
          <Icon size={17} />
        </span>
      </div>
      <strong>{value}</strong>
      <div className="kpi-caption">
        {onClick ? (
          <button onClick={onClick}>
            {caption}
            <ArrowUpRight size={13} />
          </button>
        ) : (
          caption
        )}
      </div>
    </div>
  );
}
function MovementChart({ trend }) {
  const max = Math.max(1, ...trend.flatMap((d) => [d.inbound, d.outbound]));
  return (
    <div className="panel movement-chart">
      <div className="panel-heading">
        <div>
          <h2>Inventory flow</h2>
          <p>Stock received and dispatched</p>
        </div>
        <span className="period-tag">Last 7 days</span>
      </div>
      <div className="chart-legend">
        <span>
          <i className="inbound" />
          Stock in
        </span>
        <span>
          <i className="outbound" />
          Stock out
        </span>
      </div>
      <div
        className="bar-chart"
        role="img"
        aria-label="Stock received and removed each day over the last seven days"
      >
        <div className="y-labels">
          <span>{number(max)}</span>
          <span>{number(Math.round(max / 2))}</span>
          <span>0</span>
        </div>
        <div className="plot">
          <div className="grid-lines">
            <i />
            <i />
            <i />
          </div>
          {trend.map((d) => (
            <div className="bar-group" key={d.date}>
              <div className="bars">
                <span
                  className="bar inbound"
                  style={{ height: `${(d.inbound / max) * 100}%` }}
                  title={`${d.date}: ${d.inbound} received`}
                />
                <span
                  className="bar outbound"
                  style={{ height: `${(d.outbound / max) * 100}%` }}
                  title={`${d.date}: ${d.outbound} removed`}
                />
              </div>
              <small>
                {new Date(`${d.date}T12:00:00Z`).toLocaleDateString("en-IN", {
                  weekday: "short",
                })}
              </small>
            </div>
          ))}
        </div>
      </div>
      {!trend.some((d) => d.inbound || d.outbound) && (
        <p className="chart-empty">No stock movement in the last 7 days.</p>
      )}
    </div>
  );
}
function CategoryChart({ categories }) {
  const sum = categories.reduce((s, c) => s + c.units, 0),
    colors = ["#23695b", "#6b9b86", "#a6c6b5", "#d6e6db", "#b1b9a0"];
  let cursor = 0;
  const gradient = categories
    .map((c, i) => {
      const start = cursor;
      cursor += (c.units / Math.max(1, sum)) * 100;
      return `${colors[i % colors.length]} ${start}% ${cursor}%`;
    })
    .join(",");
  return (
    <div className="category-chart-content">
      <div
        className="donut"
        style={{ background: sum ? `conic-gradient(${gradient})` : "#edf1ed" }}
        role="img"
        aria-label={`${number(sum)} inventory units across ${categories.length} categories`}
      >
        <div>
          <strong>{number(sum)}</strong>
          <span>total units</span>
        </div>
      </div>
      <div className="category-legend">
        {categories.slice(0, 5).map((c, i) => (
          <div key={c.name}>
            <span>
              <i style={{ background: colors[i % colors.length] }} />
              {c.name}
            </span>
            <strong>
              {number(c.units)}{" "}
              <small>{Math.round((c.units / Math.max(1, sum)) * 100)}%</small>
            </strong>
          </div>
        ))}
        {!categories.length && <p>No categories yet.</p>}
        {categories.length > 5 && (
          <small>+ {categories.length - 5} more in inventory</small>
        )}
      </div>
    </div>
  );
}
createRoot(document.getElementById("root")).render(<App />);
