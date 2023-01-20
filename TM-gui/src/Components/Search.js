import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from "@fortawesome/free-solid-svg-icons";

export function Search() {
    return (
        <div className="flex d-none d-lg-block">
            <div className="input-group">
            <input className="form-control border-white me-2" type="search" placeholder="Search" aria-label="Search" />
            <div className="input-group-append">
                <button className="btn btn-outline-white" type="button"><FontAwesomeIcon icon={faSearch} /></button>
            </div>
            </div>
        </div>
    );
}

export default Search;