import * as React from "react";

function TableComponent({data}) {
		const titles = data.reduce((t, e) => {
			Object.keys(e).map(v => t.indexOf(v) === -1 ? t.push(v) : t);
			return(t);
		}, []);

	//const titles = data.reduce((t, e) => Object.keys(e).map(v => v), []);

	console.log("titles", titles);

	const sort = {
		up: (a, b) => a - b,
		down: (a, b) => b - a
	};

	return (data.length > 0 && (
		<div className="Card-content">
			<table className="Table">
				<thead>
				<tr>
					{titles.map((e, i) => <th key={i}>{e}</th>)}
				</tr>
				</thead>
				<tbody>
				{data.map((p, i) => (
					<tr key={i} style={{"color" : p.color}}>
						{titles.map((v, k) => <td key={k}>{p[v]}</td>)}
					</tr>
				))}
				</tbody>
			</table>
		</div>
	));
}

export default TableComponent;