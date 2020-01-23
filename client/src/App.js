import React from 'react';

import './App.css';
import {RadialBarChart, RadialBar, Legend, Tooltip, PieChart, Pie} from 'recharts';
import Cell from "recharts/es6/component/Cell";
import HolderComponent from "./components/HolderComponent";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import PieComponent from "./components/PieComponent";
import {Container} from "@material-ui/core";
import TableComponent from "./components/utils/TableComponent";


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
		{name: "iron", value: 100, color: "#ccc", prout:10},
		{name: "redstone", value: 300, color: "#C00", prout:10},
		{name: "gold", value: 100, color: "#CC0", prout:10},
		{name: "diamond", value: 80, color: "#00C", prout:11},
		{name: "coal", value: 40, color: "#000", prout:11},
		{name: "air", value: 30, color: "#FFF"},
		{name: "stone", value: 50, color: "#CCC"},
	];
	return (
		<div className="App-content">
			<div className="Container">
				<Card className="Card-content">
					<CardContent className="Card">
						<div>
							<PieComponent radius={150} thickness={20} data={data02} borderSize={10} borderColor={"black"} />
							<TableComponent data={data02} />
						</div>
					</CardContent>
				</Card>
			</div>
		</div>


	);
}

export default App;
