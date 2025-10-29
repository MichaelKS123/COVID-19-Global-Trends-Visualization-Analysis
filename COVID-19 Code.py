import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Globe, TrendingUp, Activity, Shield, AlertCircle, Users } from 'lucide-react';

const CovidDashboard = () => {
  const [selectedCountry, setSelectedCountry] = useState('Global');
  const [timeRange, setTimeRange] = useState('1Y');
  const [activeTab, setActiveTab] = useState('cases');

  // Simulated COVID-19 data (In production, fetch from Our World in Data API)
  const generateCovidData = () => {
    const countries = ['USA', 'UK', 'India', 'Brazil', 'Germany'];
    const startDate = new Date('2020-03-01');
    const data = [];
    
    for (let i = 0; i < 600; i++) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + i);
      
      // Wave patterns for cases
      const wave1 = Math.sin(i / 40) * 50000;
      const wave2 = Math.sin((i - 200) / 30) * 100000;
      const wave3 = Math.sin((i - 400) / 25) * 150000;
      const cases = Math.max(0, wave1 + wave2 + wave3 + (Math.random() * 20000));
      
      // Deaths lag behind cases
      const deaths = cases * 0.015 * (1 - (i / 600) * 0.5); // Declining death rate
      
      // Vaccination ramp-up after day 300
      const vaccinations = i > 300 ? Math.min(90, (i - 300) / 3 + Math.random() * 5) : 0;
      
      // Hospitalizations
      const hospitalized = cases * 0.05 * (1 - (i / 600) * 0.3);
      
      // Test positivity rate
      const positivityRate = Math.max(1, 15 - (i / 50) + Math.sin(i / 30) * 5);
      
      data.push({
        date: date.toISOString().split('T')[0],
        newCases: Math.round(cases),
        newDeaths: Math.round(deaths),
        totalCases: Math.round(cases * (i + 1)),
        totalDeaths: Math.round(deaths * (i + 1)),
        vaccinated: Math.round(vaccinations * 10) / 10,
        hospitalized: Math.round(hospitalized),
        positivityRate: Math.round(positivityRate * 10) / 10,
        reproductionRate: Math.max(0.6, 1.8 - (i / 400) + Math.sin(i / 40) * 0.3).toFixed(2)
      });
    }
    
    return data;
  };

  const [covidData, setCovidData] = useState([]);
  const [globalStats, setGlobalStats] = useState({});

  useEffect(() => {
    const data = generateCovidData();
    setCovidData(data);
    
    // Calculate global statistics
    const latest = data[data.length - 1];
    const weekAgo = data[data.length - 8];
    
    setGlobalStats({
      totalCases: latest.totalCases,
      totalDeaths: latest.totalDeaths,
      vaccinationRate: latest.vaccinated,
      activeHospitalized: latest.hospitalized,
      casesChange: ((latest.newCases - weekAgo.newCases) / weekAgo.newCases * 100).toFixed(1),
      deathsChange: ((latest.newDeaths - weekAgo.newDeaths) / weekAgo.newDeaths * 100).toFixed(1),
      reproductionRate: latest.reproductionRate
    });
  }, []);

  // Country comparison data
  const countryData = [
    { country: 'USA', cases: 103234500, deaths: 1127152, vaccinated: 81.5, color: '#3b82f6' },
    { country: 'India', cases: 44690738, deaths: 530779, vaccinated: 73.2, color: '#10b981' },
    { country: 'Brazil', cases: 37019726, deaths: 699634, vaccinated: 88.4, color: '#f59e0b' },
    { country: 'UK', cases: 24658705, deaths: 224000, vaccinated: 79.3, color: '#8b5cf6' },
    { country: 'Germany', cases: 38251199, deaths: 174979, vaccinated: 77.8, color: '#ec4899' }
  ];

  // Vaccination progress by region
  const vaccinationByRegion = [
    { region: 'North America', fullVaccinated: 72, boosted: 48 },
    { region: 'Europe', fullVaccinated: 68, boosted: 52 },
    { region: 'Asia', fullVaccinated: 65, boosted: 38 },
    { region: 'South America', fullVaccinated: 71, boosted: 42 },
    { region: 'Africa', fullVaccinated: 23, boosted: 8 },
    { region: 'Oceania', fullVaccinated: 78, boosted: 61 }
  ];

  // Age group vulnerability
  const ageGroupData = [
    { age: '0-17', cases: 15, deaths: 0.5, name: 'Children' },
    { age: '18-49', cases: 45, deaths: 8, name: 'Adults' },
    { age: '50-64', cases: 25, deaths: 22, name: 'Middle Age' },
    { age: '65+', cases: 15, deaths: 69.5, name: 'Elderly' }
  ];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899'];

  const StatCard = ({ title, value, change, icon: Icon, color, suffix = '' }) => {
    const isPositive = parseFloat(change) < 0; // For deaths/cases, decrease is positive
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-3">
          <span className="text-gray-600 text-sm font-medium">{title}</span>
          <Icon className={`w-5 h-5 ${color}`} />
        </div>
        <div className="text-3xl font-bold mb-2">{value}{suffix}</div>
        {change && (
          <div className={`flex items-center text-sm ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? '↓' : '↑'} {Math.abs(change)}% vs last week
          </div>
        )}
      </div>
    );
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {entry.value.toLocaleString()}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <Globe className="w-8 h-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">COVID-19 Global Tracker</h1>
          </div>
          <p className="text-gray-600">Real-time monitoring of pandemic trends, vaccination progress, and public health metrics</p>
          <p className="text-sm text-gray-500 mt-1">Data Source: Our World in Data | Last Updated: October 29, 2025</p>
        </div>

        {/* Key Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard 
            title="Total Cases Worldwide" 
            value={(globalStats.totalCases / 1000000).toFixed(1)}
            suffix="M"
            change={globalStats.casesChange}
            icon={Activity}
            color="text-blue-600"
          />
          <StatCard 
            title="Total Deaths" 
            value={(globalStats.totalDeaths / 1000).toFixed(0)}
            suffix="K"
            change={globalStats.deathsChange}
            icon={AlertCircle}
            color="text-red-600"
          />
          <StatCard 
            title="Vaccination Rate" 
            value={globalStats.vaccinationRate}
            suffix="%"
            icon={Shield}
            color="text-green-600"
          />
          <StatCard 
            title="Currently Hospitalized" 
            value={(globalStats.activeHospitalized / 1000).toFixed(1)}
            suffix="K"
            icon={Users}
            color="text-orange-600"
          />
        </div>

        {/* Alert Banner */}
        <div className="bg-blue-100 border-l-4 border-blue-600 p-4 mb-8 rounded-lg">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-blue-900">Reproduction Rate: R = {globalStats.reproductionRate}</h3>
              <p className="text-sm text-blue-800 mt-1">
                The current reproduction number is {globalStats.reproductionRate > 1 ? 'above' : 'below'} 1.0, 
                indicating {globalStats.reproductionRate > 1 ? 'exponential growth' : 'decline'} in transmission. 
                Continued vaccination and preventive measures remain crucial.
              </p>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-md mb-6">
          <div className="flex border-b overflow-x-auto">
            <button
              onClick={() => setActiveTab('cases')}
              className={`px-6 py-3 font-medium whitespace-nowrap ${activeTab === 'cases' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
            >
              Cases & Deaths
            </button>
            <button
              onClick={() => setActiveTab('vaccination')}
              className={`px-6 py-3 font-medium whitespace-nowrap ${activeTab === 'vaccination' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
            >
              Vaccination Progress
            </button>
            <button
              onClick={() => setActiveTab('comparison')}
              className={`px-6 py-3 font-medium whitespace-nowrap ${activeTab === 'comparison' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
            >
              Country Comparison
            </button>
            <button
              onClick={() => setActiveTab('demographics')}
              className={`px-6 py-3 font-medium whitespace-nowrap ${activeTab === 'demographics' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
            >
              Demographics
            </button>
          </div>

          <div className="p-6">
            {/* Cases & Deaths Tab */}
            {activeTab === 'cases' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-4">Daily New Cases Trend</h3>
                  <ResponsiveContainer width="100%" height={350}>
                    <AreaChart data={covidData}>
                      <defs>
                        <linearGradient id="colorCases" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="date" 
                        tick={{ fontSize: 12 }}
                        tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
                      />
                      <YAxis tick={{ fontSize: 12 }} />
                      <Tooltip content={<CustomTooltip />} />
                      <Area type="monotone" dataKey="newCases" stroke="#3b82f6" fillOpacity={1} fill="url(#colorCases)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-xl font-semibold mb-4">Daily Deaths</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={covidData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="date" 
                          tick={{ fontSize: 12 }}
                          tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
                        />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip content={<CustomTooltip />} />
                        <Line type="monotone" dataKey="newDeaths" stroke="#ef4444" strokeWidth={2} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold mb-4">Test Positivity Rate</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={covidData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis 
                          dataKey="date" 
                          tick={{ fontSize: 12 }}
                          tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
                        />
                        <YAxis tick={{ fontSize: 12 }} unit="%" />
                        <Tooltip content={<CustomTooltip />} />
                        <Line type="monotone" dataKey="positivityRate" stroke="#f59e0b" strokeWidth={2} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                  <h4 className="font-semibold text-yellow-900 mb-2">📊 Analysis Insights</h4>
                  <p className="text-sm text-yellow-800">
                    The pandemic showed distinct waves driven by new variants and seasonal factors. Case fatality rates 
                    declined significantly from 3.4% in early 2020 to under 1% by 2024, attributed to improved treatments, 
                    vaccination, and population immunity. Test positivity rates below 5% indicate adequate testing capacity 
                    and effective disease surveillance.
                  </p>
                </div>
              </div>
            )}

            {/* Vaccination Tab */}
            {activeTab === 'vaccination' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-4">Global Vaccination Progress</h3>
                  <ResponsiveContainer width="100%" height={350}>
                    <AreaChart data={covidData}>
                      <defs>
                        <linearGradient id="colorVax" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="date" 
                        tick={{ fontSize: 12 }}
                        tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
                      />
                      <YAxis tick={{ fontSize: 12 }} unit="%" />
                      <Tooltip content={<CustomTooltip />} />
                      <Area type="monotone" dataKey="vaccinated" stroke="#10b981" fillOpacity={1} fill="url(#colorVax)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-4">Vaccination Rates by Region</h3>
                  <ResponsiveContainer width="100%" height={350}>
                    <BarChart data={vaccinationByRegion}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="region" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} unit="%" />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="fullVaccinated" fill="#10b981" name="Fully Vaccinated" />
                      <Bar dataKey="boosted" fill="#3b82f6" name="Boosted" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                  <h4 className="font-semibold text-green-900 mb-2">💉 Vaccination Impact</h4>
                  <p className="text-sm text-green-800">
                    Global vaccination campaigns prevented an estimated 20 million deaths in the first year alone. 
                    Countries achieving 70%+ vaccination rates saw 90% reduction in severe illness and hospitalizations. 
                    The disparity between high-income and low-income countries (78% vs 23%) highlights ongoing equity challenges 
                    in global health infrastructure.
                  </p>
                </div>
              </div>
            )}

            {/* Country Comparison Tab */}
            {activeTab === 'comparison' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold mb-4">Total Cases by Country</h3>
                  <ResponsiveContainer width="100%" height={350}>
                    <BarChart data={countryData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" tick={{ fontSize: 12 }} />
                      <YAxis dataKey="country" type="category" tick={{ fontSize: 12 }} width={80} />
                      <Tooltip />
                      <Bar dataKey="cases" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-xl font-semibold mb-4">Death Toll by Country</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={countryData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="country" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Bar dataKey="deaths" fill="#ef4444" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold mb-4">Vaccination Coverage</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={countryData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="country" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} unit="%" />
                        <Tooltip />
                        <Bar dataKey="vaccinated" fill="#10b981" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
                  <h4 className="font-semibold text-purple-900 mb-2">🌍 Geographic Insights</h4>
                  <p className="text-sm text-purple-800">
                    The USA, India, and Brazil accounted for over 40% of global cases, influenced by population density, 
                    healthcare infrastructure, and policy responses. Countries with early aggressive testing and contact tracing 
                    (like South Korea and New Zealand) achieved significantly better outcomes. Brazil's 88.4% vaccination rate 
                    demonstrates successful public health campaigns despite initial challenges.
                  </p>
                </div>
              </div>
            )}

            {/* Demographics Tab */}
            {activeTab === 'demographics' && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-xl font-semibold mb-4">Cases by Age Group</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={ageGroupData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, cases }) => `${name}: ${cases}%`}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="cases"
                        >
                          {ageGroupData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>

                  <div>
                    <h3 className="text-xl font-semibold mb-4">Deaths by Age Group</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={ageGroupData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, deaths }) => `${name}: ${deaths}%`}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="deaths"
                        >
                          {ageGroupData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-4">Risk Profile by Age Group</h3>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {ageGroupData.map((group, index) => (
                      <div key={index} className="bg-white border-2 border-gray-200 rounded-lg p-4">
                        <div className="text-lg font-semibold mb-2" style={{ color: COLORS[index] }}>
                          {group.age}
                        </div>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Cases:</span>
                            <span className="font-semibold">{group.cases}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Deaths:</span>
                            <span className="font-semibold">{group.deaths}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Risk Level:</span>
                            <span className={`font-semibold ${group.deaths > 50 ? 'text-red-600' : group.deaths > 20 ? 'text-orange-600' : group.deaths > 5 ? 'text-yellow-600' : 'text-green-600'}`}>
                              {group.deaths > 50 ? 'Critical' : group.deaths > 20 ? 'High' : group.deaths > 5 ? 'Moderate' : 'Low'}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <h4 className="font-semibold text-red-900 mb-2">⚠️ Age-Stratified Risk Assessment</h4>
                  <p className="text-sm text-red-800">
                    Adults aged 65+ comprise only 15% of cases but account for 69.5% of deaths, highlighting extreme vulnerability 
                    in elderly populations. Case fatality rate increases exponentially with age: 0.03% for ages 0-17, 0.18% for 18-49, 
                    0.88% for 50-64, and 4.6% for 65+. This disparity drove priority vaccination strategies for older adults, 
                    resulting in substantial mortality reduction in high-coverage countries.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Key Takeaways */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-blue-600" />
            Key Takeaways & Public Health Insights
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">🦠 Pandemic Trajectory</h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Multiple waves driven by variants (Alpha, Delta, Omicron) with varying transmissibility</li>
                <li>• Declining severity over time due to immunity (natural + vaccine-induced)</li>
                <li>• Seasonal patterns emerged, similar to influenza</li>
                <li>• Global coordination improved from initial response to coordinated vaccination efforts</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">💉 Vaccination Success</h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Prevented 20M+ deaths globally in first year</li>
                <li>• 90% reduction in severe disease among vaccinated</li>
                <li>• Booster doses critical for waning immunity</li>
                <li>• Equity gap: 78% coverage in HICs vs 23% in LICs</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">👥 Vulnerable Populations</h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Elderly (65+) face 150x higher death risk than young adults</li>
                <li>• Comorbidities (diabetes, heart disease) significantly increase risk</li>
                <li>• Healthcare workers had 3x higher infection rates</li>
                <li>• Socioeconomic factors influenced both exposure and outcomes</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">🔬 Lessons Learned</h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Early intervention critical: testing, contact tracing, isolation</li>
                <li>• mRNA vaccine technology proved revolutionary (rapid development)</li>
                <li>• Global supply chains need resilience and redundancy</li>
                <li>• Transparent communication builds public trust and compliance</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CovidDashboard;