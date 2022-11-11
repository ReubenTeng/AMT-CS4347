const API_URL = "http://localhost:80";

export async function getDefaultMidi() {
    const response = await fetch(API_URL + "/default-midi", {
        method: "GET",
    });
    return await response.json();
}

export async function separate(file) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(API_URL + "/separate", {
        method: "POST",
        body: formData,
    });
    return await response.json();
}

export async function separate_by_youtube(url) {
    console.log(url);
    const response = await fetch(API_URL + "/separate-youtube", {
        method: "POST",
        body: JSON.stringify({ url: url }),
        headers: {
            "Content-Type": "application/json",
        },
    });
    return await response.json();
}
