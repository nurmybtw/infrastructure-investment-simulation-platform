'use client'

import React, { useEffect, useState } from 'react'
import Image from 'next/image'

import { Group, SegmentedControl, Text } from '@mantine/core'
import Map from './Map'

import DataTab from './tabs/DataTab'
import RatingTab from './tabs/RatingTab'
import SatteliteTab from './tabs/SatteliteTab'

const Stats = () => {
    const [selectedCounty, setSelectedCounty]: any = useState({
        id: 13,
        name: 'Astana',
        type: 'City',
        ru_name: 'г. Астана',
    })

    const [tab, setTab]: any = useState('data')

    return (
        <div className='flex gap-5 grow overflow-auto'>
            <div className='basis-0 grow-[9]'>
                <div className='border-b p-4 border rounded-lg bg-white mb-4'>
                    <SegmentedControl
                        withItemsBorders={false}
                        value={tab}
                        onChange={setTab}
                        data={[
                            {
                                value: 'data',
                                label: 'Данные',
                            },
                            {
                                value: 'rating',
                                label: 'Рейтинг секторов инфраструктуры',
                            },
                            {
                                value: 'condition',
                                label: 'Состояние инфраструктуры',
                            },
                        ]}
                    />
                </div>
                <div className='border rounded-lg bg-white'>
                    <div className='max-h-[500px]'>
                        <Map
                            selectedCounty={selectedCounty}
                            setSelectedCounty={setSelectedCounty}
                        />
                    </div>
                    <div className='border-t p-4'>
                        <div className='font-semibold text-xl'>
                            {selectedCounty?.type &&
                            selectedCounty.type === 'City'
                                ? `Город ${
                                      selectedCounty.ru_name.split(' ')[1]
                                  }`
                                : `${selectedCounty.ru_name} Область`}
                        </div>
                    </div>
                </div>
            </div>
            <div className='basis-0 grow-[11] border rounded-lg bg-white overflow-auto flex flex-col'>
                {/* <div className='flex max-w-full flex-col'> */}

                <div className='grow overflow-auto'>
                    {tab === 'data' ? (
                        <DataTab region={selectedCounty} />
                    ) : tab === 'rating' ? (
                        <RatingTab region={selectedCounty} />
                    ) : (
                        <SatteliteTab region={selectedCounty} />
                    )}
                </div>
            </div>
        </div>
    )
}

export default Stats
