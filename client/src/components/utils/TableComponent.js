import * as React from "react";
import {useState} from "react";
import './Table.css'
import {useEffect} from "react";

const iconsVisibility = {
	on : <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 -2 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>,
	off : <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 -2 24 24"><path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/></svg>
};

const iconsSorting = {
	up : <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 40 40"><path d="M 8 16 L 20 4 L 32 16 z"/></svg>,
	down : <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 40 40"><path d="M 8 24 H 32 H 32 L 20 36 z"/></svg>,
	middle : <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 40 40"><path d="M 8 16 L 20 4 L 32 16 z M 8 24 H 32 H 32 L 20 36 z"/></svg>,
};



function TableComponent({data, onChange, visibility}) {
		const titles = data.reduce((t, e) => {
			Object.keys(e).map(v => t.indexOf(v) === -1 ? t.push(v) : t);
			return(t);
		}, []);
//		data = boolToIcon(data);
	//const titles = data.reduce((t, e) => Object.keys(e).map(v => v), []);
	const [sortTableState, setSortTableState] = useState([]);
	const dataTmp = Array.from(data);
	const swapValue = (i,v) => {
		dataTmp[i][v] = !dataTmp[i][v];
		onChange(dataTmp);
	};


	//didmount
	useEffect(() => {
		const sortTable = {};
		titles.map(v => {
			sortTable[v] = 0;
		});
		setSortTableState(sortTable);
		console.log(sortTable);

	},[]);

	useEffect(() => {
		let index;
		// find index to sort
		for (let [k,v] of Object.entries(sortTableState)) {
			if (v !== 0)
				index = k;
		}
		// verify existing sorting set
		if (index) {
			// verify types
			let type = "";
			let errorType = false;
			let noValue = false;
			for (let v of dataTmp) {
				console.log("TEST");
				console.log("TEST2", v[index]);
				if (type === "")
					type = typeof v[index];
				else if (type !== typeof v[index]) {
					// check if undefined value
					if (type === "undefined" || typeof v[index] === "undefined")
						noValue = true;
					errorType = true;
					break;
				}
			}

			// TODO Implement undefined value consistent sorting
			// break if different types
			if (errorType/* && (type !== "string" && )*/) {
				console.error("ERROR TYPE in Table");
				return;
			}

			// solving undefined value
			for (let v of dataTmp) {
				if (type !== "undefined") {
					if (v[index] === undefined) {
						if (type === "string")
							v[index] = "";
/*						else if (type === "boolean")
							v[index] = false;
						else
							v[index] = 0;*/
					}
				}
			}

			// sort table
			console.log("TYPE", type);
			if (type === "string")
				dataTmp.sort((a, b) => {
					if (sortTableState[index] === 1)
						return a[index].localeCompare(b[index]);
					if (sortTableState[index] === -1)
						return b[index].localeCompare(a[index]);
				});
			else
				dataTmp.sort((a, b) => {
					if (sortTableState[index] === 1)
						return a[index] - b[index];
					if (sortTableState[index] === -1)
						return b[index] - a[index];
				});
			onChange(dataTmp);
		}
	},[sortTableState]);

/*	const sortByIndex = (index) => {
		dataTmp.sort((a, b) => {
			if(sortTableState[index] === 1)
				return a[index] - b[index];
			if(sortTableState[index] === -1)
				return b[index] - a[index];
		});
		onChange(dataTmp);
	};*/

	const sortTable = (index) => {
		const sortTableTmp = {...sortTableState};
		for (let [k,v] of Object.entries(sortTableTmp)) {
			if (k !== index) {sortTableTmp[k]= 0; continue;}
			if (v === 1 && k === index) {
				sortTableTmp[k] = -1;
				continue;
			}
			if (v === -1 && k === index) {
				sortTableTmp[k] = 0;
				continue;
			}
			if (v === 0 && k === index) {
				sortTableTmp[k] = 1;
			}
		}
		setSortTableState(sortTableTmp);
/*		sortByIndex(index);*/
	};

	const makeArrow = (e) => {
		if(sortTableState[e] === 0)
			return iconsSorting.middle;
		if(sortTableState[e] === 1)
			return iconsSorting.up;
		if(sortTableState[e] === -1)
			return iconsSorting.down;
	};

	return (
		dataTmp.length > 0 && (
		<div className="Card-content">
			<table className="Table">
				<thead className="Table-head">
					<tr>
						{titles.map((e, i) => <th className="Head-text" key={i} onClick={() => sortTable(e)}>{e} <div className="Arrow">{makeArrow(e)}</div></th>)}
					</tr>
				</thead>
				<tbody>
				{dataTmp.map((p, i) => (
					<tr key={i} style={{"color" : p.color}}>
						{titles.map((v, k) => v === visibility ? p[v] ? <td key={k} style={{height:"100%"}} onClick={() => {
							swapValue(i,v);
						}}>{iconsVisibility.on}</td> : <td key={k} onClick={() => {
							swapValue(i,v);
						}}>{iconsVisibility.off}</td>
							: <td key={k} className="Table-block">{p[v]}</td> )}
					</tr>
				))}
				</tbody>
			</table>
		</div>
	));
}

export default TableComponent;