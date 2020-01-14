import React, { useState, useEffect } from 'react';
import axios from "axios";



function HolderComponent() {
	const axiosConfig = {
		headers: {'Access-Control-Allow-Origin': '*'}
	};

	const [data, setData] = useState(
		axios.get('http://localhost:5000/listeTypeBlocks',axiosConfig)
		.then(response => {
			console.log(data);
			return(response.data);
		})
		.catch(function (error) {
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