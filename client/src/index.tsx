import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import {BrowserRouter} from 'react-router-dom';
import {App} from './app/App';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <App/>
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
);

serviceWorker.unregister();

