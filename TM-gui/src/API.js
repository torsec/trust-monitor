/* import dayjs from 'dayjs'; */

const getTasksByFilter = async (selectedFilter) => {
  const response = await fetch(`/api/tasks?filter=${selectedFilter}`);
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const getAllEntities = async () => {
  const response = await fetch("/entity");
  const body = await response.json();
  if (response.ok) {
    return body.entities;
  } else {
    throw body.error;
  }
};

const addEntity = async (entity) => {
  const response = await fetch(`/entity`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(entity),
  });
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const deleteEntity = async (uuid) => {
  const response = await fetch(`/entity`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({entity_uuid: uuid}),
  });
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const editEntity = async (entity) => {
  const response = await fetch(`/entity`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(entity),
  });
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const API = {
  getTasksByFilter,
  getAllEntities,
  addEntity,
  deleteEntity,
  editEntity
};
export default API;
