import * as React from "react";
import {Pie, PieChart} from "recharts";
import Cell from "recharts/es6/component/Cell";

function PieComponent({data, radius, thickness, borderSize, borderColor}) {

	console.log(data);
	// reducing total value
	const totalValue = data.reduce((t, {value}) => t + value, 0);

	console.log("totalValue",totalValue);
	return(
		<PieChart width={radius * 2 + borderSize} height={radius * 2 + borderSize}>
			<text
				x={radius+ borderSize/2}
				y={radius+ borderSize/2}
				fill="#fff"
				textAnchor="middle"
				dominantBaseline="middle"
			>
				Ores
			</text>
			<Pie
				dataKey="value"
				nameKey="name"
				data={data}
				cx={radius}
				cy={radius}
				innerRadius={radius-thickness}
				outerRadius={radius}
				stroke={borderColor}
				strokeWidth={borderSize}
			>
				{
					data.map((entry, index) => {
						console.log(entry);
						return <Cell key={index} fill={entry.color}/>;
					})
				}
			</Pie>
		</PieChart>
	)
}

export default PieComponent;