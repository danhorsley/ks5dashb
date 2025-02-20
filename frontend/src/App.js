import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [schoolData, setSchoolData] = useState(null);
  const urn = "100001";  // Replace with a real URN from your data

  useEffect(() => {
    axios.get(`http://localhost:8000/schools/${urn}`)
      .then(res => setSchoolData(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!schoolData) return <div className="text-center p-5">Loading...</div>;

  const chartData = {
    labels: schoolData.data.map(d => d.year),
    datasets: [
      { label: 'Avg Grade', data: schoolData.data.map(d => d.avg_grade), borderColor: 'blue', fill: false },
      { label: 'STEM Grade', data: schoolData.data.map(d => d.stem), borderColor: 'green', fill: false },
      { label: 'Arts Grade', data: schoolData.data.map(d => d.arts), borderColor: 'red', fill: false },
    ],
  };

  return (
    <div className="p-5 max-w-4xl mx-auto">
      <h1 className="text-3xl text-blue-700 mb-5">KS5 Dashboard - School {schoolData.school}</h1>
      <div className="bg-white p-5 rounded shadow">
        <Line data={chartData} options={{ responsive: true, scales: { y: { min: 0, max: 6 } } }} />
      </div>
    </div>
  );
}

export default App;
