import { Container, Row, Collapse } from "react-bootstrap";
import { Sidebar, EntityList, AddEditTask, ButtonRounded } from "./";
import { useState, useEffect } from "react";
import API from "../API";
import { useRouteMatch } from "react-router-dom";

export function Main({ ...props }) {
  const { menuFilters, toggle, user } = props;
  const filter = useRouteMatch().params.filter;

  const [entitiesList, setEntitiesList] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(filter ? false : true);
  const [filterLoading, setFilterLoading] = useState(filter ? true : false);
  const [showModal, setShowModal] = useState(false);
  const [refresh, setRefresh] = useState(true);
  const [entityToEdit, setEntityToEdit] = useState();

  useEffect(() => {
    const getEntities = async () => {
      try {
        let list = [];
        if (true /*!filter*/) {
          list = await API.getAllEntities();
          setLoading(false);
        } else {
          if (menuFilters.find((item) => item.name === filter)) {
            list = await API.getTasksByFilter(filter);
          } else {
            list = await API.getTasksByFilter("All");
          }
        }
        setEntitiesList(list);
        if (filterLoading) {
          setFilterLoading(false);
        }
      } catch (err) {
        setError(err.error);
      }
    };
    if (refresh) {
      getEntities();
      setRefresh(false);
    }
  }, [refresh, filter]);

  const selectEntityToEdit = (uuid) => {
    const list = [...entitiesList];
    setEntityToEdit(list.filter((entity) => entity.entity_uuid === uuid)[0]);
    handleShowNewTask();
  };

  const deleteEntity = async (uuid) => {
    setEntitiesList((entitiesList) =>
      entitiesList.map((entity) => {
        if (entity.entity_uuid === uuid) return { ...entity, deleted: true };
        else return entity;
      })
    );
    await API.deleteEntity(uuid);
    setRefresh(true);
  };

  /* Modal View Handler */
  const handleCloseNewTask = () => {
    setShowModal(false);
    setEntityToEdit();
  };
  const handleShowNewTask = () => {
    setShowModal(true);
  };

  /* Entity list Add/Remove/Edit Handler */
  const editEntity = (entityEdit) => {
    setEntitiesList((list) =>
      list.map((entity) =>
        entity.entity_uuid === entityEdit.entity_uuid ? Object.assign({}, entityEdit) : entity
      )
    );
  };

  const addEntity = (entityNew) => {
    setEntitiesList((list) => [...list, entityNew]);
  };

  //const tasks = API.getTasks(filter);
  return (
    <main>
      <Container fluid>
       
          <Collapse in={toggle}>
            <nav id="toggleMenu" className="col-4 d-lg-block sidebar pt-3">
              <Sidebar
                menuFilters={menuFilters}
                setRefresh={setRefresh}
                filter={filter}
                setFilterLoading={setFilterLoading}
              />
            </nav>
          </Collapse>
          <EntityList
            entitiesList={entitiesList}
            selectEntityToEdit={selectEntityToEdit}
            deleteEntity={deleteEntity}
            filter={filter}
            loading={loading}
            error={error}
            filterLoading={filterLoading}
          />
          <ButtonRounded addTaskFunc={handleShowNewTask} />
          <AddEditTask
            user={user}
            editEntity={editEntity}
            addEntity={addEntity}
            setRefresh={setRefresh}
            entityToEdit={entityToEdit}
            show={showModal}
            onHide={handleCloseNewTask}
          />
       
      </Container>
    </main>
  );
}

export default Main;
