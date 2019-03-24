
import { GetRandomColor } from '../utils/commons';

function randomScalingFactor() { return Math.round(Math.random() * 100) };

export function getData(data) {

    var labels = [], left = [], right = [], top = [], bottom = [];
    data.map((o,i) => {
        labels.unshift(o.track_date);
        left.unshift(o.left);
        right.unshift(o.right);
        // top.unshift(o.fields.top);
        // bottom.unshift(o.fields.bottom);
    })

    var lineChartData = {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: "left", 
                    borderColor:"rgb(75, 192, 192)",
                    data: left
                },
                {
                    label: "right", 
                    borderColor:"rgb(255, 128, 0)",
                    data: right
                }
            ]
        }
        
    }

    return lineChartData;
}