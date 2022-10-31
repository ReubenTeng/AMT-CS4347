export async function getDefaultMidi() {
    const response = await fetch(`http://localhost/default-midi`, {
        method: "GET",
    });
    return await response.json();
}
