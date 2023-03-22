import { VerifierItem } from '.';
import { Alert, Spinner, Button } from 'react-bootstrap';

export function VerifierList({ ...props }) {
    const { verifiers, filter, loading, error, filterLoading } = props;

    //const orderedList = [...verifiersList].sort( (a, b) => a.entity_uuid - b.entity_uuid )

    const verifiers_ = [...verifiers].map( (verifier, index) => <VerifierItem key={index} {...verifier} />);
    return (
        <div className="col-lg-8 pt-3">
            <div className="d-flex justify-content-center align-items-center">
                <h1 className="d-flex justify-content-center">{filter === "/verifiers" ? 'Verifiers' : ""}</h1> {filterLoading && <span className="ml-4"><Spinner animation="border" role="status" variant="warning" /> </span>}
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
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Attestation tech</th>
                            <th className="col-1 d-flex align-items-center justify-content-center" scope="col">Infrastructure ID</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Metatdata</th>
                            <th className="col-2 d-flex align-items-center justify-content-center" scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {verifiers_}
                    </tbody>
                </table>
            </>
            }
        </div>
    );
}

export default VerifierList;