const taskForm = document.getElementById("task-form");
const taskList = document.getElementById("task-list");
const consoleOutput = document.getElementById("api-console");
const taskCount = document.getElementById("task-count");
const lastUpdated = document.getElementById("last-updated");
const template = document.getElementById("task-card-template");

const formatTimestamp = () => new Date().toLocaleTimeString();

const setConsole = (data) => {
  consoleOutput.textContent = JSON.stringify(data, null, 2);
  lastUpdated.textContent = formatTimestamp();
};

const handleResponse = async (response) => {
  const payload = await response.json();
  setConsole(payload);
  return payload;
};

const loadTasks = async () => {
  const response = await fetch("/tasks");
  const tasks = await handleResponse(response);
  taskList.innerHTML = "";

  if (!tasks.length) {
    const empty = document.createElement("p");
    empty.textContent = "No tasks yet. Create one to get started.";
    empty.classList.add("task-id");
    taskList.appendChild(empty);
  } else {
    tasks.forEach(renderTask);
  }

  taskCount.textContent = tasks.length;
};

const renderTask = (task) => {
  const node = template.content.cloneNode(true);
  const card = node.querySelector(".task-card");
  const titleInput = node.querySelector(".task-title");
  const descriptionInput = node.querySelector(".task-description");
  const idLabel = node.querySelector(".task-id");
  const actions = node.querySelector(".task-actions");

  titleInput.value = task.title;
  descriptionInput.value = task.description ?? "";
  idLabel.textContent = `Task ID: ${task.id}`;

  actions.addEventListener("click", async (event) => {
    const target = event.target.closest("button");
    if (!target) {
      return;
    }

    if (target.dataset.action === "save") {
      const response = await fetch(`/tasks/${task.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: titleInput.value,
          description: descriptionInput.value,
        }),
      });
      await handleResponse(response);
      await loadTasks();
    }

    if (target.dataset.action === "delete") {
      const response = await fetch(`/tasks/${task.id}`, {
        method: "DELETE",
      });
      await handleResponse(response);
      await loadTasks();
    }
  });

  taskList.appendChild(node);
};

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(taskForm);
  const payload = {
    title: formData.get("title"),
    description: formData.get("description"),
  };

  const response = await fetch("/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  await handleResponse(response);
  taskForm.reset();
  await loadTasks();
});

loadTasks();
