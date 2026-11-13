import assert from "node:assert/strict";
import { test } from "node:test";

import { shouldDispatchSessionExpiredEvent } from "../src/sessionExpired.js";

test("does not treat an unauthenticated session check as an expired session", () => {
  assert.equal(shouldDispatchSessionExpiredEvent("/users/me/", 401), false);
});

test("dispatches session expiry for unauthorized protected requests", () => {
  assert.equal(shouldDispatchSessionExpiredEvent("/projects/", 401), true);
});

test("does not dispatch session expiry for rejected login attempts", () => {
  assert.equal(shouldDispatchSessionExpiredEvent("/sessions/", 401), true);
});
