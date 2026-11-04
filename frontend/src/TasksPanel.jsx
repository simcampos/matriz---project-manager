import { useEffect, useState } from "react";

import {
  apiRequest,
  ensureCsrfCookie,
  getCsrfCookie,
  getRequestError,
  getResponseError,
} from "./api";

const taskStatuses = [
  ["TODO", "Por fazer"],
  ["IN_PROGRESS", "Em progresso"],
  ["DONE", "Concluída"],
];
const taskPriorities = [
  ["LOW", "Baixa"],
  ["MEDIUM", "Média"],
  ["HIGH", "Alta"],
];
const statusLabels = Object.fromEntries(taskStatuses);
const priorityLabels = Object.fromEntries(taskPriorities);

function TaskForm({ task, onCancel, onSave, pending, message }) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [status, setStatus] = useState(task?.status || "TODO");
  const [priority, setPriority] = useState(task?.priority || "MEDIUM");

  function handleSubmit(event) {
    event.preventDefault();
    onSave({ title, description, status, priority });
  }

  return (
    <section className="task-editor" aria-labelledby="task-form-title">
      <h3 id="task-form-title">{task ? "Editar tarefa" : "Nova tarefa"}</h3>
      <form className="task-form" onSubmit={handleSubmit}>
        <label htmlFor="task-title">Título</label>
        <input
          autoComplete="off"
          id="task-title"
          maxLength={150}
          minLength={3}
          onChange={(event) => setTitle(event.target.value)}
          required
          value={title}
        />
        <label htmlFor="task-description">Descrição (opcional)</label>
        <textarea
          id="task-description"
          maxLength={2000}
          onChange={(event) => setDescription(event.target.value)}
          rows={4}
          value={description}
        />
        <div className="task-form-options">
          <label htmlFor="task-status">Estado</label>
          <select
            id="task-status"
            onChange={(event) => setStatus(event.target.value)}
            value={status}
          >
            {taskStatuses.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <label htmlFor="task-priority">Prioridade</label>
          <select
            id="task-priority"
            onChange={(event) => setPriority(event.target.value)}
            value={priority}
          >
            {taskPriorities.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
        {message && (
          <p className="form-message" role="alert">
            {message}
          </p>
        )}
        <div className="action-row">
          <button disabled={pending} type="submit">
            {pending ? "A guardar..." : "Guardar tarefa"}
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

export default function TasksPanel({ project, user, canManage }) {
  const [tasks, setTasks] = useState([]);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [taskListError, setTaskListError] = useState("");
  const [view, setView] = useState("list");
  const [selectedTask, setSelectedTask] = useState(null);
  const [failedTaskId, setFailedTaskId] = useState(null);
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [message, setMessage] = useState("");
  const [notice, setNotice] = useState("");
  const [pending, setPending] = useState(false);
  const [assignees, setAssignees] = useState([]);
  const [projectMembers, setProjectMembers] = useState([]);
  const [comments, setComments] = useState([]);
  const [selectedAssigneeId, setSelectedAssigneeId] = useState("");
  const [commentContent, setCommentContent] = useState("");

  async function requestProjectTasks() {
    const response = await apiRequest(
      `/projects/${project.projectId}/tasks/`,
    );
    if (!response.ok) {
      throw new Error(
        await getResponseError(response, "Não foi possível carregar as tarefas."),
      );
    }
    return response.json();
  }

  async function reloadTasks() {
    const projectTasks = await requestProjectTasks();
    setTasks(projectTasks);
    return projectTasks;
  }

  useEffect(() => {
    let active = true;
    setTasksLoading(true);
    setTaskListError("");

    async function loadTasks() {
      try {
        const projectTasks = await requestProjectTasks();
        if (active) {
          setTasks(projectTasks);
        }
      } catch (error) {
        if (active) {
          const loadError = getRequestError(
            error,
            "Não foi possível carregar as tarefas.",
          );
          setTaskListError(loadError);
          setMessage(loadError);
        }
      } finally {
        if (active) {
          setTasksLoading(false);
        }
      }
    }

    loadTasks();
    return () => {
      active = false;
    };
  }, [project.projectId]);

  async function retryTasks() {
    setTasksLoading(true);
    setTaskListError("");
    setMessage("");
    try {
      await reloadTasks();
    } catch (error) {
      const loadError = getRequestError(
        error,
        "Não foi possível carregar as tarefas.",
      );
      setTaskListError(loadError);
      setMessage(loadError);
    } finally {
      setTasksLoading(false);
    }
  }

  async function openTask(taskId) {
    setPending(true);
    setMessage("");
    setNotice("");
    setFailedTaskId(taskId);
    setView("loading-detail");
    try {
      const taskPath = `/projects/${project.projectId}/tasks/${taskId}`;
      const responses = await Promise.all([
        apiRequest(`${taskPath}/`),
        apiRequest(`${taskPath}/assignees/`),
        apiRequest(`/projects/${project.projectId}/members/`),
        apiRequest(`${taskPath}/comments/`),
      ]);
      const errors = [
        "Não foi possível abrir a tarefa.",
        "Não foi possível carregar os responsáveis.",
        "Não foi possível carregar os membros do projeto.",
        "Não foi possível carregar os comentários.",
      ];
      for (let index = 0; index < responses.length; index += 1) {
        if (!responses[index].ok) {
          throw new Error(
            await getResponseError(responses[index], errors[index]),
          );
        }
      }
      const [task, taskAssignees, members, taskComments] = await Promise.all(
        responses.map((response) => response.json()),
      );
      setSelectedTask(task);
      setAssignees(taskAssignees);
      setProjectMembers(members);
      setComments(taskComments);
      setSelectedAssigneeId("");
      setCommentContent("");
      setView("detail");
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível abrir a tarefa."));
      setView("detail-error");
    } finally {
      setPending(false);
    }
  }

  async function saveTask(values) {
    setPending(true);
    setMessage("");
    setNotice("");
    const editing = view === "edit";
    const taskUrl = editing
      ? `/projects/${project.projectId}/tasks/${selectedTask.taskId}/`
      : `/projects/${project.projectId}/tasks/`;
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(taskUrl, {
        method: editing ? "PATCH" : "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfCookie(),
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível guardar a tarefa."),
        );
      }
      const savedTask = await response.json();
      setSelectedTask(savedTask);
      if (!editing) {
        setAssignees([]);
        setProjectMembers([]);
        setComments([]);
      }
      setView("detail");
      setTasks((currentTasks) => [
        ...currentTasks.filter((task) => task.taskId !== savedTask.taskId),
        savedTask,
      ]);
      try {
        await reloadTasks();
      } catch (error) {
        setMessage(
          `A tarefa foi guardada, mas a lista não foi atualizada: ${getRequestError(error, "Não foi possível carregar as tarefas.")}`,
        );
      }
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível guardar a tarefa."));
    } finally {
      setPending(false);
    }
  }

  async function updateStatus(task, nextStatus) {
    setPending(true);
    setMessage("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/tasks/${task.taskId}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfCookie(),
          },
          body: JSON.stringify({ status: nextStatus }),
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível alterar o estado."),
        );
      }
      const savedTask = await response.json();
      setTasks((currentTasks) =>
        currentTasks.map((item) =>
          item.taskId === savedTask.taskId ? savedTask : item,
        ),
      );
      setSelectedTask((currentTask) =>
        currentTask?.taskId === savedTask.taskId ? savedTask : currentTask,
      );
      try {
        await reloadTasks();
      } catch (error) {
        setMessage(
          `O estado foi alterado, mas a lista não foi atualizada: ${getRequestError(error, "Não foi possível carregar as tarefas.")}`,
        );
      }
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível alterar o estado."));
    } finally {
      setPending(false);
    }
  }

  async function deleteTask() {
    if (!window.confirm(`Eliminar "${selectedTask.title}"?`)) {
      return;
    }
    setPending(true);
    setMessage("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/tasks/${selectedTask.taskId}/`,
        {
          method: "DELETE",
          headers: { "X-CSRFToken": getCsrfCookie() },
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível eliminar a tarefa."),
        );
      }
      setTasks((currentTasks) =>
        currentTasks.filter((task) => task.taskId !== selectedTask.taskId),
      );
      setSelectedTask(null);
      setView("list");
      try {
        await reloadTasks();
      } catch (error) {
        setMessage(
          `A tarefa foi eliminada, mas a lista não foi atualizada: ${getRequestError(error, "Não foi possível carregar as tarefas.")}`,
        );
      }
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível eliminar a tarefa."));
    } finally {
      setPending(false);
    }
  }

  async function addAssignee(event) {
    event.preventDefault();
    setPending(true);
    setMessage("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/tasks/${selectedTask.taskId}/assignees/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfCookie(),
          },
          body: JSON.stringify({ userId: Number(selectedAssigneeId) }),
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível atribuir o responsável."),
        );
      }
      const assignee = await response.json();
      setAssignees((current) => [...current, assignee]);
      setSelectedTask((current) => ({
        ...current,
        assigneeIds: [...current.assigneeIds, assignee.userId],
      }));
      setSelectedAssigneeId("");
      setNotice("Responsável atribuído.");
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível atribuir o responsável."));
    } finally {
      setPending(false);
    }
  }

  async function removeAssignee(assignee) {
    setPending(true);
    setMessage("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/tasks/${selectedTask.taskId}/assignees/${assignee.userId}/`,
        {
          method: "DELETE",
          headers: { "X-CSRFToken": getCsrfCookie() },
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível remover o responsável."),
        );
      }
      setAssignees((current) =>
        current.filter((item) => item.userId !== assignee.userId),
      );
      setSelectedTask((current) => ({
        ...current,
        assigneeIds: current.assigneeIds.filter(
          (userId) => userId !== assignee.userId,
        ),
      }));
      setNotice("Responsável removido.");
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível remover o responsável."));
    } finally {
      setPending(false);
    }
  }

  async function addComment(event) {
    event.preventDefault();
    setPending(true);
    setMessage("");
    setNotice("");
    try {
      await ensureCsrfCookie();
      const response = await apiRequest(
        `/projects/${project.projectId}/tasks/${selectedTask.taskId}/comments/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfCookie(),
          },
          body: JSON.stringify({ content: commentContent }),
        },
      );
      if (!response.ok) {
        throw new Error(
          await getResponseError(response, "Não foi possível adicionar o comentário."),
        );
      }
      const comment = await response.json();
      setComments((current) => [...current, comment]);
      setCommentContent("");
      setNotice("Comentário adicionado.");
    } catch (error) {
      setMessage(getRequestError(error, "Não foi possível adicionar o comentário."));
    } finally {
      setPending(false);
    }
  }

  const visibleTasks = tasks.filter(
    (task) =>
      (!statusFilter || task.status === statusFilter) &&
      (!priorityFilter || task.priority === priorityFilter),
  );
  const counts = Object.fromEntries(
    taskStatuses.map(([status]) => [
      status,
      tasks.filter((task) => task.status === status).length,
    ]),
  );

  return (
    <section className="tasks-section" aria-labelledby="tasks-title">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">Trabalho do projeto</p>
          <h2 id="tasks-title">Tarefas</h2>
        </div>
        {canManage && view === "list" && (
          <button
            disabled={pending || tasksLoading || Boolean(taskListError)}
            onClick={() => {
              setMessage("");
              setSelectedTask(null);
              setView("create");
            }}
            type="button"
          >
            Nova tarefa
          </button>
        )}
      </div>

      {tasksLoading ? (
        <p aria-live="polite" className="loading-state">
          A carregar tarefas e contagens...
        </p>
      ) : !taskListError ? (
        <div className="task-counts" aria-label="Contagem de tarefas por estado">
          {taskStatuses.map(([status, label]) => (
            <p key={status}>
              <strong>{counts[status]}</strong> {label}
            </p>
          ))}
        </div>
      ) : null}

      {message &&
        view !== "create" &&
        view !== "edit" &&
        view !== "detail-error" &&
        view !== "loading-detail" && (
        <p className="form-message" role="alert">
          {message}
        </p>
      )}
      {notice && (
        <p className="success-message" role="status">
          {notice}
        </p>
      )}

      {view === "list" && tasksLoading ? null : view === "list" && taskListError ? (
        <button disabled={pending} onClick={retryTasks} type="button">
          Tentar novamente
        </button>
      ) : view === "loading-detail" ? (
        <p aria-live="polite" className="loading-state">
          A carregar detalhe da tarefa...
        </p>
      ) : view === "detail-error" ? (
        <div>
          <p className="form-message" role="alert">
            {message}
          </p>
          <div className="action-row">
            <button
              disabled={pending}
              onClick={() => openTask(failedTaskId)}
              type="button"
            >
              Tentar novamente
            </button>
            <button
              className="secondary-button"
              disabled={pending}
              onClick={() => {
                setMessage("");
                setView("list");
              }}
              type="button"
            >
              Voltar às tarefas
            </button>
          </div>
        </div>
      ) : view === "create" || view === "edit" ? (
        <TaskForm
          message={message}
          onCancel={() => {
            setMessage("");
            setView(selectedTask ? "detail" : "list");
          }}
          onSave={saveTask}
          pending={pending}
          task={view === "edit" ? selectedTask : null}
        />
      ) : view === "detail" && selectedTask ? (
        <div className="task-detail">
          <button
            className="back-button"
            disabled={pending}
            onClick={() => setView("list")}
            type="button"
          >
            Voltar às tarefas
          </button>
          <h3>{selectedTask.title}</h3>
          <p className="task-description">
            {selectedTask.description || "Sem descrição."}
          </p>
          <dl className="task-metadata">
            <div>
              <dt>Estado</dt>
              <dd>{statusLabels[selectedTask.status]}</dd>
            </div>
            <div>
              <dt>Prioridade</dt>
              <dd>{priorityLabels[selectedTask.priority]}</dd>
            </div>
            <div>
              <dt>Responsáveis</dt>
              <dd>
                {assignees.length
                  ? assignees.map((assignee) => assignee.email).join(", ")
                  : "Sem responsáveis"}
              </dd>
            </div>
          </dl>
          <section className="task-detail-section" aria-labelledby="assignees-title">
            <h4 id="assignees-title">Responsáveis</h4>
            {assignees.length === 0 ? (
              <p className="empty-state">Ainda não há responsáveis.</p>
            ) : (
              <ul className="assignee-list">
                {assignees.map((assignee) => (
                  <li key={assignee.userId}>
                    <span>{assignee.email}</span>
                    {canManage && (
                      <button
                        className="secondary-button"
                        disabled={pending}
                        onClick={() => removeAssignee(assignee)}
                        type="button"
                      >
                        Remover
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            )}
            {canManage && (
              <form className="assignee-form" onSubmit={addAssignee}>
                <label htmlFor="eligible-assignee">
                  Atribuir membro do projeto
                </label>
                <select
                  id="eligible-assignee"
                  onChange={(event) => setSelectedAssigneeId(event.target.value)}
                  value={selectedAssigneeId}
                >
                  <option value="">Selecionar utilizador</option>
                  {projectMembers
                    .filter(
                      (member) =>
                        !assignees.some(
                          (assignee) => assignee.userId === member.userId,
                        ),
                    )
                    .map((member) => (
                      <option key={member.userId} value={member.userId}>
                        {member.email}
                      </option>
                    ))}
                </select>
                <button
                  disabled={pending || !selectedAssigneeId}
                  type="submit"
                >
                  Atribuir
                </button>
              </form>
            )}
          </section>
          <section className="task-detail-section" aria-labelledby="comments-title">
            <h4 id="comments-title">Comentários</h4>
            {comments.length === 0 ? (
              <p className="empty-state">Ainda não há comentários.</p>
            ) : (
              <ol className="comment-list">
                {comments.map((comment) => (
                  <li key={comment.commentId}>
                    <div className="comment-heading">
                      <strong>{comment.author.email}</strong>
                      <time dateTime={comment.createdAt}>
                        {new Intl.DateTimeFormat("pt-PT", {
                          dateStyle: "short",
                          timeStyle: "short",
                        }).format(new Date(comment.createdAt))}
                      </time>
                    </div>
                    <p>{comment.content}</p>
                  </li>
                ))}
              </ol>
            )}
            <form className="comment-form" onSubmit={addComment}>
              <label htmlFor="new-comment">Novo comentário</label>
              <textarea
                id="new-comment"
                maxLength={2000}
                onChange={(event) => setCommentContent(event.target.value)}
                required
                rows={3}
                value={commentContent}
              />
              <button disabled={pending} type="submit">
                {pending ? "A guardar..." : "Comentar"}
              </button>
            </form>
          </section>
          {canManage && (
            <div className="action-row">
              <button
                disabled={pending}
                onClick={() => {
                  setMessage("");
                  setView("edit");
                }}
                type="button"
              >
                Editar
              </button>
              <button
                className="danger-button"
                disabled={pending}
                onClick={deleteTask}
                type="button"
              >
                Eliminar
              </button>
            </div>
          )}
        </div>
      ) : (
        <>
          <div className="task-filters">
            <label htmlFor="task-status-filter">Estado</label>
            <select
              id="task-status-filter"
              onChange={(event) => setStatusFilter(event.target.value)}
              value={statusFilter}
            >
              <option value="">Todos</option>
              {taskStatuses.map(([status, label]) => (
                <option key={status} value={status}>
                  {label}
                </option>
              ))}
            </select>
            <label htmlFor="task-priority-filter">Prioridade</label>
            <select
              id="task-priority-filter"
              onChange={(event) => setPriorityFilter(event.target.value)}
              value={priorityFilter}
            >
              <option value="">Todas</option>
              {taskPriorities.map(([priority, label]) => (
                <option key={priority} value={priority}>
                  {label}
                </option>
              ))}
            </select>
          </div>
          {visibleTasks.length === 0 ? (
            <p className="empty-state">
              {tasks.length
                ? "Não existem tarefas correspondentes aos filtros."
                : "Este projeto ainda não tem tarefas."}
            </p>
          ) : (
            <ul className="task-list">
              {visibleTasks.map((task) => {
                const canUpdateStatus =
                  canManage ||
                  (user.role === "DEVELOPER" &&
                    task.assigneeIds.includes(user.userId));
                return (
                  <li className="task-card" key={task.taskId}>
                    <button
                      className="task-open"
                      disabled={pending}
                      onClick={() => openTask(task.taskId)}
                      type="button"
                    >
                      <strong>{task.title}</strong>
                      <span>{priorityLabels[task.priority]}</span>
                    </button>
                    <label htmlFor={`task-status-${task.taskId}`}>Estado</label>
                    {canUpdateStatus ? (
                      <select
                        disabled={pending}
                        id={`task-status-${task.taskId}`}
                        onChange={(event) =>
                          updateStatus(task, event.target.value)
                        }
                        value={task.status}
                      >
                        {taskStatuses.map(([status, label]) => (
                          <option key={status} value={status}>
                            {label}
                          </option>
                        ))}
                      </select>
                    ) : (
                      <span>{statusLabels[task.status]}</span>
                    )}
                  </li>
                );
              })}
            </ul>
          )}
        </>
      )}
    </section>
  );
}
