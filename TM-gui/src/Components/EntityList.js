import { EntityItem } from '.';
import { Alert, Spinner, Button } from 'react-bootstrap';

export function EntityList({ ...props }) {
    const { entitiesList, selectEntityToEdit, deleteEntity, attestEntity, attestLoading, uuidAttest, setUuidAttest, filter, loading, error, filterLoading } = props;

    const orderedList = [...entitiesList].sort( (a, b) => a.entity_uuid - b.entity_uuid )

    const entities = [...orderedList].map( (entity) => <EntityItem key={entity.entity_uuid} {...entity} deleteEntity={deleteEntity} attestEntity={attestEntity} attestLoading={attestLoading} uuidAttest={uuidAttest} setUuidAttest={setUuidAttest} selectEntityToEdit={selectEntityToEdit} />);
    return (
        <div className="col-lg-8 pt-3">
            <div className="d-flex justify-content-center align-items-center">
                <h1 className="d-flex justify-content-center">{filter === "/" ? 'Entities' : ""}</h1> {filterLoading && <span className="ml-4"><Spinner animation="border" role="status" variant="warning" /> </span>}
            </div>
            
            {loading ? 
                <div className="d-flex justify-content-center align-items-center">
                    <Button variant="primary" size="lg" disabled><Spinner as="span" animation="grow" size="sm" role="status" aria-hidden="true"/>Loading...</Button>
                </div>
                :
            <>
                {error && <Alert variant={'warning'}>{error}</Alert>}
                <table className="table">
                    <thead>
                        <tr className="d-flex">
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Entity UUID</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Infrastructure ID</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Attestation tech</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Name</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">External ID</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Type</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Whitelist UUID</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Child</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Parent</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">State</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Metatdata</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {entities}
                    </tbody>
                </table>
            </>
            }
        </div>
    );
}

export default EntityList;