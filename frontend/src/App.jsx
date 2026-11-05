import { useCallback, useEffect, useState } from "react";

import Dashboard from "./Dashboard";
import ProjectMembersPanel from "./ProjectMembersPanel";
import TasksPanel from "./TasksPanel";
import UsersPanel from "./UsersPanel";
import {
  apiRequest,
  ensureCsrfCookie,
  getCsrfCookie,
  getRequestError,
  getResponseError,
  sessionExpiredEvent,
} from "./api";

async function requestProjects(name = "") {
  const search = name.trim()
    ? `?name=${encodeURIComponent(name.trim())}`
    : "";
  const response = await apiRequest(`/projects/${search}`);
  if (response.status === 401) {
    return null;
  }
  if (!response.ok) {
    throw new Error(
      await getResponseError(response, "Não foi possível carregar os projetos."),
    );
  }
  return response.json();
}

function LoginForm({ onLogin, message, pending }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    const authenticated = await onLogin(email, password);
    if (authenticated) {
      setPassword("");
    }
  }

  return (
    <section className="auth-card" aria-labelledby="page-title">
      <p className="eyebrow">Gestão de projetos e tarefas</p>
      <h1 id="page-title">Matriz</h1>
      <p className="intro">Inicia sessão para aceder aos teus projetos.</p>
      <form className="login-form" onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          autoComplete="username"
          id="email"
          name="email"
          onChange={(event) => setEmail(event.target.value)}
          required
          type="email"
          value={email}
        />
        <label htmlFor="password">Palavra-passe</label>
        <input
          autoComplete="current-password"
          id="password"
          name="password"
          onChange={(event) => setPassword(event.target.value)}
          required
          type="password"
          value={password}
        />
        {message && (
          <p className="form-message" role="alert">
            {message}
          </p>
        )}
        <button disabled={pending} type="submit">
          {pending ? "A iniciar sessão..." : "Iniciar sessão"}
        </button>
      </form>
    </section>
  );
}

function ProjectForm({ project, onCancel, onSave, pending, message }) {
  const [title, setTitle] = useState(project?.title || "");
  const [description, setDescription] = useState(project?.description || "");

  function handleSubmit(event) {
    event.preventDefault();
    onSave({ title, description });
  }

  return (
    <section className="workspace-card" aria-labelledby="project-form-title">
      <button className="back-button" onClick={onCancel} type="button">
        Voltar
      </button>
      <h2 id="project-form-title">
        {project ? "Editar projeto" : "Criar projeto"}
      </h2>
      <form className="project-form" onSubmit={handleSubmit}>
        <label htmlFor="project-title">Nome</label>
        <input
          autoComplete="off"
          id="project-title"
          maxLength={100}
          minLength={3}
          onChange={(event) => setTitle(event.target.value)}
          required
          value={title}
        />
        <label htmlFor="project-description">Descrição (opcional)</label>
        <textarea
          id="project-description"
          maxLength={1000}
          onChange={(event) => setDescription(event.target.value)}
          rows={5}
          value={description}
        />
        {message && (
          <p className="form-message" role="alert">
            {message}
          </p>
        )}
        <div className="action-row">
          <button disabled={pending} type="submit">
            {pending ? "A guardar..." : "Guardar projeto"}
          </button>
          <button
            className="secondary-button"
            disabled={pending}
            onClick={onCancel}
            type="button"
          >
            Cancelar
          </button>
        </div>
      </form>
    </section>
  );
}

function ProjectsList({
  projects,
  searchTerm,
  onSearchChange,
  onSearch,
  onCreate,
  onOpen,
  canCreate,
  message,
  loading,
  loadError,
  onRetry,
  pending,
}) {
  return (
    <section className="workspace-card" aria-labelledby="projects-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Matriz</p>
          <h1 id="projects-title">Projetos</h1>
        </div>
        {canCreate && (
          <button
            disabled={pending || loading || Boolean(loadError)}
            onClick={onCreate}
            type="button"
          >
            Novo projeto
          </button>
        )}
      </div>
      <form className="project-search" onSubmit={onSearch} role="search">
        <label className="visually-hidden" htmlFor="project-search">
          Pesquisar projetos por nome
        </label>
        <input
          id="project-search"
          disabled={loading}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Pesquisar por nome"
          type="search"
          value={searchTerm}
        />
        <button disabled={pending || loading} type="submit">
          Pesquisar
        </button>
      </form>
      {loading ? (
        <p aria-live="polite" className="loading-state">
          A carregar projetos...
        </p>
      ) : loadError ? (
        <div>
          <p className="form-message" role="alert">
            {loadError}
          </p>
          <button
            disabled={pending}
            onClick={onRetry}
            type="button"
          >
            Tentar novamente
          </button>
        </div>
      ) : message ? (
        <p className="form-message" role="alert">
          {message}
        </p>
      ) : projects.length === 0 ? (
        <p className="empty-state">
          {searchTerm.trim()
            ? "Não existem projetos correspondentes a esta pesquisa."
            : "Não há projetos acessíveis para apresentar."}
        </p>
      ) : (
        <ul className="project-list">
          {projects.map((project) => (
            <li key={project.projectId}>
              <button
                className="project-card"
                disabled={pending || loading}
                onClick={() => onOpen(project.projectId)}
                type="button"
              >
                <span className="project-card-title">{project.title}</span>
                <span className="project-card-description">
                  {project.description || "Sem descrição"}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function ProjectDetails({
  project,
  user,
  canManage,
  onBack,
  onEdit,
  onDelete,
  pending,
}) {
  return (
    <section className="workspace-card" aria-labelledby="project-detail-title">
      <button className="back-button" onClick={onBack} type="button">
        Voltar aos projetos
      </button>
      <p className="eyebrow">Detalhe do projeto</p>
      <h1 id="project-detail-title">{project.title}</h1>
      <p className="project-description">
        {project.description || "Sem descrição."}
      </p>
      {canManage && (
        <div className="action-row">
          <button disabled={pending} onClick={onEdit} type="button">
            Editar
          </button>
          <button
            className="danger-button"
            disabled={pending}
            onClick={onDelete}
            type="button"
          >
            Eliminar
          </button>
        </div>
      )}
      <ProjectMembersPanel
        canManage={canManage}
        project={project}
      />
      <TasksPanel
        canManage={canManage}
        key={project.projectId}
        project={project}
        user={user}
      />
    </section>
  );
}

export default function App() {
  const [authStatus, setAuthStatus] = useState("checking");
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);
  const [projects, setProjects] = useState([]);
  const [projectsLoading, setProjectsLoading] = useState(false);
  const [projectsLoadError, setProjectsLoadError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [projectView, setProjectView] = useState("dashboard");
  const [selectedProject, setSelectedProject] = useState(null);
  const [failedProjectId, setFailedProjectId] = useState(null);
  const [projectMessage, setProjectMessage] = useState("");

  const handleSessionExpired = useCallback(() => {
    setUser(null);
    setProjects([]);
    setProjectsLoading(false);
    setProjectsLoadError("");
    setSelectedProject(null);
    setProjectView("dashboard");
    setAuthStatus("anonymous");
    setMessage("A sessão terminou ou não é válida. Inicia sessão novamente.");
  }, []);

  useEffect(() => {
    window.addEventListener(sessionExpiredEvent, handleSessionExpired);
    const controller = new AbortController();

    async function checkSession() {
      let sessionFound = false;
      try {
        const response = await apiRequest("/users/me/", {
          signal: controller.signal,
        });
        if (!response.ok) {
          if (response.status === 401) {
            setAuthStatus("anonymous");
            return;
          }
          throw new Error("Não foi possível verificar a sessão.");
        }
        const currentUser = await response.json();
        sessionFound = true;
        setUser(currentUser);
        setAuthStatus("authenticated");
        setMessage("");
        setProjectsLoading(true);
        setProjectsLoadError("");
        const accessibleProjects = await requestProjects();
        if (accessibleProjects) {
          setProjects(accessibleProjects);
        }
      } catch (error) {
        if (error.name !== "AbortError") {
          if (sessionFound) {
            const loadError =
              getRequestError(error, "Não foi possível carregar os projetos.");
            setProjectMessage(loadError);
            setProjectsLoadError(loadError);
          } else {
            setAuthStatus("anonymous");
            setMessage(getRequestError(error, "Não foi possível ligar à aplicação."));
          }
        }
      } finally {
        if (sessionFound) {
          setProjectsLoading(false);
        }
      }
    }

    checkSession();
    return () => {
      controller.abort();
      window.removeEventListener(sessionExpiredEvent, handleSessionExpired);
    };
  }, [handleSessionExpired]);

  async function handleLogin(email, password) {
    setPending(true);
    setMessage("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest("/sessions/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfCookie(),
        },
        body: JSON.stringify({ email, password }),
      });
      const result = await response.json();
      if (!response.ok) {
        setMessage(result.message || "Não foi possível iniciar sessão.");
        return false;
      }
      setUser(result.user);
      setAuthStatus("authenticated");
      setMessage("");
      setProjects([]);
      setProjectsLoading(true);
      setProjectsLoadError("");
      setProjectView("dashboard");
      setProjectMessage("");
      try {
        const accessibleProjects = await requestProjects();
        if (accessibleProjects) {
          setProjects(accessibleProjects);
        }
      } catch (error) {
        const loadError =
          getRequestError(error, "Não foi possível carregar os projetos.");
        setProjectMessage(loadError);
        setProjectsLoadError(loadError);
      } finally {
        setProjectsLoading(false);
      }
      return true;
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível ligar à aplicação."));
      return false;
    } finally {
      setPending(false);
    }
  }

  async function handleLogout() {
    setPending(true);
    setMessage("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest("/sessions/current/", {
        method: "DELETE",
        headers: { "X-CSRFToken": getCsrfCookie() },
      });
      if (response.status === 401) {
        setUser(null);
        setAuthStatus("anonymous");
        setMessage("A sessão terminou ou não é válida. Inicia sessão novamente.");
        return;
      }
      if (!response.ok) {
        throw new Error("Não foi possível terminar sessão.");
      }
      setUser(null);
      setProjects([]);
      setProjectsLoading(false);
      setProjectsLoadError("");
      setSelectedProject(null);
      setProjectView("list");
      setAuthStatus("anonymous");
      setMessage("Terminaste a sessão.");
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível terminar sessão."));
    } finally {
      setPending(false);
    }
  }

  async function refreshProjects(name = searchTerm) {
    setProjectMessage("");
    setProjectsLoadError("");
    setProjectsLoading(true);
    try {
      const accessibleProjects = await requestProjects(name);
      if (accessibleProjects) {
        setProjects(accessibleProjects);
      }
    } catch (error) {
      const loadError =
        getRequestError(error, "Não foi possível carregar os projetos.");
      setProjectMessage(loadError);
      setProjectsLoadError(loadError);
    } finally {
      setProjectsLoading(false);
    }
  }

  function showDashboard() {
    setProjectMessage("");
    setProjectView("dashboard");
  }

  function showProjects() {
    setProjectMessage("");
    setSearchTerm("");
    setProjectView("list");
    refreshProjects("");
  }

  function showUsers() {
    setProjectMessage("");
    setProjectView("users");
  }

  async function handleCurrentUserUpdated(updatedUser) {
    setUser(updatedUser);
    if (updatedUser.role !== "ADMIN") {
      setProjectView("dashboard");
      await refreshProjects("");
    }
  }

  async function openProject(projectId) {
    setPending(true);
    setProjectMessage("");
    setFailedProjectId(projectId);
    setSelectedProject(null);
    setProjectView("loading-project");
    try {
      const response = await apiRequest(`/projects/${projectId}/`);
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível abrir o projeto."),
        );
      }
      setSelectedProject(await response.json());
      setProjectView("detail");
    } catch (error) {
      setProjectMessage(getRequestError(error, "Não foi possível abrir o projeto."));
      setProjectView("project-error");
    } finally {
      setPending(false);
    }
  }

  async function saveProject(values) {
    setPending(true);
    setProjectMessage("");
    const isEditing = projectView === "edit";
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        isEditing ? `/projects/${selectedProject.projectId}/` : "/projects/",
        {
          method: isEditing ? "PATCH" : "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfCookie(),
          },
          body: JSON.stringify(values),
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível guardar o projeto."),
        );
      }
      const savedProject = await response.json();
      setSelectedProject(savedProject);
      setProjectView("detail");
      if (!isEditing) {
        setSearchTerm("");
      }
      await refreshProjects(isEditing ? searchTerm : "");
    } catch (error) {
      setProjectMessage(getRequestError(error, "Não foi possível guardar o projeto."));
    } finally {
      setPending(false);
    }
  }

  async function deleteProject() {
    if (
      !window.confirm(
        `Eliminar "${selectedProject.title}"? As tarefas, responsáveis e comentários dependentes também serão eliminados.`,
      )
    ) {
      return;
    }

    setPending(true);
    setProjectMessage("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${selectedProject.projectId}/`,
        {
          method: "DELETE",
          headers: { "X-CSRFToken": getCsrfCookie() },
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível eliminar o projeto."),
        );
      }
      setSelectedProject(null);
      setProjectView("dashboard");
      setProjectMessage("Projeto eliminado.");
      await refreshProjects();
    } catch (error) {
      setProjectMessage(getRequestError(error, "Não foi possível eliminar o projeto."));
    } finally {
      setPending(false);
    }
  }

  function cancelProjectForm() {
    setProjectMessage("");
    setProjectView(selectedProject ? "detail" : "list");
  }

  function startCreate() {
    setSelectedProject(null);
    setProjectMessage("");
    setProjectView("create");
  }

  const canManageSelectedProject =
    user?.role === "PROJECT_MANAGER" &&
    selectedProject?.managerId === user.userId;

  return (
    <main className="page">
      {authStatus === "checking" ? (
        <section className="auth-card" aria-live="polite">
          <p className="eyebrow">Matriz</p>
          <p className="intro">A verificar a sessão...</p>
        </section>
      ) : authStatus === "authenticated" ? (
        <div className="workspace">
          <header className="workspace-bar">
            <p>
              Sessão: {user.email} <span>({user.role})</span>
            </p>
            <button
              className="secondary-button"
              disabled={pending}
              onClick={handleLogout}
              type="button"
            >
              Terminar sessão
            </button>
          </header>
          {projectView !== "create" && projectView !== "edit" && (
            <nav aria-label="Navegação principal" className="workspace-nav">
              <button
                aria-current={projectView === "dashboard" ? "page" : undefined}
                className={
                  projectView === "dashboard" ? "" : "secondary-button"
                }
                disabled={pending}
                onClick={showDashboard}
                type="button"
              >
                Painel
              </button>
              <button
                aria-current={
                  projectView === "dashboard" || projectView === "users"
                    ? undefined
                    : "page"
                }
                className={
                  projectView === "dashboard" || projectView === "users"
                    ? "secondary-button"
                    : ""
                }
                disabled={pending}
                onClick={showProjects}
                type="button"
              >
                Projetos
              </button>
              {user.role === "ADMIN" && (
                <button
                  aria-current={projectView === "users" ? "page" : undefined}
                  className={
                    projectView === "users" ? "" : "secondary-button"
                  }
                  disabled={pending}
                  onClick={showUsers}
                  type="button"
                >
                  Utilizadores
                </button>
              )}
            </nav>
          )}
          {projectView === "users" ? (
            <UsersPanel
              currentUser={user}
              onCurrentUserUpdated={handleCurrentUserUpdated}
            />
          ) : projectView === "dashboard" ? (
            <Dashboard
              onOpenProject={openProject}
              onViewProjects={showProjects}
              user={user}
            />
          ) : projectView === "loading-project" ? (
            <section aria-live="polite" className="workspace-card">
              <p className="loading-state">A carregar o projeto...</p>
            </section>
          ) : projectView === "project-error" ? (
            <section className="workspace-card">
              <p className="form-message" role="alert">
                {projectMessage}
              </p>
              <div className="action-row">
                <button
                  disabled={pending}
                  onClick={() => openProject(failedProjectId)}
                  type="button"
                >
                  Tentar novamente
                </button>
                <button
                  className="secondary-button"
                  disabled={pending}
                  onClick={showProjects}
                  type="button"
                >
                  Voltar aos projetos
                </button>
              </div>
            </section>
          ) : projectView === "create" || projectView === "edit" ? (
            <ProjectForm
              message={projectMessage}
              onCancel={cancelProjectForm}
              onSave={saveProject}
              pending={pending}
              project={projectView === "edit" ? selectedProject : null}
            />
          ) : projectView === "detail" && selectedProject ? (
            <ProjectDetails
              canManage={canManageSelectedProject}
              onBack={() => setProjectView("list")}
              onDelete={deleteProject}
              onEdit={() => {
                setProjectMessage("");
                setProjectView("edit");
              }}
              pending={pending}
              project={selectedProject}
              user={user}
            />
          ) : (
            <ProjectsList
              canCreate={user.role === "PROJECT_MANAGER"}
              loading={projectsLoading}
              loadError={projectsLoadError}
              message={projectMessage}
              onCreate={startCreate}
              onOpen={openProject}
              onRetry={() => refreshProjects()}
              onSearch={(event) => {
                event.preventDefault();
                refreshProjects();
              }}
              onSearchChange={setSearchTerm}
              pending={pending}
              projects={projects}
              searchTerm={searchTerm}
            />
          )}
        </div>
      ) : (
        <LoginForm
          message={message}
          onLogin={handleLogin}
          pending={pending}
        />
      )}
    </main>
  );
}
