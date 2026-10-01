import { useEffect, useState } from "react";
import { api } from "./api";
import "./styles.css";

const USER = "demo"; // exercise: replace with real login + role-based access
const STEPS = ["Assess", "Identify gaps", "Learning path", "Test", "Improve"];
const LEVEL = { strong: ["Strong", "var(--good)"], developing: ["Developing", "var(--saf)"], gap: ["Gap", "var(--bad)"] };

export default function App() {
  const [step, setStep] = useState(0);
  const [result, setResult] = useState(null);
  const [mcqs, setMcqs] = useState([]);
  const [quizId, setQuizId] = useState(0);

  useEffect(() => { window.scrollTo(0, 0); }, [step]);
  const newQuiz = (q) => { setMcqs(q); setQuizId((n) => n + 1); setStep(3); };
  const locked = [false, !result, !result, !mcqs.length, false];
  return (
    <div className="app">
      <aside>
        <h1>AIMinds</h1>
        <p>Competency learning for India's Official Statistical System</p>
        <ol className="steps">
          {STEPS.map((s, i) => (
            <li key={s}><button className={i === step ? "on" : ""} onClick={() => setStep(i)}>{s}</button></li>
          ))}
        </ol>
      </aside>
      <main aria-live="polite">
        {step === 0 && <Assess onDone={(r) => { setResult(r); setStep(1); }} />}
        {step === 1 && <Gaps result={result} go={setStep} />}
        {step === 2 && <Path result={result} go={setStep} onQuiz={newQuiz} />}
        {step === 3 && <Test key={quizId} mcqs={mcqs} go={setStep} onNew={() => api.quiz(USER).then(newQuiz)} />}
        {step === 4 && <Improve result={result} go={setStep} />}
      </main>
    </div>
  );
}

function Need({ go }) {
  return (<>
    <h2>Take the assessment first</h2>
    <p className="lead">We need your results to find gaps and recommend training.</p>
    <button className="btn" onClick={() => go(0)}>Start assessment</button>
  </>);
}

function Assess({ onDone }) {
  const [comps, setComps] = useState([]);
  const [ans, setAns] = useState({});
  useEffect(() => { api.assessment().then(setComps); }, []);

  const send = async () => {
    const answers = {};
    comps.forEach((c) => { answers[c.id] = c.questions.map((_, i) => ans[`${c.id}-${i}`] ?? -1); });
    onDone(await api.submit(USER, answers));
  };

  return (<>
    <h2>Competency assessment</h2>
    <p className="lead">Answer these {comps.length * 2} questions. Your results show where your skills are strong and where training will help most.</p>
    {comps.map((c) => c.questions.map((q, i) => (
      <div className="card q" key={`${c.id}-${i}`}>
        <div className="c">{c.name}</div><p>{q.q}</p>
        {q.options.map((o, j) => (
          <label key={j}><input type="radio" name={`${c.id}-${i}`} onChange={() => setAns({ ...ans, [`${c.id}-${i}`]: j })} />{o}</label>
        ))}
      </div>
    )))}
    <button className="btn" onClick={send}>See my competency gaps</button>
  </>);
}

function Gaps({ result, go }) {
  if (!result) return <Need go={go} />;
  const gl = result.report.filter((r) => r.level !== "strong");
  return (<>
    <h2>Your competency profile</h2>
    <p className="lead">The line on each bar marks the target level. {gl.length
      ? <>Priority areas: <b>{gl.map((r) => r.name).join(", ")}</b>.</> : "No gaps found. Great work."}</p>
    <div className="card">
      {result.report.map((r) => {
        const [label, col] = LEVEL[r.level];
        return (
          <div className="row" key={r.id}>
            <span>{r.name}</span>
            <div className="bar"><i style={{ width: `${(r.correct / r.total) * 100}%`, background: col }} /><b style={{ left: "100%" }} /></div>
            <span className="tag" style={{ color: col }}>{label}</span>
          </div>
        );
      })}
    </div>
    <button className="btn" onClick={() => go(2)}>Get my learning path</button>
  </>);
}

function Path({ result, go, onQuiz }) {
  const [note, setNote] = useState("");
  if (!result) return <Need go={go} />;

  const upload = async (e) => {
    try { const r = await api.upload(USER, e.target.files[0]); setNote(`Indexed ${r.chunks_indexed} chunks. Ready to generate a quiz.`); }
    catch (err) { setNote(String(err)); }
  };
  const generate = async () => {
    setNote("Generating questions…");
    try { onQuiz(await api.quiz(USER)); } catch (err) { setNote(String(err)); }
  };

  return (<>
    <h2>Personalised learning path</h2>
    <p className="lead">Courses are ordered by gap size. The catalogue below is sample data; the production version pulls courses from iGOT Karmayogi through its APIs.</p>
    {result.learning_path.length ? result.learning_path.map((p) => (
      <div className="card" key={p.competency}>
        <h3>{p.competency}</h3>
        {p.courses.map((c) => (<div className="course" key={c}><span>{c}</span><span className="tag">iGOT course (sample)</span></div>))}
      </div>
    )) : <div className="card">You are at target level in every area. Try the quiz generator to keep practising.</div>}
    <div className="card">
      <h3>Learn from your own material</h3>
      <p className="note">Upload a PDF or .txt file. The platform indexes it and turns it into MCQs.</p>
      <input type="file" accept=".pdf,.txt" onChange={upload} />
      <p className="note">{note}</p>
    </div>
    <button className="btn" onClick={generate}>Generate quiz from this material</button>
  </>);
}

function Test({ mcqs, go, onNew }) {
  const [pick, setPick] = useState({});
  const [checked, setChecked] = useState(false);
  if (!mcqs.length) return (<>
    <h2>Test yourself</h2>
    <p className="lead">Generate questions from your learning material first.</p>
    <button className="btn" onClick={() => go(2)}>Add learning material</button>
  </>);

  const score = mcqs.filter((m, i) => pick[i] === m.answer).length;
  const check = async () => { setChecked(true); await api.saveQuiz(USER, score, mcqs.length); };

  return (<>
    <h2>Auto-generated quiz</h2>
    <p className="lead">Choose the best answer for each question. A human reviewer should check generated questions before formal use.</p>
    {mcqs.map((m, i) => (
      <div className="card q" key={i}>
        <p>{i + 1}. {m.q}</p>
        {m.options.map((o, j) => (
          <label key={j}><input type="radio" name={`m${i}`} onChange={() => setPick({ ...pick, [i]: j })} />{o}</label>
        ))}
        {checked && (pick[i] === m.answer
          ? <div><span className="ok">✓ Correct</span> {m.explanation}</div>
          : <div><span className="no">✗ Incorrect.</span> Answer: <b>{m.options[m.answer]}</b>. {m.explanation}</div>)}
      </div>
    ))}
    {checked && <p><b>Score: {score}/{mcqs.length}.</b> <a href="#" onClick={(e) => { e.preventDefault(); go(4); }}>See progress</a></p>}
    <button className="btn" onClick={check} disabled={checked}>Check answers</button>{" "}
    <button className="btn alt" onClick={onNew}>New questions</button>
  </>);
}

function Improve({ result, go }) {
  const [rows, setRows] = useState([]);
  useEffect(() => { api.progress(USER).then(setRows); }, []);
  const hasGaps = result && result.report.some((r) => r.level !== "strong");
  return (<>
    <h2>Progress and feedback</h2>
    <p className="lead">Each assessment and quiz is recorded so you can see growth over time.</p>
    <div className="card">
      {rows.length ? (
        <table className="hist"><tbody>
          <tr><th>Date</th><th>Activity</th><th>Score</th><th>%</th></tr>
          {rows.map((r, i) => (
            <tr key={i}><td>{r.date}</td><td style={{ textTransform: "capitalize" }}>{r.kind}</td><td>{r.score}/{r.total}</td><td>{Math.round((r.score / r.total) * 100)}%</td></tr>
          ))}
        </tbody></table>
      ) : <p>No activity yet. Start with the assessment.</p>}
    </div>
    {result && <div className="card"><h3>Next step</h3><p>{hasGaps
      ? "Finish the recommended courses, then retake the assessment to confirm your gaps have closed."
      : "Keep practising with quizzes built from new material."}</p></div>}
    <button className="btn" onClick={() => go(0)}>Retake assessment</button>
  </>);
}
