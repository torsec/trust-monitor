import { ButtonGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { useState } from 'react';

export function Sidebar({...props}) {
    const { menuFilters, setRefresh, filter, setFilterLoading } = props;

    const [activeFilter, setActiveFilter] = useState(filter || 'All');

    const buttons = menuFilters.map( (val, index) =>  <Link 
        key={index} 
        onClick={() => {
                        setRefresh(true);
                        setActiveFilter(val.name);
                        setFilterLoading(true);
                    }}
        className={`list-group-item list-group-item-action ${activeFilter === val.name ? 'active': ''}`} 
        to={`/filter/${val.name}`}>{val.name}
    </Link>);
    return (
        <>
            <SidebarSearch />
            <ButtonGroup className="d-flex list-group list-group-flush">
                {buttons}
            </ButtonGroup>                           
        </>
    );
}

function SidebarSearch() {
    return (
        <div className="dflex d-lg-none pb-3">
            <div className="input-group">
                <input className="form-control border-success me-2" type="search" placeholder="Search" aria-label="Search" />
                <div className="input-group-append">
                    <button className="btn btn-outline-success" type="button"><FontAwesomeIcon icon={faSearch} /></button>
                </div>
            </div>
        </div>
    );
}

export default Sidebar;