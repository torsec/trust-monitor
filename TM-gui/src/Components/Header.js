import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckDouble, faUserCircle } from "@fortawesome/free-solid-svg-icons";
import Search from './Search';
import { Navbar, Dropdown } from 'react-bootstrap';
import { useKeycloak } from "@react-keycloak/web";

export function Header({...props}) {
    const { toggleFunc, title, username } = props;
    //const { keycloak, initialized } = useKeycloak();

    return (
        <Navbar onToggle={toggleFunc} bg="success" expand="lg" className="d-flex justify-content-between" variant="dark">
            <Navbar.Toggle className="white-toggler d-block d-lg-none" aria-controls="toggleMenu" />
            <Navbar.Brand className="navbar-brand" href=""><FontAwesomeIcon icon={faCheckDouble} className={"mr-2"} />{title}</Navbar.Brand>
            {username ? 
                <Navbar.Brand className="navbar-brand" href="" align="rigth"><FontAwesomeIcon icon={faUserCircle} className={"mr-2"} />{username}</Navbar.Brand>
                :
                ""
            }
            {/*<Search />*/}
            {/*<Dropdown>
                <Dropdown.Toggle variant="success" className="d-flex align-items-center">
                    <FontAwesomeIcon className="navbar-user mr-2" icon={faUserCircle} />
                    username
                </Dropdown.Toggle>
                <Dropdown.Menu align={'right'} id="dropdown-menu-align-right">
                    {!false && (
                    <Dropdown.Item
                        onClick={() => {return} }
                    >
                        Login
                    </Dropdown.Item>
                    )}

                    {!!true && (
                    <Dropdown.Item
                        onClick={() => {return}}
                    >
                        Logout ({})
                    </Dropdown.Item>
                    )}
                </Dropdown.Menu>
                    </Dropdown>*/}
        </Navbar>
    );
}

export default Header;