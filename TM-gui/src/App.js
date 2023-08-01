import "bootstrap/dist/css/bootstrap.min.css";
import "./css/style.css";
import { Header, Main, InitialSpinner } from "./Components";
import { useState, React, useEffect } from "react";
import { menuFilters } from "./DataBase";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
//import Keycloak from 'keycloak-js';
//import { ReactKeycloakProvider } from "@react-keycloak/web";
import API from "./API";

function App() {
  const [toggle, setToggle] = useState(false);
  //const [keycloak, setKeycloak] = useState(null)
  const [tokenCheck, setTokenCheck] = useState(true);
  const [error, setError] = useState("");
  //const [authenticated, setAuthenticated] = useState(false);
  //const [token, setToken] = useState();
  const [username, setUsername] = useState();
  
  const params = new URLSearchParams(window.location.search);
  const session = params.get('session');
  console.log(session);
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

  //useEffect(() => {

    /*const checkToken = async (token) => {
      //try{
        const resp = await API.verifyToken(token);
        if(resp.error){
          setError(resp.error_description);
          setTokenCheck(false);
          setAuthenticated(false);
        }
        else{
          setAuthenticated(true);
          setTokenCheck(false);
        }
      //}
      //catch(err){
        //setError(err);
        //setTokenCheck(false);
        //setAuthenticated(false);
      //}
    };*/

    //const params = new URLSearchParams(window.location.search);
    //token = params.get('token');
    //console.log(token);
    //setToken(tmp);

    /*if(tokenCheck){
      checkToken(token);
    }*/

  //}, [/*tokenCheck,*/ token]);

  const hideShow = () => {
    setToggle((toggle) => !toggle);
  };

  return (
    /*<ReactKeycloakProvider authClient={keycloak}>*/
    <>
    {/*tokenCheck*/ false ? <InitialSpinner/> : ( /*authenticated*/ true ?
        <Router>
          <Switch>
          <Route path="/entities">
              <Redirect to={`/?session=${session}`}/>
            </Route>
            <Route path="/verifiers">
            <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                    username={username}
                  />
                  <Main toggle={toggle} menuFilters={menuFilters} session={session} username={username} setUsername={setUsername}/>
            </Route>
            <Route path="/status">
            <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                    username={username}
                  />
                  <Main toggle={toggle} menuFilters={menuFilters} session={session} username={username} setUsername={setUsername}/>
            </Route>
            <Route path="/whitelists">
            <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                    username={username}
                  />
            </Route>
            <Route path="/">
              <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                    username={username}
                  />
                  <Main toggle={toggle} menuFilters={menuFilters} session={session} username={username} setUsername={setUsername}/>
            </Route>
          </Switch>
        </Router>
        :
        <p>{error}</p>
      )
    }
    </>
    /*</ReactKeycloakProvider>*/
    );
}

export default App;
