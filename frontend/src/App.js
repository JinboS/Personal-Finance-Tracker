import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [records, setRecords] = useState([]);
  const [form, setForm] = useState({
    date: '',
    category: 'expense',
    description: '',
    amount: ''
  });

  // Retrieve all records
  const fetchRecords = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/records');
      setRecords(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  // Add record
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/records', form);
      setForm({ date: '', category: 'expense', description: '', amount: '' });
      fetchRecords();
    } catch (error) {
      console.error(error);
    }
  };

  // Calculate total income and expense
  const incomeTotal = records.filter(r => r.category === 'income').reduce((acc, r) => acc + r.amount, 0);
  const expenseTotal = records.filter(r => r.category === 'expense').reduce((acc, r) => acc + r.amount, 0);

  const chartData = {
    labels: ['Income', 'Expense'],
    datasets: [{
      label: 'Total Amount',
      data: [incomeTotal, expenseTotal],
      backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)']
    }]
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Personal Finance Tracker</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input 
          type="date" 
          value={form.date} 
          onChange={e => setForm({...form, date: e.target.value})}
          required
        />
        <select 
          value={form.category} 
          onChange={e => setForm({...form, category: e.target.value})}
          style={{ marginLeft: '10px' }}
        >
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
        <input 
          type="text" 
          placeholder="Description" 
          value={form.description} 
          onChange={e => setForm({...form, description: e.target.value})}
          style={{ marginLeft: '10px' }}
        />
        <input 
          type="number" 
          placeholder="Amount" 
          value={form.amount} 
          onChange={e => setForm({...form, amount: parseFloat(e.target.value) || 0})}
          required
          style={{ marginLeft: '10px', width: '100px' }}
        />
        <button type="submit" style={{ marginLeft: '10px' }}>Add Record</button>
      </form>

      <h2>Records</h2>
      <table border="1" cellPadding="5" style={{ width: '100%', marginBottom: '20px' }}>
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Description</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {records.map(record => (
            <tr key={record.id}>
              <td>{record.date}</td>
              <td>{record.category}</td>
              <td>{record.description}</td>
              <td>{record.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Summary Chart</h2>
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <Bar data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
      </div>
    </div>
  );
}

export default App;  

