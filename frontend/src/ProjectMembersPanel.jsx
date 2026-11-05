import { useEffect, useState } from "react";

import {
  apiRequest,
  ensureCsrfCookie,
  getCsrfCookie,
  getRequestError,
  getResponseError,
} from "./api";

const roleLabels = {
  ADMIN: "Admin",
  PROJECT_MANAGER: "Project Manager",
  DEVELOPER: "Developer",
};

export default function ProjectMembersPanel({ project, canManage }) {
  const [members, setMembers] = useState([]);
  const [eligibleUsers, setEligibleUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState("");
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [reloadCount, setReloadCount] = useState(0);

  useEffect(() => {
    let active = true;

    async function loadMembers() {
      setLoading(true);
      setError("");
      try {
        const membersResponse = await apiRequest(
          `/projects/${project.projectId}/members/`,
        );
        if (!membersResponse.ok) {
          throw new Error(
            await getResponseError(
              membersResponse,
              "Não foi possível carregar os membros do projeto.",
            ),
          );
        }
        const loadedMembers = await membersResponse.json();
        let loadedEligibleUsers = [];
        if (canManage) {
          const eligibleResponse = await apiRequest(
            `/projects/${project.projectId}/eligible-members/`,
          );
          if (!eligibleResponse.ok) {
            throw new Error(
              await getResponseError(
                eligibleResponse,
                "Não foi possível carregar os utilizadores elegíveis.",
              ),
            );
          }
          loadedEligibleUsers = await eligibleResponse.json();
        }
        if (active) {
          setMembers(loadedMembers);
          setEligibleUsers(loadedEligibleUsers);
        }
      } catch (requestError) {
        if (active) {
          setError(
            getRequestError(
              requestError,
              "Não foi possível carregar os membros do projeto.",
            ),
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadMembers();
    return () => {
      active = false;
    };
  }, [canManage, project.projectId, reloadCount]);

  async function addMember(event) {
    event.preventDefault();
    if (!selectedUserId) {
      return;
    }

    setPending(true);
    setError("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/members/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfCookie(),
          },
          body: JSON.stringify({ userId: Number(selectedUserId) }),
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível adicionar o membro."),
        );
      }
      const addedMember = await response.json();
      setMembers((currentMembers) => [...currentMembers, addedMember]);
      setEligibleUsers((currentUsers) =>
        currentUsers.filter((user) => user.userId !== addedMember.userId),
      );
      setSelectedUserId("");
      setNotice(`${addedMember.email} foi associado ao projeto.`);
    } catch (requestError) {
      setError(
        getRequestError(requestError, "Não foi possível adicionar o membro."),
      );
    } finally {
      setPending(false);
    }
  }

  async function removeMember(member) {
    if (
      !window.confirm(
        `Remover ${member.email} do projeto? As atribuições desta pessoa às tarefas do projeto também serão removidas.`,
      )
    ) {
      return;
    }

    setPending(true);
    setError("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/members/${member.userId}/`,
        {
          method: "DELETE",
          headers: { "X-CSRFToken": getCsrfCookie() },
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível remover o membro."),
        );
      }
      setMembers((currentMembers) =>
        currentMembers.filter((currentMember) => currentMember.userId !== member.userId),
      );
      setEligibleUsers((currentUsers) => [...currentUsers, member]);
      setNotice(`${member.email} foi removido do projeto.`);
    } catch (requestError) {
      setError(
        getRequestError(requestError, "Não foi possível remover o membro."),
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="project-members" aria-labelledby="project-members-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Acesso ao trabalho</p>
          <h2 id="project-members-title">Membros do projeto</h2>
        </div>
        {!loading && (
          <button
            className="secondary-button"
            disabled={pending}
            onClick={() => setReloadCount((count) => count + 1)}
            type="button"
          >
            Atualizar
          </button>
        )}
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
          A carregar membros...
        </p>
      ) : members.length === 0 ? (
        <p className="empty-state">O projeto ainda não tem membros.</p>
      ) : (
        <ul className="project-member-list">
          {members.map((member) => (
            <li key={member.userId}>
              <div>
                <strong>{member.email}</strong>
                <span>
                  {member.userId === project.managerId
                    ? `${roleLabels[member.role]} · Gestor`
                    : roleLabels[member.role]}
                </span>
              </div>
              {canManage && member.userId !== project.managerId && (
                <button
                  className="secondary-button"
                  disabled={pending}
                  onClick={() => removeMember(member)}
                  type="button"
                >
                  Remover
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
      {canManage && !loading && (
        <form className="project-member-form" onSubmit={addMember}>
          <label htmlFor="project-member-select">Adicionar utilizador ativo</label>
          <select
            disabled={pending || eligibleUsers.length === 0}
            id="project-member-select"
            onChange={(event) => setSelectedUserId(event.target.value)}
            value={selectedUserId}
          >
            <option value="">
              {eligibleUsers.length
                ? "Selecionar utilizador"
                : "Não há mais utilizadores elegíveis"}
            </option>
            {eligibleUsers.map((user) => (
              <option key={user.userId} value={user.userId}>
                {user.email} · {roleLabels[user.role]}
              </option>
            ))}
          </select>
          <button disabled={pending || !selectedUserId} type="submit">
            {pending ? "A guardar..." : "Adicionar membro"}
          </button>
        </form>
      )}
    </section>
  );
}
