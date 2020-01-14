import React from 'react';

import './App.css';
import {RadialBarChart, RadialBar, Legend, Tooltip, PieChart, Pie} from 'recharts';
import Cell from "recharts/es6/component/Cell";
import HolderComponent from "./components/HolderComponent";

function App() {
  const data = [
    {
      "name": "iron",
      "uv": 30,
      "fill": "#ccc"
    },
    {
      "name": "redstone",
      "uv": 15,
      "fill": "#f00"
    },
    {
      "name": "gold",
      "uv": 4,
      "fill": "#ff0"
    },
    {
      "name": "diamond",
      "uv": 5,
      "fill": "#0ff"
    },
    {
      "name": "coal",
      "uv": 100,
      "fill": "#000"
    },
    {
      "name": "air",
      "uv": 1000,
      "fill": "#fff"
    },
    {
      "name": "stone",
      "uv": 4000,
      "fill": "#aaa"
    }
  ];
  const data02 = [
    { name: "iron", value: 100, color:"#ccc"},
    { name: "redstone", value: 300, color:"#C00" },
    { name: "gold", value: 100, color:"#CC0" },
    { name: "diamond", value: 80, color:"#00C" },
    { name: "coal", value: 40, color:"#000" },
    { name: "air", value: 30, color:"#FFF" },
    { name: "stone", value: 50, color:"#CCC" },
  ];
  return (
    <div className="App-content">
      <RadialBarChart
        width={730}
        height={250}
        innerRadius="10%"
        outerRadius="80%"
        data={data}
        startAngle={180}
        endAngle={0}
        >
        <RadialBar
          label={{ fill: '#666', position: 'insideStart' }}
          background
          clockWise={true}
          data={data}
          dataKey='uv' />
        <Legend
          iconSize={10}
          width={120}
          height={140}
          layout='vertical'
          verticalAlign='middle'
          align="right" />
        <Tooltip />
      </RadialBarChart>
      <PieChart width={700} height={400}>
        <text
            x={305}
            y={205}
            fill="#fff"
            textAnchor="middle"
            dominantBaseline="middle"
        >
          Ores
        </text>
        <Pie
            dataKey="value"
            nameKey="name"
            data={data02}
            cx={300}
            cy={200}
            innerRadius={80}
            outerRadius={100}
            stroke={"black"}
            strokeWidth={10}
        >
          {
            data02.map((entry, index) => {
              console.log(entry);
              return <Cell key={index} fill={entry.color}/>;
            })
          }
        </Pie>
      </PieChart>
      <HolderComponent/>

    </div>


  );
}

export default App;
