const initialState = {
  user: {},
  isAuth: false,
  lists: [],
  currentList: '',
  currentID: '',
  username: '',
  delReq: false, //delete request))
}

const reducer = (state = initialState, action) => {
  var new_lists

  console.log(state)
  console.log(action)
  switch (action.type) {
    case 'GET_LISTS':
      console.log(action.lists)
      return {
        ...state,
        lists: Array.isArray(action.lists) ? action.lists : [],
      }
    case 'ADD_LIST':
    case 'ADD_ITEM_FAST':
      console.log([action.new_list])
      return {
        ...state,
        lists: [...state.lists, ...[action.new_list]],
      }

    case 'ADD_GROUP':
      console.log([action.new_group])
      return {
        ...state,
        lists: [...state.lists, ...[action.new_group]],
      }

    case 'MARK_ITEM':
      new_lists = [...state.lists]
      new_lists[action.itemMark.index].bought = action.itemMark.mark
      return {
        ...state,
        lists: new_lists,
      }
    case 'LABEL_ITEM':
      new_lists = [...state.lists]
      new_lists[action.itemLabel.index].labels.push(action.itemLabel.label)
      console.log(new_lists)
      return {
        ...state,
        lists: new_lists,
      }
    case 'DELETE_LABEL_ITEM':
      new_lists = [...state.lists]
      new_lists[action.itemLabel.index].labels = new_lists[
        action.itemLabel.index
      ].labels.filter((label) => label.id !== action.itemLabel.label_id)

      console.log(new_lists)
      return {
        ...state,
        lists: new_lists,
      }
    case 'DELETE_LIST_REQ':
      return {
        ...state,
        delReq: true,
      }
    case 'DELETE_LIST':
      return {
        ...state,
        lists: state.lists.filter((item) => item.id !== action.list_id),
        delReq: false,
      }

    case 'DELETE_GROUP_REQ':
      return {
        ...state,
        delReq: true,
      }

    case 'DELETE_ITEM_REQ':
      return {
        ...state,
        itemDelReq: true,
      }
    case 'DELETE_ITEM':
      return {
        ...state,
        itemDelReq: false,
      }
    case 'DELETE_GROUP':
      return {
        ...state,
        lists: state.lists.filter((item) => item.id !== action.group_id),
        delReq: false,
      }

    case 'ADD_ITEM_LIST':
      return {
        ...state,
      }
    case 'ADD_ITEM':
      console.log('item added, what else do you want?')
      return {
        ...state,
      }
    case 'GET_ITEMS':
      return {
        ...state,
        items: action.items,
      }
    case 'SET_OPEN_LIST':
      return {
        ...state,
        lists: [],
        currentList: action.listInfo.name,
        currentID: action.listInfo.id,
      }
    case 'SET_USER':
      return {
        ...state,
        isAuth: true,
        username: action.username,
      }
    case 'SET_GOOGLE_AUTH':
      return {
        ...state,
        googleAuth: true,
        username: action.user.login,
        hasAccount: action.user.hasAccount,
      }
    case 'GET_AUTH': {
      return {
        ...state,
        res: action.rest,
      }
    }
    case 'DUMMY_EXPORT': {
      return {
        ...state,
      }
    }
    default:
      return state
  }
}

export default reducer
