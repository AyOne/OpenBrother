import React, {useState} from 'react';

import './App.css';
import {RadialBarChart, RadialBar, Legend, Tooltip, PieChart, Pie} from 'recharts';
import Cell from "recharts/es6/component/Cell";
import HolderComponent from "./components/HolderComponent";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import PieComponent from "./components/PieComponent";
import {Container} from "@material-ui/core";
import TableComponent from "./components/utils/TableComponent";
import axios from "axios";


function App() {

	const data02 = [
		{name: "iron", value: 100, color: "#ccc", prout: 10},
		{name: "redstone", value: 300, color: "#C00", prout: 10},
		{name: "gold", value: 100, color: "#CC0", prout: 10},
		{name: "diamond", value: 80, color: "#00C", prout: 11},
		{name: "coal", value: 40, color: "#000", prout: 11},
		{name: "air", value: 30, color: "#FFF"},
		{name: "stone", value: 50, color: "#CCC"},
	];
	const axiosConfig = {
		headers: {'Access-Control-Allow-Origin': '*'}
	};
	const [params, setParams] = useState({
			data: {
				chunks: [
					{
						x: 2,
						z: 0
					}
				],
				filter: {},
				dim: "overworld",
			}
		});
	const [data, refreshData] = useState(axios.get('http://localhost:8190/listeTypeBlocks?', {
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Accept': 'application/json'
			},
			params: params,
		})
			.then(response => {
				console.log(params);
				console.log(data);
				return (response.data);
			})
			.catch(function (error) {
				console.log(params);
				console.log(error);
			}));

	return (
		<div className="App-content">
			<div className="Container">
				<Card className="Card-content">
					<CardContent className="Card">
						<div>
							<PieComponent radius={150} thickness={20} data={data02} borderSize={10}
										  borderColor={"black"}/>
							<TableComponent data={data02}/>
						</div>
					</CardContent>
				</Card>
					<button onClick={() => {axios.get('http://localhost:8190/debug/rebuild?', {params : {data:{radius : 2}}}).then(r => console.log(r)).catch(e => console.log(e))}}/>
			</div>
		</div>


	);
}

export default App;
