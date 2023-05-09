import { Modal, Button, Form, Col, Alert, Spinner } from "react-bootstrap";
import { useState, useEffect } from "react";
import API from "../API";

export function AddEditTask({ ...props }) {
  const { addEntity, editEntity, setRefresh, entityToEdit, onHide, show, user, session } =
    props;
  const [error, setError] = useState();
  const [loading, setLoading] = useState(false);
  const [validated, setValidated] = useState(false);

  /* Form inputs Handler */
  const [entityUuid, setEntityUuid] = useState("");
  const [name, setName] = useState("");
  const [type, setType] = useState("");
  const [infId, setInfId] = useState("");
  const [attTech, setAttTech] = useState("");
  const [externalId, setExternalId] = useState("");
  const [whitelistUiid, setWhitelistUuid] = useState("");
  const [child, setChild] = useState("");
  const [parent, setParent] = useState("");
  const [metadata, setMetadata] = useState("");

  useEffect(() => {
    if (show) {
      console.log(entityToEdit);
      setError();
      setEntityUuid(entityToEdit ? entityToEdit.entity_uuid : "");
      setInfId(entityToEdit ? entityToEdit.inf_id : "");
      setAttTech(entityToEdit ? (entityToEdit.att_tech ? entityToEdit.att_tech.toString() : "") : "");
      setName(entityToEdit ? entityToEdit.name : "");
      setType(entityToEdit ? entityToEdit.type : "");
      setExternalId(entityToEdit ? (entityToEdit.external_id ? entityToEdit.external_id : "") : "");
      setWhitelistUuid(entityToEdit ? (entityToEdit.whitelist_uuid ? entityToEdit.whitelist_uuid : "") : "");
      setChild(entityToEdit ? (entityToEdit.child ? entityToEdit.child.toString() : "") : "");
      setParent(entityToEdit ? (entityToEdit.parent ? entityToEdit.parent : "") : "");
      setMetadata(entityToEdit ? (entityToEdit.metadata ? JSON.stringify(entityToEdit.metadata) : "") : "");
    }
  }, [show, entityToEdit]);

  const handleChangeEntityUuid = (event) => {
    setEntityUuid(event.target.value);
  };
  const handleChangeInfId = (event) => {
    setInfId(event.target.value);
  };
  const handleChangeAttTech = (event) => {
    setAttTech(event.target.value);
  };
  const handleChangeName = (event) => {
    setName(event.target.value);
  };
  const handleChangeType = (event) => {
    setType(event.target.value);
  };
  const handleChangeExternalId = (event) => {
    setExternalId(event.target.value);
  };
  const handleChangeWhitelistUuid = (event) => {
    setWhitelistUuid(event.target.value);
  };
  const handleChangeChild = (event) => {
    setChild(event.target.value);
  };
  const handleChangeParent = (event) => {
    setParent(event.target.value);
  };
  const handleChangeMetadata = (event) => {
    setMetadata(event.target.value);
  };

  /* Form Actions Handler */
  const submitTask = async (event) => {
    const form = event.currentTarget;
    event.preventDefault();
    event.stopPropagation();
    setError();
    if (form.checkValidity() === true) {
      setLoading(true);
      if (entityToEdit) {
        var editedEntity = {
          entity_uuid: parseInt(entityUuid, 10),
          inf_id: parseInt(infId, 10),
          att_tech: attTech ? attTech.split(",") : null,
          name: name,
          external_id: externalId,
          type: type,
          whitelist_uuid: whitelistUiid ? parseInt(whitelistUiid, 10) : null,
          child: child ? child.split(",").map( val => parseInt(val, 10)) : null,
          metadata: JSON.parse(metadata)
        };
        if (editedEntity.child === null) delete editedEntity.child;
        if (editedEntity.whitelist_uuid === null) delete editedEntity.whitelist_uuid;
        if (editedEntity.att_tech === null) delete editedEntity.att_tech;

        const tmp = editedEntity;
        
        API.editEntity(tmp, session)
          .then(() => {
            editEntity(tmp);
            setRefresh(true);
            setLoading(false);
            onHide();
            resetTask();
          })
          .catch((error) => {
            console.log(error);
            setError(JSON.stringify(error));
            setRefresh(true);
            setLoading(false);
          });
      } else {
        var newEntity = {
          entity_uuid: parseInt(entityUuid, 10),
          inf_id: parseInt(infId, 10),
          att_tech: attTech ? attTech.split(",") : null,
          name: name,
          external_id: externalId,
          type: type,
          whitelist_uuid: whitelistUiid ? parseInt(whitelistUiid, 10) : null,
          child: child ? child.split(",").map( val => parseInt(val, 10)) : null,
          metadata: metadata ? JSON.parse(metadata) : {}
        };
        if (newEntity.child === null) delete newEntity.child;
        if (newEntity.whitelist_uuid === null) delete newEntity.whitelist_uuid;
        if (newEntity.att_tech === null) delete newEntity.att_tech;

        const tmp = newEntity;
        
        API.addEntity(tmp, session)
          .then(() => {
            addEntity(tmp);
            setRefresh(true);
            setLoading(false);
            onHide();
            resetTask();
          })
          .catch((error) => {
            console.log(error);
            setError(JSON.stringify(error));
            setRefresh(true);
            setLoading(false);
          });
      }
    } else {
      setValidated(true);
    }
  };

  const resetTask = () => {
    setError();
    setName("");
    setType("");
    setInfId("");
    setAttTech("");
    setExternalId("");
    setWhitelistUuid("");
    setChild("");
    setParent("");
    setMetadata("");
  };

  return (
    <Modal
      onHide={onHide}
      show={show}
      size="md"
      aria-labelledby="add-new-entity-title"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="add-new-entity-title">
          {entityToEdit ? "Edit" : "Add new"} Entity
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form
          noValidate
          validated={validated}
          onSubmit={(event) => submitTask(event)}
        >
          <Form.Group>
            <Form.Label>
              Entity UUID <span className="urgent">*</span>
            </Form.Label>
            <Form.Control
              disabled={entityToEdit ? true : false}
              readOnly={entityToEdit ? true : false}
              required
              type="number"
              value={entityUuid}
              placeholder="entity_uuid"
              onChange={(event) => handleChangeEntityUuid(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid entity UUID.
            </Form.Control.Feedback>
            {/*<Form.Text className="text-muted">
              Insert here your todo description
              </Form.Text>*/}
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Infrastructure ID <span className="urgent">*</span>
            </Form.Label>
            <Form.Control
              required
              type="number"
              value={infId}
              placeholder="inf_id"
              onChange={(event) => handleChangeInfId(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid Infrastructure ID.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Attestation technologies <span className="urgent">*</span>
            </Form.Label>
            <Form.Control
              requested
              type="text"
              value={attTech}
              placeholder="att_tech_1,att_tech_2,..."
              onChange={(event) => handleChangeAttTech(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid attestation technologies.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Name <span className="urgent">*</span>
            </Form.Label>
            <Form.Control
              required
              type="text"
              value={name}
              placeholder="name"
              onChange={(event) => handleChangeName(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid entity name.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              External ID
            </Form.Label>
            <Form.Control
              type="text"
              value={externalId}
              placeholder="external_id"
              onChange={(event) => handleChangeExternalId(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid Infrastructure ID.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Type <span className="urgent">*</span>
            </Form.Label>
            <Form.Control
              required
              type="text"
              value={type}
              placeholder="type"
              onChange={(event) => handleChangeType(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid type.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Whitelist UUID
            </Form.Label>
            <Form.Control
              type="number"
              value={whitelistUiid}
              placeholder="whitelist_uuid"
              onChange={(event) => handleChangeWhitelistUuid(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid Whitelist UUID.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Child
            </Form.Label>
            <Form.Control
              type="text"
              value={child}
              placeholder="[uuid_1,uuid_2,...]"
              onChange={(event) => handleChangeChild(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid child.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Parent
            </Form.Label>
            <Form.Control
              type="number"
              value={parent}
              placeholder="parent"
              onChange={(event) => handleChangeParent(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid parent ID.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Group>
            <Form.Label>
              Metatdata
            </Form.Label>
            <Form.Control
              as="textarea"
              rows={5}
              value={metadata}
              placeholder="metadata"
              onChange={(event) => handleChangeMetadata(event)}
            />
            <Form.Control.Feedback type="invalid">
              Please fill with a valid metadta.
            </Form.Control.Feedback>
          </Form.Group>
          <Form.Row
            className={"d-flex justify-content-center align-items-center"}
          >
            {error && <Alert variant={"warning"}>{error}</Alert>}
          </Form.Row>
          <Modal.Footer>
            <Form.Group>
              <Button
                className="d-flex align-items-center"
                variant="warning"
                type="button"
                onClick={() => resetTask()}
								disabled={loading}
              >
                Reset
              </Button>
            </Form.Group>
            <Form.Group>
              <Button
                className="d-flex align-items-center"
                variant="success"
                type="submit"
                disabled={loading}
              >
                {loading && <Spinner animation="border" size="sm" />}
                {entityToEdit ? "Save" : "Add"}
              </Button>
            </Form.Group>
          </Modal.Footer>
        </Form>
      </Modal.Body>
    </Modal>
  );
}

export default AddEditTask;
