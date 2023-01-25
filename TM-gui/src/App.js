import "bootstrap/dist/css/bootstrap.min.css";
import "./css/style.css";
import { Header, Main, InitialSpinner } from "./Components";
import { useState, React, useEffect } from "react";
import { menuFilters } from "./DataBase";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import Keycloak from 'keycloak-js';
import { ReactKeycloakProvider } from "@react-keycloak/web";
import API from "./API";

function App() {
  const [toggle, setToggle] = useState(false);
  //const [keycloak, setKeycloak] = useState(null)
  const [authenticated, setAuthenticated] = useState(false)

  /*const keycloak = new Keycloak({
    url: "http://localhost:8080/auth",
    realm: "tmrealm",
    clientId: "tmclient",
  });*/

  /*useEffect(()=>{
    

    keycloak.init({ onLoad: 'login-required' }).then(authenticated => {
      setKeycloak(keycloak)
      setAuthenticated(authenticated)
    })
  }, [])*/

  const hideShow = () => {
    setToggle((toggle) => !toggle);
  };

  return (
    /*<ReactKeycloakProvider authClient={keycloak}>*/
        <Router>
          <Switch>
          <Route path="/entities">
              <Redirect to="/"/>
            </Route>
            <Route path="/verifiers">
            <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                  />
            </Route>
            <Route path="/status">
            <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                  />
                  <Main toggle={toggle} menuFilters={menuFilters} />
            </Route>
            <Route path="/whitelists">
            <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                  />
            </Route>
            <Route path="/">
              <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                  />
                  <Main toggle={toggle} menuFilters={menuFilters} />
            </Route>
          </Switch>
        </Router>
    /*</ReactKeycloakProvider>*/
    );
}

export default App;
