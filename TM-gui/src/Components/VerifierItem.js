import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, Collapse, Card, Spinner } from 'react-bootstrap';
import { faUser , faPencilAlt, faTrash, faPlay, faStop } from "@fortawesome/free-solid-svg-icons";
import { useState } from 'react';

export function EntityItem({...props}) {
    const { att_tech, inf_id, metadata/*, deleted, edited, isNew*/ } = props;
    
    const [open, setOpen] = useState(false);

    return (
        <>
        {/*<tr className={`d-flex ${deleted? 'table-danger' : ''} ${ edited? 'table-warning' : ''} ${ isNew ? 'table-success' : ''}`} >*/}
        <tr className='d-flex'>
            <td className="col-2 d-flex align-items-center justify-content-center">{att_tech ? att_tech.toString() : ""}</td>
            <td className="col-1 d-flex align-items-center justify-content-center">{inf_id}</td>
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
            <td className="col-2 d-flex align-items-center justify-content-center">
                { open ? "" :
                <>
                    {/*<FontAwesomeIcon className="text-warning mr-1" icon={faPencilAlt} onClick={() => null } />*/}
                    <FontAwesomeIcon className="text-danger ml-1" icon={faTrash} onClick={() => null } />
                </>
                }
            </td>
        </tr>
        </>
    );
}

export default EntityItem;