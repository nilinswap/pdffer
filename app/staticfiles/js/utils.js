export async function hit_api(url, method, body) {
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

const getCookieValue = (name) =>
  document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || "";

export async function is_authenticated() {
  const session_id_val = getCookieValue("session_id");
  if (
    session_id_val != null &&
    session_id_val != "" &&
    session_id_val != undefined
  ) {
    const response = await fetch("/auth/verify_session/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: session_id_val,
      }),
    });
    const data = await response.json();
    if (data.success) {
      return true;
    }
  }
  return false;
}
