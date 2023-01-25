
const ip = "127.0.0.1"
const port = "5080"
const baseURL = `http://${ip}:${port}`

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
  const response = await fetch(`${baseURL}/entity`);
  const body = await response.json();
  if (response.ok) {
    return body.entities;
  } else {
    throw body.error;
  }
};

const addEntity = async (entity) => {
  const response = await fetch(`${baseURL}/entity`, {
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
  const response = await fetch(`${baseURL}/entity`, {
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
  const response = await fetch(`${baseURL}/entity`, {
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

const attestEntity = async (uuid) => {
  const response = await fetch(`${baseURL}/attest_entity`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "entity_uuid": uuid
    }),
  });
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
}

const stopAttestEntity = async (uuid) => {
  const response = await fetch(`${baseURL}/attest_entity`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "entity_uuid": uuid
    }),
  });
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
}

const getStatus = async () => {
  const response = await fetch(`${baseURL}/status`);
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
}

const getEntityReport = async (uuid) => {
  const response = await fetch(`${baseURL}/report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "entity_uuid": uuid,
      "last": true
    }),
  });
  const body = await response.json();
  if (response.ok) {
    return body.report_list[0].trust;
  } else {
    throw body.error;
  }
}

const API = {
  getTasksByFilter,
  getAllEntities,
  addEntity,
  deleteEntity,
  editEntity,
  attestEntity,
  stopAttestEntity,
  getStatus,
  getEntityReport
};
export default API;
