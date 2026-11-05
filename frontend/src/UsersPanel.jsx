import { useEffect, useState } from "react";

import {
  apiRequest,
  ensureCsrfCookie,
  getCsrfCookie,
  getRequestError,
  getResponseError,
} from "./api";

const userRoles = [
  ["ADMIN", "Admin"],
  ["PROJECT_MANAGER", "Project Manager"],
  ["DEVELOPER", "Developer"],
];
const roleLabels = Object.fromEntries(userRoles);

export default function UsersPanel({ currentUser, onCurrentUserUpdated }) {
  const [users, setUsers] = useState([]);
  const [selectedRoles, setSelectedRoles] = useState({});
  const [loading, setLoading] = useState(true);
  const [pendingUserId, setPendingUserId] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [reloadCount, setReloadCount] = useState(0);

  useEffect(() => {
    let active = true;

    async function loadUsers() {
      setLoading(true);
      setError("");
      try {
        const response = await apiRequest("/users/");
        if (!response.ok) {
          throw new Error(
            await getResponseError(response, "Não foi possível carregar os utilizadores."),
          );
        }
        const loadedUsers = await response.json();
        if (active) {
          setUsers(loadedUsers);
          setSelectedRoles({});
        }
      } catch (requestError) {
        if (active) {
          setError(
            getRequestError(
              requestError,
              "Não foi possível carregar os utilizadores.",
            ),
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadUsers();
    return () => {
      active = false;
    };
  }, [reloadCount]);

  async function saveRole(event, user) {
    event.preventDefault();
    const role = selectedRoles[user.userId] || user.role;
    if (role === user.role) {
      return;
    }

    setPendingUserId(user.userId);
    setError("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(`/users/${user.userId}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfCookie(),
        },
        body: JSON.stringify({ role }),
      });
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível atualizar o papel."),
        );
      }
      const updatedUser = await response.json();
      setUsers((currentUsers) =>
        currentUsers.map((currentUser) =>
          currentUser.userId === updatedUser.userId
            ? updatedUser
            : currentUser,
        ),
      );
      setSelectedRoles((currentRoles) => {
        const { [user.userId]: _savedRole, ...remainingRoles } = currentRoles;
        return remainingRoles;
      });
      setNotice(`Papel de ${updatedUser.email} atualizado.`);
      if (updatedUser.userId === currentUser.userId) {
        onCurrentUserUpdated(updatedUser);
      }
    } catch (requestError) {
      setError(
        getRequestError(requestError, "Não foi possível atualizar o papel."),
      );
    } finally {
      setPendingUserId(null);
    }
  }

  return (
    <section className="workspace-card" aria-labelledby="users-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Administração</p>
          <h1 id="users-title">Utilizadores e papéis</h1>
        </div>
        <button
          disabled={loading || pendingUserId !== null}
          onClick={() => setReloadCount((count) => count + 1)}
          type="button"
        >
          Atualizar
        </button>
      </div>
      {error && (
        <p className="form-message" role="alert">
          {error}
        </p>
      )}
      {notice && (
        <p className="success-message" role="status">
          {notice}
        </p>
      )}
      {loading ? (
        <p aria-live="polite" className="loading-state">
          A carregar utilizadores...
        </p>
      ) : users.length === 0 ? (
        <p className="empty-state">Não existem utilizadores para apresentar.</p>
      ) : (
        <ul className="user-role-list">
          {users.map((user) => {
            const selectedRole = selectedRoles[user.userId] || user.role;
            return (
              <li key={user.userId}>
                <div className="user-role-identity">
                  <strong>{user.email}</strong>
                  <span>{user.isActive ? "Ativo" : "Inativo"}</span>
                </div>
                <form
                  className="user-role-form"
                  onSubmit={(event) => saveRole(event, user)}
                >
                  <label htmlFor={`user-role-${user.userId}`}>Papel</label>
                  <select
                    disabled={pendingUserId !== null}
                    id={`user-role-${user.userId}`}
                    onChange={(event) =>
                      setSelectedRoles((currentRoles) => ({
                        ...currentRoles,
                        [user.userId]: event.target.value,
                      }))
                    }
                    value={selectedRole}
                  >
                    {userRoles.map(([value, label]) => (
                      <option key={value} value={value}>
                        {label}
                      </option>
                    ))}
                  </select>
                  <span className="user-role-current">
                    Atual: {roleLabels[user.role]}
                  </span>
                  <button
                    disabled={pendingUserId !== null || selectedRole === user.role}
                    type="submit"
                  >
                    {pendingUserId === user.userId ? "A guardar..." : "Guardar"}
                  </button>
                </form>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
