import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [schoolData, setSchoolData] = useState(null);
  const urns = ["100001", "102257","102942","110158"];  // Add up to 4 URNs, replace with real ones

  useEffect(() => {
    axios.get(`http://localhost:8000/schools?urns=${urns.join(',')}`)
      .then(res => setSchoolData(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!schoolData) return <div className="text-center p-5">Loading...</div>;

  const chartData = {
    labels: Object.values(schoolData)[0].map(d => d.year),  // Use first school's years
    datasets: Object.entries(schoolData).map(([urn, data], index) => ({
      label: `School ${urn} Avg Grade`,
      data: data.map(d => d.avg_grade),
      borderColor: `hsl(${index * 90}, 70%, 50%)`,  // Unique colors for each school
      fill: false,
    })).concat(
      Object.entries(schoolData).map(([urn, data], index) => ({
        label: `School ${urn} STEM Grade`,
        data: data.map(d => d.stem),
        borderColor: `hsl(${index * 90 + 30}, 70%, 50%)`,
        fill: false,
      })).concat(
        Object.entries(schoolData).map(([urn, data], index) => ({
          label: `School ${urn} Arts Grade`,
          data: data.map(d => d.arts),
          borderColor: `hsl(${index * 90 + 60}, 70%, 50%)`,
          fill: false,
        }))
      )
    ),
  };

  return (
    <div className="p-5 max-w-4xl mx-auto">
      <h1 className="text-3xl text-blue-700 mb-5">KS5 Dashboard - Compare Schools</h1>
      <div className="bg-white p-5 rounded shadow">
        <Line data={chartData} options={{ 
          responsive: true, 
          scales: { y: { min: 0, max: 6 } },
          plugins: { legend: { position: 'top' } }
        }} />
      </div>
    </div>
  );
}

export default App;