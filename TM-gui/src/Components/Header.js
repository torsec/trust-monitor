import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckDouble, faUserCircle } from "@fortawesome/free-solid-svg-icons";
import Search from './Search';
import { Navbar, Dropdown } from 'react-bootstrap';
import { useKeycloak } from "@react-keycloak/web";

export function Header({...props}) {
    const { toggleFunc, title } = props;
    //const { keycloak, initialized } = useKeycloak();

    return (
        <Navbar onToggle={toggleFunc} bg="success" expand="lg" className="d-flex justify-content-between" variant="dark">
            <Navbar.Toggle className="white-toggler d-block d-lg-none" aria-controls="toggleMenu" />
            <Navbar.Brand className="navbar-brand" href="#home"><FontAwesomeIcon icon={faCheckDouble} className={"mr-2"} />{title}</Navbar.Brand>
            {/*<Search />*/}
            {/*<Dropdown drop={'down'}>
                <Dropdown.Toggle variant="success" className="d-flex align-items-center">
                    <FontAwesomeIcon className="navbar-user mr-2" icon={faUserCircle} />
                    username
                </Dropdown.Toggle>
                <Dropdown.Menu align={'right'} id="dropdown-menu-align-right">
                    {!keycloak.authenticated && (
                    <Dropdown.Item
                        onClick={() => keycloak.login()}
                    >
                        Login
                    </Dropdown.Item>
                    )}

                    {!!keycloak.authenticated && (
                    <Dropdown.Item
                        onClick={() => keycloak.logout()}
                    >
                        Logout ({keycloak.tokenParsed.preferred_username})
                    </Dropdown.Item>
                    )}
                </Dropdown.Menu>
                    </Dropdown>*/}
        </Navbar>
    );
}

export default Header;