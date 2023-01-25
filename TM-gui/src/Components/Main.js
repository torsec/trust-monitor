import { Container, Row, Collapse } from "react-bootstrap";
import { Sidebar, EntityList, AddEditTask, ButtonRounded, Status } from "./";
import { useState, useEffect } from "react";
import API from "../API";
import { useRouteMatch } from "react-router-dom";
import { useKeycloak } from "@react-keycloak/web";

export function Main({ ...props }) {
  const { menuFilters, toggle, user } = props;
  const filter = useRouteMatch().path;
  //const { keycloak } = useKeycloak();

  //const isLoggedIn = keycloak.authenticated;
 
  const [entitiesList, setEntitiesList] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(filter ? false : true);
  const [filterLoading, setFilterLoading] = useState(filter ? true : false);
  const [showModal, setShowModal] = useState(false);
  const [refresh, setRefresh] = useState(true);
  const [entityToEdit, setEntityToEdit] = useState();
  const [attestLoading, setAttestLoading] = useState(false);
  const [uuidAttest, setUuidAttest] = useState();
  const [status, setStatus] = useState({});

  useEffect(() => {
    const getEntities = async () => {
      try {
        let list = [];
        let temp = {};
        if (filter === "/") {
          list = await API.getAllEntities();
          setLoading(false);
        }else {
          setLoading(true);
          temp = await API.getStatus();
          
          for (let i = 0; i < temp.att_processes.length; i++){
            const val = temp.att_processes[i];
            let trust = await API.getEntityReport(val.entity_uuid);
            for (let index = 0; index < temp.att_processes.length; index++) {
              if (temp.att_processes[index].entity_uuid === val.entity_uuid){
                temp.att_processes[index]["trust"] = trust;
              }
            }
          }

          setStatus(temp);
          setLoading(false);
        }
        
        setEntitiesList(list);
        if (filterLoading) {
          setFilterLoading(false);
        }
      } catch (err) {
        console.log(err);
      }
    };
    if (refresh) {
      getEntities();
      setRefresh(false);
    }
  }, [refresh, filter]);

  const attestEntity = async (uuid, start) => {
    setAttestLoading(true);
    setUuidAttest(uuid);
    if(start){
      await API.attestEntity(uuid);
    }
    else {
      await API.stopAttestEntity(uuid);
    }
    setRefresh(true);
    setAttestLoading(false);
    setUuidAttest(-1);
  }

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
  return ( true /*isLoggedIn*/ ?
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
          { (filter === "/") ?
            <>
              <EntityList
              entitiesList={entitiesList}
              selectEntityToEdit={selectEntityToEdit}
              deleteEntity={deleteEntity}
              attestEntity={attestEntity}
              attestLoading={attestLoading}
              uuidAttest={uuidAttest}
              setUuidAttest={setUuidAttest}
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
          </>
          :
          (
            (filter === "/status") ?
            <Status
              status={status}
              error={error}
              loading={loading}
              filterLoading={filterLoading}
              attestLoading={attestLoading}
              attestEntity={attestEntity}
            />
            :
            ""
          )
          }
      </Container>
    </main>
    :
    <p>Not Authenticated</p>
  );
}

export default Main;
