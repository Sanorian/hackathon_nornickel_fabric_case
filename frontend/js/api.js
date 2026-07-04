const API = "/api/projects";

async function getProjects() {
    const res = await fetch('/api/projects/');

    const text = await res.text();

    console.log(res.status);
    console.log(text);

    if (!res.ok) {
        throw new Error(text);
    }

    return JSON.parse(text);
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