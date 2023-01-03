const initialState = {
    user: {},
    isAuth: false,
    profile: {},
    users: [],
    projects: [],
    current_project_id: '',
    current_task_id: '',
    current_user_id: ''
  };
  
  export default (state = initialState, action) => {
    // console.log(action)
    switch (action.type) {
    case 'LOGIN_STARTED':
      return {
        ...state,
        loading: true,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        loading: false,
        error: null,
        isAuth: true,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        loading: false,
        error: action.payload.error,
      };
    case 'SET_USER': {
      return {
        ...state,
        isAuth: Object.keys(action.user).length > 0,
        user: action.user,
      };
    }
    case 'SET_USERS': {
        return {
          ...state,
          users: action.users,
        };
      }
    case 'SET_PROJECTS':
      return {
        ...state,
        projects: action.projects,
      };
      case 'SET_TASKS':
        return {
          ...state,
          tasks: action.tasks,
        };
        case 'SET_SELECETED_TASK':
            return {
              ...state,
              sel_task: action.sel_task,
            };
    case 'LOGOUT':
      return {
        ...state,
        isAuth: false,
        user: action.user,
      };
      case 'SET_USER': {
        return {
          ...state,
          isAuth: Object.keys(action.user).length > 0 ? true : false,
          user: action.user,
        };
      }
      case 'FOLLOW_USER': {
        return {
          ...state,
          user: action.user,
        };
      }
      case 'UNFOLLOW_USER': {
        return {
          ...state,
          user: {},
        };
      }
      case 'SET_PROFILE':
        return {
          ...state,
          profile: action.profile,
        };
      case 'SET_FRIENDS':
        return {
          ...state,
          friends: action.friends,
        };
      case 'SET_PROFILES':
        return {
          ...state,
          profiles: action.profiles,
        };
      case 'LOGOUT':
        return {
          ...state,
          isAuth: false,
          profile: action.user,
          user: action.user,
        };
      default:
        return state;
    }
  };
  