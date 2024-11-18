'use client'

import { ComposableMap, Geographies, Geography } from 'react-simple-maps'
import geoData from '@/public/kz.json'

function Map({
    selectedCounty,
    setSelectedCounty,
}: {
    selectedCounty: any
    setSelectedCounty: any
}) {
    return (
        <div className=''>
            <ComposableMap
                projection='geoMercator'
                projectionConfig={{
                    center: [66.9237, 48.0196],
                    scale: 1000,
                }}
            >
                <Geographies geography={geoData}>
                    {({ geographies }: { geographies: any }) =>
                        geographies.map((geo: any) => {
                            const isSelected = selectedCounty?.id === geo.id
                            return (
                                <Geography
                                    key={geo.rsmKey}
                                    geography={geo}
                                    onClick={() =>
                                        setSelectedCounty({
                                            id: geo.id,
                                            name: geo.properties.name,
                                            type: geo.properties.type,
                                            ru_name: geo.properties.ru_name,
                                        })
                                    }
                                    style={{
                                        default: {
                                            fill: isSelected
                                                ? 'red'
                                                : '#ECEFF1',
                                            outline: 'none',
                                            stroke: 'gray',
                                            strokeWidth: 1,
                                            transition:
                                                'fill 0.3s ease, stroke 0.8s ease',
                                        },
                                        hover: {
                                            fill: isSelected
                                                ? 'red'
                                                : '#CFD8DC',
                                            outline: 'none',
                                            stroke: 'gray',
                                            strokeWidth: 1,
                                        },
                                        pressed: {
                                            fill: '#CFD8DC',
                                            outline: 'none',
                                            stroke: 'gray',
                                            strokeWidth: 1,
                                        },
                                    }}
                                />
                            )
                        })
                    }
                </Geographies>
            </ComposableMap>
        </div>
    )
}

export default Map
