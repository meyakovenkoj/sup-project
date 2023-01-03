import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";
import authUser from './authUser';

const createRootReducer = (history) =>
  combineReducers({
    router: connectRouter(history),
    authUser
  });

export default createRootReducer;
