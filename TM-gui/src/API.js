
const ip = "10.4.34.136" //"10.4.34.139" //"trust-monitor" //"127.0.0.1"
const port = 31012 //32580 // "5080" //"5443"
const baseURL =  `https://${ip}:${port}` //`https://${ip}:${port}`

const getTasksByFilter = async (selectedFilter) => {
  const response = await fetch(`/api/tasks?filter=${selectedFilter}`);
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const getAllEntities = async (token) => {
  const response = await fetch(`${baseURL}/entity?token=${token}`);
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const getAllVerifiers = async (token) => {
  const response = await fetch(`${baseURL}/verifier?token=${token}`);
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
};

const addEntity = async (entity, token) => {
  const response = await fetch(`${baseURL}/entity?token=${token}`, {
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

const deleteEntity = async (uuid, token) => {
  const response = await fetch(`${baseURL}/entity?token=${token}`, {
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

const editEntity = async (entity, token) => {
  const response = await fetch(`${baseURL}/entity?token=${token}`, {
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

const attestEntity = async (uuid, token) => {
  const response = await fetch(`${baseURL}/attest_entity?token=${token}`, {
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

const stopAttestEntity = async (uuid, token) => {
  const response = await fetch(`${baseURL}/attest_entity?token=${token}`, {
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

const getStatus = async (token) => {
  const response = await fetch(`${baseURL}/status?token=${token}`);
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    throw body.error;
  }
}

const getEntityReport = async (uuid, token) => {
  const response = await fetch(`${baseURL}/report?token=${token}`, {
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
    return body;
  } else {
    throw body.error;
  }
}

/*const verifyToken = async (token) => {
  var details = {
    'access_token': token
  };

  var formBody = [];
  for (var property in details) {
    var encodedKey = encodeURIComponent(property);
    var encodedValue = encodeURIComponent(details[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  formBody = formBody.join("&");

  const response = await fetch(`https://fishy-idm.dsi.uminho.pt/auth/realms/fishy-realm/protocol/openid-connect/userinfo`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formBody
  });
  const body = await response.json();
  if (response.ok) {
    return body;
  } else {
    return body;
  }
};*/

const API = {
  getTasksByFilter,
  getAllEntities,
  getAllVerifiers,
  addEntity,
  deleteEntity,
  editEntity,
  attestEntity,
  stopAttestEntity,
  getStatus,
  getEntityReport,
  //verifyToken
};
export default API;
