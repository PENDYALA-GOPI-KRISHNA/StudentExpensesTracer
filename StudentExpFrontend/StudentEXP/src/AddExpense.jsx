import { useState } from "react";
import "./AddExpense.css"
const API_URL = "http://127.0.0.1:5000";

function AddExpense({ studentId }) {
  const [date, setDate] = useState("");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");
  const [expenses, setExpenses] = useState([]);
  const [showExpenses, setShowExpenses] = useState(false);

  const fetchExpenses = async () => {
    const res = await fetch(`${API_URL}/expenses/${studentId}`);
    const data = await res.json();
    setExpenses(data);
    setShowExpenses(true);
  };

  const saveExpense = async () => {
    await fetch(`${API_URL}/add-expense`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: studentId,
        date,
        amount,
        category,
        description,
      }),
    });

    alert("Expense saved successfully");

    setDate("");
    setAmount("");
    setCategory("");
    setDescription("");

    if (showExpenses) {
      fetchExpenses();
    }
  };
  return (
    <div className="expense-container">
      <h2 className="expense-heading">Add Expense</h2>

      <input
        className="expense-input"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />

      <input
        className="expense-input"
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      <input
        className="expense-input"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />

      <input
        className="expense-input"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <button className="expense-button" onClick={saveExpense}>
        Save
      </button>

      <button className="expense-button secondary" onClick={fetchExpenses}>
        Show My Expenses
      </button>

      {showExpenses && (
        <div className="expense-table-container">
          <h3 className="expense-heading">All Expenses</h3>
          {expenses.length === 0 ? (
            <p>No expenses found.</p>
          ) : (
            <table className="expense-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Amount</th>
                  <th>Category</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {expenses.map((exp) => (
                  <tr key={exp.expense_id}>
                    <td>{exp.expenses_date}</td>
                    <td>{exp.amount}</td>
                    <td>{exp.category}</td>
                    <td>{exp.discription}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default AddExpense;
