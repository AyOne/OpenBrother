import React, { useState, useEffect } from 'react';
import axios from "axios";



function HolderComponent() {
	const axiosConfig = {
		headers: {'Access-Control-Allow-Origin': '*'}
	};
	const [params, setParams] = useState(
		{
		chunks:[
			{
				x:2,
				z:0
			}
		],
		filter:{},
		dim:"overworld",
	});

	const [data, refreshData] = useState(
		axios.get('http://localhost:8190/front/listeTypeBlocks?',{
			headers: {	'Access-Control-Allow-Origin': '*',
						'Accept' : 'application/json'
			},
			body : params,
		})
		.then(response => {
			console.log(params);
			console.log(data);
			return(response.data);
		})
		.catch(function (error) {
			console.log(params);
			console.log(error);
		}));

	//use effect = component did mount et did update

	return(
		<div>
			Holder
		</div>
	)
}

export default HolderComponent;