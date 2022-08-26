export async function hit_api(url: string, method: string, body: any): Promise<any> {
    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });
    const data = await response.json();
    return { data: data, status: response.status };
}