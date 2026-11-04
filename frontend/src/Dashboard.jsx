import { useEffect, useState } from "react";

import { apiRequest, getRequestError, getResponseError } from "./api";

const taskStatuses = [
  ["TODO", "Por fazer"],
  ["IN_PROGRESS", "Em progresso"],
  ["DONE", "Concluída"],
];
const statusLabels = Object.fromEntries(taskStatuses);

export default function Dashboard({ user, onOpenProject, onViewProjects }) {
  const [projects, setProjects] = useState([]);
  const [tasksByProject, setTasksByProject] = useState({});
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [reloadCount, setReloadCount] = useState(0);

  useEffect(() => {
    let active = true;

    async function loadDashboard() {
      setLoading(true);
      setMessage("");
      try {
        const projectsResponse = await apiRequest("/projects/");
        if (!projectsResponse.ok) {
          throw new Error(
            await getResponseError(
              projectsResponse,
              "Não foi possível carregar os projetos.",
            ),
          );
        }

        const accessibleProjects = await projectsResponse.json();
        const taskLists = await Promise.all(
          accessibleProjects.map(async (project) => {
            const response = await apiRequest(
              `/projects/${project.projectId}/tasks/`,
            );
            if (!response.ok) {
              throw new Error(
                await getResponseError(
                  response,
                  `Não foi possível carregar as tarefas de "${project.title}".`,
                ),
              );
            }
            return [project.projectId, await response.json()];
          }),
        );

        if (active) {
          setProjects(accessibleProjects);
          setTasksByProject(Object.fromEntries(taskLists));
        }
      } catch (error) {
        if (active) {
          setProjects([]);
          setTasksByProject({});
          setMessage(getRequestError(error, "Não foi possível carregar o painel inicial."));
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadDashboard();
    return () => {
      active = false;
    };
  }, [reloadCount]);

  const allTasks = projects.flatMap((project) =>
    (tasksByProject[project.projectId] || []).map((task) => ({
      ...task,
      projectTitle: project.title,
    })),
  );
  const taskCounts = Object.fromEntries(
    taskStatuses.map(([status]) => [
      status,
      allTasks.filter((task) => task.status === status).length,
    ]),
  );
  const assignedTasks = allTasks.filter((task) =>
    task.assigneeIds.includes(user.userId),
  );

  return (
    <section className="workspace-card dashboard" aria-labelledby="dashboard-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Matriz</p>
          <h1 id="dashboard-title">Painel inicial</h1>
          <p className="intro">Visão geral do trabalho</p>
        </div>
        <button disabled={loading} onClick={onViewProjects} type="button">
          Ver projetos
        </button>
      </div>

      {loading ? (
        <p aria-live="polite" className="loading-state">
          A carregar o painel...
        </p>
      ) : message ? (
        <div>
          <p className="form-message" role="alert">
            {message}
          </p>
          <button
            onClick={() => setReloadCount((current) => current + 1)}
            type="button"
          >
            Tentar novamente
          </button>
        </div>
      ) : (
        <>
          <div
            aria-label="Contagem total de tarefas por estado"
            className="dashboard-counts"
          >
            {taskStatuses.map(([status, label]) => (
              <section className="dashboard-count-card" key={status}>
                <span>{label}</span>
                <strong>{taskCounts[status]}</strong>
              </section>
            ))}
          </div>

          <div className="dashboard-columns">
            <section
              aria-labelledby="dashboard-projects-title"
              className="dashboard-section"
            >
              <h2 id="dashboard-projects-title">Projetos acessíveis</h2>
              {projects.length === 0 ? (
                <p className="empty-state">
                  Não há projetos acessíveis para apresentar.
                </p>
              ) : (
                <ul className="dashboard-list">
                  {projects.map((project) => {
                    const projectTasks = tasksByProject[project.projectId] || [];
                    const counts = Object.fromEntries(
                      taskStatuses.map(([status]) => [
                        status,
                        projectTasks.filter((task) => task.status === status)
                          .length,
                      ]),
                    );
                    return (
                      <li key={project.projectId}>
                        <button
                          className="dashboard-project-card"
                          onClick={() => onOpenProject(project.projectId)}
                          type="button"
                        >
                          <strong>{project.title}</strong>
                          <span>
                            {counts.TODO} por fazer · {counts.IN_PROGRESS} em
                            progresso · {counts.DONE} concluídas
                          </span>
                        </button>
                      </li>
                    );
                  })}
                </ul>
              )}
            </section>

            <section
              aria-labelledby="dashboard-tasks-title"
              className="dashboard-section"
            >
              <h2 id="dashboard-tasks-title">As minhas tarefas</h2>
              {assignedTasks.length === 0 ? (
                <p className="empty-state">
                  Não tens tarefas atribuídas nos projetos acessíveis.
                </p>
              ) : (
                <ul className="dashboard-list">
                  {assignedTasks.map((task) => (
                    <li key={task.taskId}>
                      <button
                        className="dashboard-task-card"
                        onClick={() => onOpenProject(task.projectId)}
                        type="button"
                      >
                        <strong>{task.title}</strong>
                        <span>
                          {task.projectTitle} · {statusLabels[task.status]}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>
        </>
      )}
    </section>
  );
}
