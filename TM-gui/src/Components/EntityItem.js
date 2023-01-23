import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, Collapse, Card, Spinner } from 'react-bootstrap';
import { faUser , faPencilAlt, faTrash, faPlay, faStop } from "@fortawesome/free-solid-svg-icons";
import { useState } from 'react';

export function EntityItem({...props}) {
    const { entity_uuid, inf_id, att_tech, name, external_id, type, whitelist_uuid, child, parent, metadata, state, deleteEntity, attestEntity, attestLoading, uuidAttest, setUuidAttest, selectEntityToEdit, deleted, edited, isNew } = props;
    
    const [open, setOpen] = useState(false);

    return (
        <tr className={`d-flex ${deleted? 'table-danger' : ''} ${ edited? 'table-warning' : ''} ${ isNew ? 'table-success' : ''}`} >
            <td className="col-1 d-flex align-items-center justify-content-center">{entity_uuid}</td>
            <td className="col-1 d-flex align-items-center justify-content-center">{inf_id}</td>
            <td className="col-2 d-flex align-items-center justify-content-center">{att_tech ? att_tech.toString() : ""}</td>
            <td className="col-2 d-flex align-items-center justify-content-center">{name}</td>
            <td className="col-2 d-flex align-items-center justify-content-center">{external_id}</td>
            <td className="col-1 d-flex align-items-center justify-content-center">{type}</td>
            <td className="col-1 d-flex align-items-center justify-content-center">{whitelist_uuid}</td>
            <td className="col-2 d-flex align-items-center justify-content-center">{child ? child.toString() : ""}</td>
            <td className="col-1 d-flex align-items-center justify-content-center">{parent}</td>
            <td className="col-2 d-flex align-items-center justify-content-center">
                <>
                    <p>{state}</p>
                    { (attestLoading && entity_uuid === uuidAttest) ? <Spinner as="span" animation="grow" size="sm" role="status" aria-hidden="true"/> : (
                        state === "registered" ?
                        <FontAwesomeIcon className="mr-1" icon={faPlay} onClick={() => attestEntity(entity_uuid, true) } />
                        :
                        <FontAwesomeIcon className=" text-danger mr-1" icon={faStop} onClick={() => attestEntity(entity_uuid, false) } />
                        )
                    }
                </>
            </td>
            <td className="col-2 d-flex align-items-center justify-content-center">
            <>
                <Button
                    onClick={() => setOpen((open) => !open)}
                    aria-controls="example-collapse-text"
                    aria-expanded={open}
                >
                    { !open ? "Show" : "Hide" }
                </Button>
                <div style={{ minHeight: '100px' }}>
                    <Collapse in={open} dimension="width">
                    <div id="example-collapse-text">
                        <Card body style={{ width: 'auto' }}>
                        {metadata ? JSON.stringify(metadata) : ""}
                        </Card>
                    </div>
                    </Collapse>
                </div>
            </>
            </td>
            <td className="col-1 d-flex align-items-center justify-content-center">
                { open ? "" :
                <>
                    <FontAwesomeIcon className="text-warning mr-1" icon={faPencilAlt} onClick={() => selectEntityToEdit(entity_uuid) } />
                    <FontAwesomeIcon className="text-danger ml-1" icon={faTrash} onClick={() => deleteEntity(entity_uuid) } />
                </>
                }
            </td>
        </tr>
    );
}

export default EntityItem;