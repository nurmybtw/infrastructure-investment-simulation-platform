'use client'

import React, { useState, useEffect } from 'react'
import {
    Center,
    Loader,
    NativeSelect,
    Group,
    SegmentedControl,
    Text,
} from '@mantine/core'
import Chart from '../Chart'

import { get5YearPrediction, getHistoricalData } from '@/app/api/data.api'
import sectors from '../../utils/sectors'

const DataTab = ({ region }: { region: any }) => {
    const [analysisType, setAnalysisType]: any = useState('historical')
    const [sector, setSector]: any = useState(
        'Снабжение электроэнергией, газом, паром, горячей водой и кондиционированным воздухом'
    )
    const [data, setData]: any = useState(null)
    const [dataLoading, setDataLoading]: any = useState(false)

    useEffect(() => {
        const loadHistoricalData = async (region: any, sector: any) => {
            setDataLoading(true)
            const temp = await getHistoricalData({ region, sector })
            setData(temp)
            setDataLoading(false)
        }
        const load5YearPrediction = async (region: any, sector: any) => {
            setDataLoading(true)
            const temp = await get5YearPrediction({ region, sector })
            setData(temp)
            setDataLoading(false)
        }
        if (region) {
            if (analysisType == 'historical') {
                loadHistoricalData(region.ru_name, sector)
            } else if (analysisType == 'forecast') {
                load5YearPrediction(region.ru_name, sector)
            }
        }
    }, [region, sector, analysisType])

    return (
        <div className='flex flex-col overflow-auto'>
            <div className='border-b p-4'>
                <Group>
                    <NativeSelect
                        label='Выберите данные для вывода'
                        data={sectors}
                        value={sector}
                        onChange={(event) =>
                            setSector(event.currentTarget.value)
                        }
                    />
                    <div>
                        <Text size='sm' fw={500} mb={1}>
                            Тип анализа
                        </Text>
                        <SegmentedControl
                            withItemsBorders={false}
                            value={analysisType}
                            onChange={setAnalysisType}
                            data={[
                                {
                                    value: 'historical',
                                    label: 'История',
                                },
                                {
                                    value: 'forecast',
                                    label: 'Прогноз на 5 лет',
                                },
                            ]}
                        />
                    </div>
                </Group>
            </div>
            <div className='p-8 grow overflow-auto flex flex-col'>
                {dataLoading ? (
                    <Loader />
                ) : (
                    <div className='grow overflow-auto min-h-[400px]'>
                        {data && !data.error ? (
                            <Chart data={data} />
                        ) : (
                            <Center>
                                <div className=''>No data to display</div>
                            </Center>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

export default DataTab
