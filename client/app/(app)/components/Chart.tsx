'use client'

import React from 'react'

import { Line } from 'react-chartjs-2'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title as ChartTitle,
    Tooltip,
    Legend,
} from 'chart.js'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    ChartTitle,
    Tooltip,
    Legend
)

const Chart = ({ data }: { data: any }) => {
    return (
        <Line
            data={{
                labels: data.labels,
                datasets: [
                    {
                        label: data.dataset,
                        data: data.values,
                        fill: false,
                        borderColor: 'green',
                    },
                ],
            }}
            options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                },
            }}
        />
    )
}

export default Chart
