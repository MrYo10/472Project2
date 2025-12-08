const BASE_URL = "http://127.0.0.1:8000";

export async function createRequest(data) {
    const res = await fetch(`${BASE_URL}/request`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    return res.json();
}

export async function runScheduler(alg) {
    const res = await fetch(`${BASE_URL}/schedule/${alg}`, {
        method: "POST"
    });
    return res.json();
}

export async function getResources() {
    const res = await fetch(`${BASE_URL}/resources`);
    return res.json();
}