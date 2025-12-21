import { useState } from "react";
import Signup from "./Signup";
import Login from "./Login";
import AddExpense from "./AddExpense";

function App() {
  const [studentId, setStudentId] = useState(null);
  const [showSignup, setShowSignup] = useState(false);

  return (
  <div className="app-container">
    <h1>Student Expense Tracker</h1>

    {!studentId ? (
      <div className="auth-container">
        {showSignup ? (
          <Signup onSignupSuccess={() => setShowSignup(false)} />
        ) : (
          <Login onLogin={setStudentId} />
        )}

        <button
          className="toggle-auth-btn"
          onClick={() => setShowSignup(!showSignup)}
        >
          {showSignup ? "Go to Login" : "Go to Signup"}
        </button>
      </div>
    ) : (
      <AddExpense studentId={studentId} />
    )}
  </div>
);

}

export default App;
