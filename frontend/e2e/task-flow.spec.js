import { randomUUID } from "node:crypto";

import { expect, test } from "@playwright/test";

import { e2eApiBaseURL, e2eCredentials } from "../playwright.config.js";

let createdProjectId;

test.afterEach(async ({ page }) => {
  if (!createdProjectId) {
    return;
  }

  const csrfResponse = await page.context().request.get(
    `${e2eApiBaseURL}/csrf/`,
  );
  expect(csrfResponse.status()).toBe(204);
  const csrfCookie = (await page.context().cookies(e2eApiBaseURL)).find(
    (cookie) => cookie.name === "csrftoken",
  );
  expect(csrfCookie).toBeDefined();
  const deleteResponse = await page.context().request.delete(
    `${e2eApiBaseURL}/projects/${createdProjectId}/`,
    { headers: { "X-CSRFToken": csrfCookie.value } },
  );
  expect(deleteResponse.status()).toBe(204);
  createdProjectId = undefined;
});

test("Project Manager signs in and creates a TODO task in a new project", async ({
  page,
}) => {
  const projectTitle = `E2E project ${randomUUID()}`;
  const taskTitle = `E2E task ${randomUUID()}`;

  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Matriz" })).toBeVisible();
  await page.getByLabel("Email").fill(e2eCredentials.email);
  await page.getByLabel("Palavra-passe").fill(e2eCredentials.password);
  await page.getByRole("button", { name: "Iniciar sessão" }).click();

  await expect(
    page.getByRole("heading", { name: "Painel inicial" }),
  ).toBeVisible();
  await expect(page.getByText(e2eCredentials.email)).toBeVisible();

  const navigation = page.getByRole("navigation", {
    name: "Navegação principal",
  });
  await navigation.getByRole("button", { name: "Projetos" }).click();
  await expect(page.getByRole("heading", { name: "Projetos" })).toBeVisible();
  await page.getByRole("button", { name: "Novo projeto" }).click();
  await expect(
    page.getByRole("heading", { name: "Criar projeto" }),
  ).toBeVisible();
  await page.getByLabel("Nome").fill(projectTitle);

  const projectCreated = page.waitForResponse(
    (response) =>
      response.url() === `${e2eApiBaseURL}/projects/` &&
      response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Guardar projeto" }).click();
  const projectResponse = await projectCreated;
  const project = await projectResponse.json();
  createdProjectId = project.projectId;
  expect(projectResponse.status()).toBe(201);

  await expect(
    page.getByRole("heading", { name: projectTitle }),
  ).toBeVisible();
  await expect(page.getByRole("heading", { name: "Tarefas" })).toBeVisible();
  await page.getByRole("button", { name: "Nova tarefa" }).click();

  const taskForm = page.getByRole("region", { name: "Nova tarefa" });
  await expect(taskForm).toBeVisible();
  await taskForm.getByLabel("Título").fill(taskTitle);
  await taskForm.getByLabel("Estado").selectOption("TODO");

  const taskCreated = page.waitForResponse(
    (response) =>
      response.url() ===
        `${e2eApiBaseURL}/projects/${createdProjectId}/tasks/` &&
      response.request().method() === "POST",
  );
  await taskForm.getByRole("button", { name: "Guardar tarefa" }).click();
  const taskResponse = await taskCreated;
  expect(taskResponse.status()).toBe(201);
  const task = await taskResponse.json();
  expect(task.title).toBe(taskTitle);
  expect(task.status).toBe("TODO");

  await expect(page.getByRole("heading", { name: taskTitle })).toBeVisible();
  await page.getByRole("button", { name: "Voltar às tarefas" }).click();

  const taskRow = page.getByRole("listitem").filter({ hasText: taskTitle });
  await expect(taskRow).toBeVisible();
  await expect(taskRow.getByLabel("Estado")).toHaveValue("TODO");
});
