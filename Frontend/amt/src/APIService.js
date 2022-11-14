const API_URL = "http://localhost:80";

export async function separate(file) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(API_URL + "/separate", {
        method: "POST",
        mode: "cors",
        body: formData,
    }).then(async (response) => await response.blob());
    return response;
}

export async function separate_by_youtube(url) {
    const response = await fetch(API_URL + "/separate-youtube", {
        method: "POST",
        mode: "cors",
        body: JSON.stringify({ url: url }),
        headers: {
            "Content-Type": "application/json",
        },
    }).then(async (response) => await response.blob());
    return response;
}
