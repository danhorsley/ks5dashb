import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [schoolData, setSchoolData] = useState(null);
  const [urns, setUrns] = useState(["100001", "102257", "102942", "110158"]);  // Default, editable

  const handleUrnChange = (index, value) => {
    const newUrns = [...urns];
    newUrns[index] = value;
    setUrns(newUrns);
  };

  useEffect(() => {
    axios.get(`http://localhost:8000/schools?urns=${urns.join(',')}`)
      .then(res => setSchoolData(res.data))
      .catch(err => console.error(err));
  }, [urns]);

  if (!schoolData) return <div className="text-center p-5">Loading...</div>;

  const chartData = {
    labels: Object.values(schoolData)[0]?.map(d => d.year) || [],
    datasets: Object.entries(schoolData).flatMap(([urn, data], schoolIndex) => [
      {
        label: `School ${urn} Avg Grade`,
        data: data.map(d => d.avg_grade || 0),
        borderColor: `hsl(${schoolIndex * 90}, 70%, 50%)`,
        fill: false,
        tension: 0.1,
      },
      {
        label: `School ${urn} STEM Grade`,
        data: data.map(d => d.stem || 0),
        borderColor: `hsl(${schoolIndex * 90 + 30}, 70%, 50%)`,
        fill: false,
        tension: 0.1,
      },
      {
        label: `School ${urn} Arts Grade`,
        data: data.map(d => d.arts || 0),
        borderColor: `hsl(${schoolIndex * 90 + 60}, 70%, 50%)`,
        fill: false,
        tension: 0.1,
      },
      {
        label: `School ${urn} Econ Grade`,
        data: data.map(d => d.econ || 0),
        borderColor: `hsl(${schoolIndex * 90 + 90}, 70%, 50%)`,  // New color for Business & Economics
        fill: false,
        tension: 0.1,
      },
    ]),
  };

  return (
    <div className="p-5 max-w-4xl mx-auto">
      <h1 className="text-3xl text-blue-700 mb-5">KS5 Dashboard - Compare Schools</h1>
      <div className="mb-5">
        {urns.map((urn, index) => (
          <input
            key={index}
            type="text"
            value={urn}
            onChange={(e) => handleUrnChange(index, e.target.value)}
            placeholder={`School URN ${index + 1}`}
            className="border p-2 mr-2 rounded"
          />
        ))}
      </div>
      <div className="bg-white p-5 rounded shadow">
        <Line data={chartData} options={{ 
          responsive: true, 
          scales: { 
            y: { 
              min: 0, 
              max: 6, 
              ticks: { stepSize: 0.5 }  // Fine increments for floats
            }
          },
          plugins: { legend: { position: 'top' } }
        }} />
      </div>
    </div>
  );
}

export default App;