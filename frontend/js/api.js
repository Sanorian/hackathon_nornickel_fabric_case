const API = "http://localhost:8000/projects";

async function getProjects() {
    const res = await fetch(API);
    return await res.json();
}

async function getProject(id) {
    const res = await fetch(`${API}/${id}`);
    return await res.json();
}

async function createProject(title) {
    const res = await fetch(`${API}/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title
        })
    });

    return await res.json();
}

async function uploadFiles(id, files) {
    const form = new FormData();

    for (const file of files)
        form.append("files", file);

    const res = await fetch(`${API}/${id}/files/add`, {
        method: "POST",
        body: form
    });

    return await res.json();
}

async function sendRequest(id, task, limitations) {
    const res = await fetch(`${API}/${id}/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            task,
            limitations
        })
    });

    return await res.json();
}