import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import WebRoutes from './routes'
import { Provider } from 'react-redux'
import configureStore from './redux/store'
import { Layout } from 'antd';
const store = configureStore()

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={{ ...store }}>
   <Layout style={{ height: '100%' }}>
    <WebRoutes store={{ ...store }} />
   </Layout>
  </Provider>
  </React.StrictMode>
);