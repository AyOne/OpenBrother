import React, {useEffect, useState} from 'react';

import './App.css'
import PieComponent from "./components/PieComponent";
import TableComponent from "./components/utils/TableComponent";
import axios from "axios";


function App() {

	const [data02, setData] = useState([
		{name: "iron", value: 100, color: "#ccc", visibility: true},
		{name: "redstone", value: 300, color: "#C00", visibility: true},
		{name: "gold", value: 100, color: "#CC0", visibility: true},
		{name: "diamond", value: 80, color: "#00C", visibility: false},
		{name: "coal", value: 40, color: "#000", visibility: false},
		{name: "air", value: 30, color: "#FFF", visibility: true},
		{name: "stone", value: 50, color: "#CCC", visibility: true},
	]);

	const [data, refreshData] = useState();
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

	useEffect(() => {
		// code to run on component mount
		console.log("Effect");
		axios.get('http://localhost:8190/listeTypeBlocks?', {
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Accept': 'application/json'
			},
			params: params,
		})
			.then(response => {
				console.log("params", params);
				console.log("data", response.data);
				//		const tmp = response.data.map();
				console.log("tmp", Object.keys(response.data));
				refreshData(response.data);
			})
			.catch(function (error) {
				console.log(params);
				console.log(error);
			})
	}, []);

	const changeData = (value) => {
		console.log("TESt", value);
		setData(value);
	};

	return (
		<div className="App-content">
			<div style={{overflow: "hidden", float: "right", alignSelf: "right", position:"relative"}}>
				<div className="Store-hide">
					sdkfjskfjsd
				</div>
				<div className="Store-button-hide">
					<div> ></div>
				</div>
			</div>
			<div className="Container">
				<div className="Card-content">
					<div className="Card">
						<div>
							<PieComponent radius={150} thickness={20} data={data02} borderSize={10}
										  borderColor={"black"}/>
							<TableComponent data={data02} onChange={changeData} visibility="visibility"/>
						</div>
					</div>
				</div>
				<button onClick={() => {
					axios.get('http://localhost:8190/debug/rebuild?', {params: {data: {radius: 2}}}).then(r => console.log(r)).catch(e => console.log(e))
				}}/>
			</div>

		</div>


	);
}

export default App;
