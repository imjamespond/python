
import { GetRandomColor } from '../utils/commons';

function randomScalingFactor() { return Math.round(Math.random() * 100) };

export function getData(data) {

    var labels = [], left = [], right = [], top = [], bottom = [];
    data.map((o,i) => {
        labels.unshift(o.track_date);
        left.unshift(o.left);
        right.unshift(o.right);
        top.unshift(o.top);
        bottom.unshift(o.bottom);
    })

    var lineChartData = {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: "left", 
                    borderColor:"#ff0000",
                    data: left
                },
                {
                    label: "right", 
                    borderColor:"#0000ff",
                    data: right
                },
                {
                    label: "top", 
                    borderColor:"#ffff00",
                    data: top
                },
                {
                    label: "bottom", 
                    borderColor:"#00ffff",
                    data: bottom
                }
            ]
        }
        
    }

    return lineChartData;
}