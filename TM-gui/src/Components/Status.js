import { Alert, Spinner, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStop } from "@fortawesome/free-solid-svg-icons";

export function Status({ ...props }) {
    const { status, error, loading, filterLoading, attestLoading, attestEntity } = props;

    return (
        <div className="col-lg-8 pt-3">
            <div className="d-flex justify-content-center align-items-center">
                <h1 className="d-flex justify-content-center">Status</h1> {filterLoading && <span className="ml-4"><Spinner animation="border" role="status" variant="warning" /> </span>}
            </div>
            
            {filterLoading ? 
                <div className="d-flex justify-content-center align-items-center">
                    <Button variant="primary" size="lg" disabled><Spinner as="span" animation="grow" size="sm" role="status" aria-hidden="true"/>Loading...</Button>
                </div>
                :
            <>
                {error && <Alert variant={'warning'}>{error}</Alert>}
                <table className="table">
                    <thead>
                        <tr className="d-flex">
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Loaded Adapters</th>
                        </tr>
                    </thead>
                    {status.adapters_loaded.length > 0 ?
                    <tbody>
                        {status.adapters_loaded.map(element => 
                            <td className="col-2 d-flex align-items-center justify-content-center">{element}</td>
                        )}
                    </tbody>
                    :
                    <p>None</p>
                    }
                </table>
                <h2>Attestation processes</h2>
                {status.att_processes.length > 0 ?
                <table className="table">
                    <thead>
                        <tr className="d-flex">
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Entity UUID</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Attestation tech</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Name</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">External ID</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Trust</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                    {status.att_processes.map(element =>
                    <tr className="d-flex">
                        <td className="col-1 d-flex align-items-center justify-content-center">{element.entity_uuid}</td>
                        <td className="col-2 d-flex align-items-center justify-content-center">{element.att_tech.toString()}</td>
                        <td className="col-2 d-flex align-items-center justify-content-center">{element.name}</td>
                        <td className="col-2 d-flex align-items-center justify-content-center">{element.external_id}</td>
                        <td className="col-1 d-flex align-items-center justify-content-center">{element.trust ? "True" : "False"}</td>
                        <td className="col-1 d-flex align-items-center justify-content-center">
                            { attestLoading ? 
                                <Spinner as="span" animation="grow" size="sm" role="status" aria-hidden="true"/>
                                :
                                <FontAwesomeIcon className="text-danger mr-1" icon={faStop} onClick={() => attestEntity(element.entity_uuid, false) } />
                            }
                        </td>
                    </tr>
                    )}
                    </tbody>
                </table>
                :
                <p>None</p>
                }
            </>
            }
        </div>
    );
}

export default Status;