const BASE = "http://localhost:8000/api";
const json = (r) => (r.ok ? r.json() : r.json().then((e) => Promise.reject(e.detail || "Request failed")));
const post = (path, body) =>
  fetch(BASE + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then(json);

export const api = {
  assessment: () => fetch(`${BASE}/assessment`).then(json),
  submit: (user, answers) => post("/assessment/submit", { user, answers }),
  upload: (user, file) => {
    const f = new FormData(); f.append("user", user); f.append("file", file);
    return fetch(`${BASE}/materials`, { method: "POST", body: f }).then(json);
  },
  quiz: (user, n = 5) => post("/quiz", { user, n }),
  saveQuiz: (user, score, total) => post("/quiz/score", { user, score, total }),
  progress: (user) => fetch(`${BASE}/progress/${user}`).then(json),
};
