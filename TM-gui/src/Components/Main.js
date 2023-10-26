import { Container, Row, Collapse, ListGroup } from "react-bootstrap";
import { Sidebar, EntityList, AddEditTask, ButtonRounded, Status, VerifierList } from "./";
import { useState, useEffect } from "react";
import API from "../API";
import { useRouteMatch } from "react-router-dom";
import { subPath } from "../DataBase";
//import { useKeycloak } from "@react-keycloak/web";

export function Main({ ...props }) {
  const { menuFilters, toggle, user, session } = props;
  const filter = useRouteMatch().path;
  //const { keycloak } = useKeycloak();

  //const isLoggedIn = keycloak.authenticated;
 
  const [entitiesList, setEntitiesList] = useState([]);
  const [verifiersList, setVerifiersList] = useState([]);
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
        if (filter === subPath) {
          list = await API.getAllEntities(session);
          setEntitiesList(list);
          setLoading(false);
        }else {
          if (filter === subPath+"/status") {
            setLoading(true);
            temp = await API.getStatus(session);
            
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
          else{
            setLoading(true);
            list = await API.getAllVerifiers(session);
            setVerifiersList(list);
            setLoading(false);
          }
        }
        
        if (filterLoading) {
          setFilterLoading(false);
        }
      } catch (err) {
        //setEntitiesList([]);
        if(Object.keys(err).length === 0){
          console.log(JSON.stringify(err));
          setError("Error Trust Monitor: net::ERR_CERT_AUTHORITY_INVALID");
        }
        else{
          console.log(err);
          setError(err);
        }
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
      await API.attestEntity(uuid, session);
    }
    else {
      await API.stopAttestEntity(uuid, session);
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
    await API.deleteEntity(uuid, session);
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
                session={session}
              />
            </nav>
          </Collapse>
          { error ? <span className="urgent">{error}</span> :
            ((filter === subPath) ?
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
                session={session}
              />
            </>
            :
            (
              (filter === subPath+"/status") ?
              <Status
                status={status}
                error={error}
                loading={loading}
                filterLoading={filterLoading}
                attestLoading={attestLoading}
                attestEntity={attestEntity}
              />
              :
              (
                (filter === subPath+"/verifiers") ?
                <VerifierList
                  verifiers={verifiersList}
                  filter={filter}
                  loading={loading}
                  error={error}
                  filterLoading={filterLoading}
                />
                :
                ""
              )
            )
            )
          }
      </Container>
    </main>
    :
    <p>Not Authenticated</p>
  );
}

export default Main;
