const tasks = [
    { id: 1, description: "Fare la spesa", urgent: true, private_: true, deadline: "2021-04-19T09:20", completed: true },
    { id: 2, description: 'Dentista', urgent: true, private_: true, deadline: "2021-04-20T10:30", completed: false },
    { id: 3, description: 'Meccanico', urgent: false, private_: false, deadline: "2021-04-01T02:00", completed: true },
    { id: 4, description: 'Lezione', urgent: true, private_: false, deadline: "2021-03-29T15:10:00", completed: false }
];

const menuFilters = [
    { name: "All" },
    { name: "Important" },
    { name: "Today" },
    { name: "Next 7 Days" },
    { name: "Private" }
];

export {tasks, menuFilters};