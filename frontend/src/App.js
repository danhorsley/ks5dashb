import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  // Move useState calls to the top
  const [schoolData, setSchoolData] = useState(null);
  const [nationalData, setNationalData] = useState(null);
  const [regionalData, setRegionalData] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [selectedUrn, setSelectedUrn] = useState("100001");
  const region = "City of London";  // Hardcode School 100001’s region (confirm)

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    if (e.target.value.length > 2) {
      axios.get(`http://localhost:8000/schools/search?q=${e.target.value}`)
        .then(res => setSearchResults(res.data))
        .catch(err => console.error(err));
    } else {
      setSearchResults([]);
    }
  };

  const handleSelectSchool = (urn) => {
    setSelectedUrn(urn);
    setSearchQuery("");
    setSearchResults([]);
  };

  useEffect(() => {
    Promise.all([
      axios.get(`http://localhost:8000/schools/${selectedUrn}`),
      axios.get(`http://localhost:8000/national-averages`),
      axios.get(`http://localhost:8000/regional-averages/${encodeURIComponent(region)}`)
    ]).then(([schoolRes, nationalRes, regionalRes]) => {
      setSchoolData(schoolRes.data.data);
      setNationalData(nationalRes.data.data);
      setRegionalData(regionalRes.data.data);
    }).catch(err => console.error(err));
  }, [selectedUrn]);

  if (!schoolData || !nationalData || !regionalData) return <div className="text-center p-5">Loading...</div>;

  const createChartData = (metric) => ({
    labels: schoolData.map(d => d.year),
    datasets: [
      { label: `School ${selectedUrn} ${metric}`, data: schoolData.map(d => d[metric] || 0), borderColor: 'blue', fill: false, tension: 0.1 },
      { label: `National ${metric}`, data: nationalData.map(d => d[metric] || 0), borderColor: 'gray', fill: false, tension: 0.1 },
      { label: `Regional ${metric}`, data: regionalData.map(d => d[metric] || 0), borderColor: 'green', fill: false, tension: 0.1 },
    ],
  });

  const latestYear = 2024;
  const school = schoolData.find(d => d.year === latestYear) || {};
  const national = nationalData.find(d => d.year === latestYear) || {};
  const getSpread = (schoolValue, nationalValue) => (schoolValue - nationalValue).toFixed(2);

  const tableData = [
    { category: "Total", avg: school.avg_grade, spread: getSpread(school.avg_grade, national.avg_grade), trend: "—" },
    { category: "STEM", avg: school.stem, spread: getSpread(school.stem, national.stem), trend: "—" },
    { category: "Arts", avg: school.arts, spread: getSpread(school.arts, national.arts), trend: "—" },
    { category: "Humanities", avg: school.humanities, spread: getSpread(school.humanities, national.humanities), trend: "—" },
    { category: "Business & Economics", avg: school.econ, spread: getSpread(school.econ, national.econ), trend: "—" },
  ];

  return (
    <div className="p-5 max-w-4xl mx-auto">
      <h1 className="text-3xl text-blue-700 mb-5">KS5 Dashboard - School {selectedUrn}</h1>
      <div className="mb-5">
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearch}
          placeholder="Search by school name or URN"
          className="border p-2 rounded w-full"
        />
        {searchResults.length > 0 && (
          <ul className="border mt-2 rounded shadow">
            {searchResults.map(result => (
              <li key={result.urn} onClick={() => handleSelectSchool(result.urn)} className="p-2 hover:bg-gray-100 cursor-pointer">
                {result.name} (URN: {result.urn}, LA: {result.la}, Type: {result.type})
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="space-y-8 md:space-y-0 md:space-x-4 md:flex md:flex-col md:items-center">
        <div className="bg-white p-5 rounded shadow">
          <h2 className="text-xl text-gray-800 mb-2">Total Avg Grade</h2>
          <Line data={createChartData('avg_grade')} options={{ responsive: true, scales: { y: { min: 0, max: 6, ticks: { stepSize: 0.5 } } }, plugins: { legend: { position: 'top' } } }} />
        </div>
        <div className="bg-white p-5 rounded shadow">
          <h2 className="text-xl text-gray-800 mb-2">STEM Avg Grade</h2>
          <Line data={createChartData('stem')} options={{ responsive: true, scales: { y: { min: 0, max: 6, ticks: { stepSize: 0.5 } } }, plugins: { legend: { position: 'top' } } }} />
        </div>
        <div className="bg-white p-5 rounded shadow">
          <h2 className="text-xl text-gray-800 mb-2">Arts & Humanities Avg Grade</h2>
          <Line data={createChartData('arts')} options={{ responsive: true, scales: { y: { min: 0, max: 6, ticks: { stepSize: 0.5 } } }, plugins: { legend: { position: 'top' } } }} />
        </div>
        <div className="bg-white p-5 rounded shadow">
          <h2 className="text-xl text-gray-800 mb-2">Business & Economics Avg Grade</h2>
          <Line data={createChartData('econ')} options={{ responsive: true, scales: { y: { min: 0, max: 6, ticks: { stepSize: 0.5 } } }, plugins: { legend: { position: 'top' } } }} />
        </div>
      </div>
      <div className="mt-8">
        <h2 className="text-xl text-gray-800 mb-2">School Information</h2>
        <table className="w-full bg-white border rounded shadow">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 border">Metric</th>
              <th className="p-2 border">Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="p-2 border">School Name</td>
              <td className="p-2 border">{schoolData[0]?.school || "N/A"}</td>
            </tr>
            <tr>
              <td className="p-2 border">Local Authority</td>
              <td className="p-2 border">{schoolData[0]?.la || "N/A"}</td>
            </tr>
            <tr>
              <td className="p-2 border">Type of School</td>
              <td className="p-2 border">{schoolData[0]?.type || "N/A"}</td>
            </tr>
            <tr>
              <td className="p-2 border">Num Students</td>
              <td className="p-2 border">{school.cohort || "N/A"}</td>
            </tr>
            <tr>
              <td className="p-2 border">Min Age</td>
              <td className="p-2 border">{schoolData[0]?.min_age || "N/A"}</td>
            </tr>
            <tr>
              <td className="p-2 border">Max Age</td>
              <td className="p-2 border">{schoolData[0]?.max_age || "N/A"}</td>
            </tr>
            <tr>
              <td className="p-2 border">Num Staff</td>
              <td className="p-2 border">N/A</td>
            </tr>
            <tr>
              <td className="p-2 border">Staff Student Ratio</td>
              <td className="p-2 border">N/A</td>
            </tr>
            {tableData.map(row => (
              <tr key={row.category}>
                <td className="p-2 border">{row.category} Avg Grade</td>
                <td className="p-2 border">{row.avg.toFixed(2)} (Spread: {row.spread > 0 ? `+${row.spread}` : row.spread}, Trend: {row.trend})</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;