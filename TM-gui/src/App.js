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
import API from "./API";

function App() {
  const [toggle, setToggle] = useState(false);

  const hideShow = () => {
    setToggle((toggle) => !toggle);
  };

  return (
    <>
        <Router>
          <Switch>
            <Route path="/">
              <Header
                    toggleFunc={hideShow}
                    title="Trust Monitor GUI"
                  />
                  <Main toggle={toggle} menuFilters={menuFilters} />
            </Route>
          </Switch>
        </Router>
    </>
  );
}

export default App;
