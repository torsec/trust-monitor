import "bootstrap/dist/css/bootstrap.min.css";
import "../css/style.css";
import { Spinner, Container } from 'react-bootstrap'

export function InitialSpinner() {
    return (<main>
        <Container fluid className="login text-center">
            <div className='d-flex justify-content-center align-items-center'>
                <Spinner as="span" variant="success" animation="grow" style={{ width: '3rem', height: '3rem' }}/>
            </div>
        </Container>
    </main>);
}

export default InitialSpinner;