db = connect("mongodb://v1517237.hosted-by-vdsina.ru:27017/sup_data");


db.User.insertMany([
    {
        name:"Админ",
        surname: "Админов",
        username: "admin",
        password_hash: "",
        projects: [],
        is_admin: true
    },
    {
        name:"Руководитель",
        surname: "Руководителев",
        username: "headmaster",
        password_hash: "",
        projects: [],
        is_admin: false
    },
    {
        name:"Работник",
        surname: "Работников",
        username: "employee",
        password_hash: "",
        projects: [],
        is_admin: false
    }
]);


db.Project.insertMany([
    {
        title:"SUP1",
        head: null,
        created: "2022-12-02",
        participants: [],
        tasks: [],
        status: "open"
    },
    {
        title:"SUP2",
        head: null,
        created: "2022-12-02",
        participants: [],
        tasks: [],
        status: "open"
    },
    {
        title:"SUP3",
        head: null,
        created: "2022-12-02",
        participants: [],
        tasks: [],
        status: "open"
    }
]);
