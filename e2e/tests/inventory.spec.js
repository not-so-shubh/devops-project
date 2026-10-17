import { test, expect } from "@playwright/test";

async function navigate(page, title) {
  const menu = page.getByRole("button", {
    name: "Open navigation",
    exact: true,
  });
  if (await menu.isVisible()) await menu.click();
  await page
    .getByRole("navigation")
    .getByRole("button", { name: title, exact: true })
    .click();
}

test("live inventory CRUD, atomic stock adjustment and retained ledger", async ({
  page,
}, testInfo) => {
  const sku = `E2E-${Date.now()}`;
  await page.goto("/");
  await expect(page.getByText("Connected to database")).toBeAttached();
  await expect(
    page.getByRole("heading", { name: "Inventory overview" }),
  ).toBeVisible();
  await page.screenshot({
    path: `../docs/evidence/frontend-${testInfo.project.name}.png`,
    fullPage: true,
  });
  await page
    .getByRole("button", { name: "Add product", exact: true })
    .first()
    .click();
  const modal = page.getByRole("dialog");
  await modal.getByLabel("Product name").fill("Browser verified lamp");
  await modal.getByLabel("SKU", { exact: true }).fill(sku);
  await modal.getByLabel("Category", { exact: true }).fill("Validation");
  await modal.getByLabel("Selling price").fill("125.50");
  await modal.getByLabel("Opening stock").fill("6");
  await modal.getByLabel("Reorder threshold").fill("3");
  await page.screenshot({path:`../docs/evidence/create-dialog-${testInfo.project.name}.png`,fullPage:false});
  await modal.getByRole("button", { name: "Add product", exact: true }).click();
  await expect(modal).not.toBeVisible();
  await page.getByLabel("Search inventory").fill(sku);
  let row = page.getByRole("row").filter({ hasText: sku });
  await expect(row).toContainText("6");
  await row
    .getByRole("button", { name: "Edit Browser verified lamp", exact: true })
    .click();
  await modal.getByLabel("Product name").fill("Browser verified lamp updated");
  await modal.getByRole("button", { name: "Save changes" }).click();
  await expect(modal).not.toBeVisible();
  await expect(row).toContainText("updated");
  await row
    .getByRole("button", { name: "Adjust Browser verified lamp updated" })
    .click();
  await modal.getByLabel("Movement", { exact: true }).selectOption("out");
  await modal.getByLabel("Quantity", { exact: true }).fill("99");
  await modal.getByLabel("Reason").fill("Browser insufficient stock check");
  await modal.getByRole("button", { name: "Confirm adjustment" }).click();
  await expect(modal.getByRole("alert")).toContainText("Insufficient stock");
  await modal.getByLabel("Quantity", { exact: true }).fill("4");
  await modal.getByLabel("Reason").fill("Browser verified shipment");
  await modal.getByRole("button", { name: "Confirm adjustment" }).click();
  await expect(modal).not.toBeVisible();
  await expect(row).toContainText("Low stock");
  await row
    .getByRole("button", { name: "Browser verified lamp updated", exact: true })
    .click();
  await expect(modal).toContainText("2 units");
  await modal.getByRole("button", { name: "Close dialog" }).click();
  await row
    .getByRole("button", { name: "Delete Browser verified lamp updated" })
    .click();
  await modal
    .getByRole("button", { name: "Delete product", exact: true })
    .click();
  await expect(modal).not.toBeVisible();
  await expect(page.getByText("No matching products")).toBeVisible();
  await navigate(page, "Stock movements");
  const movement = page
    .getByRole("row")
    .filter({ hasText: "Browser verified shipment" })
    .filter({ hasText: sku });
  await expect(movement).toContainText("Deleted product");
  await expect(movement).toContainText("-4");
  // Independent API retrieval proves the UI's movement came from persistent data.
  const response = await page.request.get("/api/inventory/movements");
  expect(
    (await response.json()).some(
      (m) => m.sku === sku && m.product_id === null && m.quantity_after === 2,
    ),
  ).toBe(true);
});

test("filters, export, guide and responsive navigation work", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByText("Connected to database")).toBeAttached();
  await navigate(page, "All inventory");
  await page.getByLabel("Search inventory").fill("NO-MATCH-UNIQUE-928391");
  await expect(page.getByText("No matching products")).toBeVisible();
  await page.getByLabel("Search inventory").fill("");
  await page.getByRole("button", { name: "Out of stock", exact: true }).click();
  const rows = page.locator("tbody tr");
  for (const row of await rows.all())
    await expect(row).toContainText("Out of stock");
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export", exact: true }).click();
  expect((await downloadPromise).suggestedFilename()).toMatch(
    /stockpilot-inventory-.*\.csv/,
  );
  if (
    await page
      .getByRole("button", { name: "Open quick guide", exact: true })
      .isVisible()
  ) {
    await page
      .getByRole("button", { name: "Open quick guide", exact: true })
      .click();
    await expect(page.getByRole("dialog")).toContainText("Record the movement");
    await page.keyboard.press("Escape");
    await expect(page.getByRole("dialog")).not.toBeVisible();
  }
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});
