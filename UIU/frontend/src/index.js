import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { CssBaseline } from '@material-ui/core';
import { CustomThemeProvider } from './components/theme/customThemeProvider';
import { ApiSocketProvider } from './components/api/apiSocket';


ReactDOM.render(
  <React.StrictMode>
    <ApiSocketProvider>
      <CustomThemeProvider>
        <CssBaseline />
        <App />
      </CustomThemeProvider>
    </ApiSocketProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
