const list = document.getElementById("projects");

async function loadProjects() {
    const projects = await getProjects();
    list.innerHTML = "";

    for (const project of projects) {
        const div = document.createElement("div");
        div.className = "project";
        div.innerHTML = `
            <a href="project.html?id=${project.id}">
                ${project.title}
            </a>
        `;
        list.appendChild(div);
    }
}

document
.getElementById("create")
.onclick = async () => {

    const title = document.getElementById("title").value;
    if (!title)
        return;
    await createProject(title);
    document.getElementById("title").value = "";
    loadProjects();
};

loadProjects();