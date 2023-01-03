import axios from 'axios';

// const url = 'https://v1517237.hosted-by-vdsina.ru';
const url = 'http://localhost:8080';

export function RegisterUser(userData) {
    return (dispatch) => {
      axios
        .post(
          url+'/_xhr/register',
          {
            username: userData.user.username,
            password: userData.user.password,
            name: userData.user.name,
            surname: userData.user.surname,
          },
          {withCredentials: true}
        )
        .then((res) => {
          const user = res.data
          alert(res)
        })
        .catch((err) => {
          alert(err.response.data.message)
        })
    }
  }

export function LoginUser(userData) {
  return (dispatch) => {
    axios
      .post(
        url+'/_xhr/login',
        {
          username: userData.user.username,
          password: userData.user.password,
        },
        {withCredentials: true}
      )
      .then((res) => {
        sessionStorage.setItem('Auth', 'true');

      })
      .catch((err) => {
        alert(err.response.data.message);
      });
  };
}

export function GetMe() {
    return (dispatch) => {
      axios
        .get(
          url+'/me',
          {withCredentials: true}
        )
        .then((res) => {
          const user = res.data.data.user;
          dispatch({type: 'SET_USER', user});
  
        })
        .catch((err) => {
          alert(err.response.data.message);
        });
    };
  }

export function Logout() {
    return (dispatch) => {
      axios
        .post(
          url+'/_xhr/logout',
          {},
          {withCredentials: true}
        )
        .then(() => {
          const user = {};
          sessionStorage.removeItem('Auth');
          dispatch({type: 'LOGOUT', user});
        })
        .catch((err) => {
          alert(err);
        });
    };
  }
  export function searchUser(username) {
    return (dispatch) => {
      axios
        .get(
          url+'/_xhr/users',
          {params: {username_match:username}, withCredentials: true}
        )
        .then((res) => {
          const usrs = res.data.data.users;
          var users = [];
            usrs.forEach(item => {
            var elem = {...item, key:item.id, label:item.username};
            users.push(elem);
            });
          dispatch({type: 'SET_USERS', users});

        })
        .catch((err) => {
          alert(err);
        });
    };
  }


  export function getUser(id) {
    return (dispatch) => {
      axios
        .get(
          url+'/_xhr/users/'+id,
          {withCredentials: true}
        )
        .then((res) => {
          const user = {};
          sessionStorage.removeItem('Auth');
          dispatch({type: 'LOGOUT', user});
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function getUsers() {
    return (dispatch) => {
      axios
        .get(
          url+'/users',
          {withCredentials: true}
        )
        .then((res) => {
          const usrs = res.data.data.users;
          var users = [];
            usrs.forEach(item => {
            var elem = {...item, key:item.id, label:item.username};
            users.push(elem);
            });
          dispatch({type: 'SET_USERS', users});

        })
        .catch((err) => {
          alert(err);
        });
    };
  }

export function getProjects() {
    return (dispatch) => {
      axios
        .get(url+'/projects', {withCredentials: true})
        .then((res) => {
          const projs = res.data.data.projects;
          var projects = [];
          projs.forEach(item => {
          var elem = {...item, key:item.id, label:item.title};
          projects.push(elem);
          });
          dispatch({ type: 'SET_PROJECTS', projects })
        })
        .catch((err) => {
          // alert(err);
          alert(err.response.data.message)
        })
    }
  }


  export function searchProject(title) {
    return (dispatch) => {
      axios
        .get(url+'/_xhr/projects', {params: {title_match:title}, withCredentials: true})
        .then((res) => {
          const projs = res.data.data.projects;
          var projects = [];
          projs.forEach(item => {
          var elem = {...item, key:item.id, label:item.title};
          projects.push(elem);
          });
          dispatch({ type: 'SET_PROJECTS', projects })
        })
        .catch((err) => {
          // alert(err);
          alert(err.response.data.message)
        })
    }
  }

  
  export function addHeadUser(user_id, project_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/project/head',
        {
            "user_id": user_id,
            "project_id": project_id
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function addUser(user_id, project_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/project/participant',
        {
            "user_id": user_id,
            "project_id": project_id
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function changeStatus(status, project_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/projects/'+project_id+'/'+status,
        {
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }


  export function createProject(title) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/project',
        {
            "title":title,
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function searchTask(title) {
    return (dispatch) => {
      axios
      .get(
        url+'/_xhr/tasks',
        {params: {title_match:title}, withCredentials: true}
      )
        .then((res) => {
            const tsks = res.data.data.tasks;
            var tasks = [];
            tsks.forEach(item => {
            var elem = {...item, key:item.id, label:item.title};
            tasks.push(elem);
            });
            dispatch({ type: 'SET_TASKS', tasks })
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function getTasks() {
    return (dispatch) => {
      axios
      .get(
        url+'/tasks',
        {withCredentials: true}
      )
        .then((res) => {
            const tsks = res.data.data.tasks;
            var tasks = [];
            tsks.forEach(item => {
            var elem = {...item, key:item.id, label:item.title};
            tasks.push(elem);
            });
            dispatch({ type: 'SET_TASKS', tasks })
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function createTask(title, description, type, project_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/tasks',
        {
            "title":title,
            "description":description,
            "task_type":type,
            "project_id":project_id
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function addFileToTask(task_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/tasks/'+task_id + '/attach',
        {

        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function deleteFileToTask(task_id, file) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/tasks/'+task_id + '/delete_files',
        {
            "files":[
                file
            ]
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

//   export function getFileFromTask(task_id, project_id, filename) {
//     return (dispatch) => {
//       axios
//       .get(
//         url+'/attachments/'+ project_id +'/'+task_id+'/'+filename,
//         {
//         },
//       )
//         .then((res) => {
//             alert(res);
//         })
//         .catch((err) => {
//           alert(err);
//         });
//     };
//   }

  export function subscribe(task_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/tasks/'+task_id + '/subscribe',
        {
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function unsubscribe(task_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/tasks/'+task_id + '/unsubscribe',
        {
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function addComment(task_id, text) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/tasks/'+task_id + '/comment',
        {
            text: text
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function editComment(comment_id, text) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/comment/'+comment_id + '/edit',
        {
            text: text
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }

  export function deleteComment(comment_id) {
    return (dispatch) => {
      axios
      .post(
        url+'/_xhr/comment/'+comment_id + '/delete',
        {
        },
        {withCredentials: true}
      )
        .then((res) => {
            alert(res);
        })
        .catch((err) => {
          alert(err);
        });
    };
  }
