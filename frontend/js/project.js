const params = new URLSearchParams(window.location.search);
const projectId = params.get("id");

async function loadProject() {
    const project = await getProject(projectId);
    document.getElementById("title").textContent =
        project.title;
    const files = document.getElementById("file-list");
    files.innerHTML = "";

    for (const file of project.files) {
        files.innerHTML += `
            <div>${file.title}</div>
        `;
    }

    const requests = document.getElementById("requests");
    requests.innerHTML = "";

    if (project.requests) {
        for (const req of project.requests) {
            requests.innerHTML += `
            <div class="request">
                <h3>${req.task}</h3>
                <b>Ограничения</b>
                <p>${req.limitations}</p>
                <b>Ответ</b>
                <p>${req.response}</p>
            </div>
            `;
        }
    }
}

document
.getElementById("upload")
.onclick = async () => {
    const files =
        document.getElementById("files").files;
    await uploadFiles(projectId, files);
    loadProject();
};

document
.getElementById("send")
.onclick = async () => {
    const task =
        document.getElementById("task").value;
    const limitations =
        document.getElementById("limitations").value;
    await sendRequest(
        projectId,
        task,
        limitations
    );

    document.getElementById("task").value = "";
    document.getElementById("limitations").value = "";
    loadProject();
};

loadProject();