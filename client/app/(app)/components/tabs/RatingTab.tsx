'use client'

import React, { useState, useEffect } from 'react'
import {
    Center,
    Loader,
    Slider,
    Badge,
    Table,
    SegmentedControl,
    Text,
    Button,
} from '@mantine/core'
import {
    getRegionalSectorImportance,
    getRegionalAutoSimulation,
    getRegionalManualSimulation,
} from '@/app/api/ranking.api'
import sectors from '../../utils/sectors'

const RatingTab = ({ region }: { region: any }) => {
    const [impactMode, setImpactMode] = useState('feature_importance')
    const [data, setData]: any = useState(null)
    const [dataLoading, setDataLoading]: any = useState(false)
    const [featuresMap, setFeaturesMap]: any = useState(
        sectors.reduce((mp: any, sector: any) => {
            mp[sector] = 1
            return mp
        }, {})
    )
    const loadRegionalManualSimulation = async (
        region: any,
        features_map: any
    ) => {
        setDataLoading(true)
        const temp = await getRegionalManualSimulation({
            region,
            features_map,
        })
        setData(temp)
        setDataLoading(false)
    }
    useEffect(() => {
        const loadRegionalSectorImportance = async (region: any) => {
            setDataLoading(true)
            const temp = await getRegionalSectorImportance({ region })
            setData(temp)
            setDataLoading(false)
        }
        const loadRegionalAutoSimulation = async (region: any) => {
            setDataLoading(true)
            const temp = await getRegionalAutoSimulation({ region })
            setData(temp)
            setDataLoading(false)
        }
        if (region) {
            if (impactMode == 'feature_importance') {
                loadRegionalSectorImportance(region.ru_name)
            } else if (impactMode == 'auto_simulation') {
                loadRegionalAutoSimulation(region.ru_name)
            }
        }
    }, [region, impactMode])

    return (
        <div className='flex flex-col overflow-auto'>
            <div className='border-b p-4'>
                <Text size='sm' fw={500} mb={1}>
                    Тип расчета значимости сектора инфраструктуры для экономики
                    региона
                </Text>
                <SegmentedControl
                    withItemsBorders={false}
                    value={impactMode}
                    onChange={setImpactMode}
                    data={[
                        {
                            value: 'feature_importance',
                            label: 'Важность в ИИ модели',
                        },
                        {
                            value: 'auto_simulation',
                            label: 'Авто-симуляционный расчет',
                        },
                        {
                            value: 'manual_simulation',
                            label: 'Ручная симуляция',
                        },
                    ]}
                />
            </div>
            <div className='p-5 grow overflow-auto flex flex-col'>
                {dataLoading ? (
                    <Loader />
                ) : impactMode === 'manual_simulation' ? (
                    <div className='overflow-hidden'>
                        <div className='border-b max-h-[460px] overflow-auto'>
                            <Text size='sm' fw={500} mb={8}>
                                Выберите симуляционный прирост для
                                нижеприведенных секторов инфраструктуры
                            </Text>
                            {sectors.map((sector, i) => (
                                <div
                                    key={i}
                                    className='flex p-3 mb-3 border rounded-lg bg-slate-50'
                                >
                                    <div className='w-[300px] mr-4'>
                                        {sector}
                                    </div>
                                    <div className='grow'>
                                        <Slider
                                            value={(
                                                (featuresMap[sector] - 1) *
                                                100
                                            ).toFixed(2)}
                                            onChange={(val) =>
                                                setFeaturesMap((prev: any) => ({
                                                    ...prev,
                                                    [sector]: 1 + val / 100,
                                                }))
                                            }
                                            marks={[
                                                {
                                                    value: 20,
                                                    label: '20%',
                                                },
                                                {
                                                    value: 40,
                                                    label: '40%',
                                                },
                                                {
                                                    value: 60,
                                                    label: '60%',
                                                },
                                                {
                                                    value: 80,
                                                    label: '80%',
                                                },
                                            ]}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className='flex py-4 justify-between items-center min-h-[80px] overflow-hidden sticky bottom-0 left-0'>
                            <Button
                                onClick={() =>
                                    loadRegionalManualSimulation(
                                        region.ru_name,
                                        featuresMap
                                    )
                                }
                            >
                                Симуляция
                            </Button>
                            {data ? (
                                !data.error && data.impact !== undefined ? (
                                    <div className='font-semibold p-2 rounded-lg border bg-slate-100'>
                                        Прогнозируемый прирост ВВП:{' '}
                                        {(data.impact * 0.1).toFixed(2)} трлн.
                                        тенге
                                    </div>
                                ) : data.code && data.code === 10203 ? (
                                    <div className='font-semibold p-2 rounded-lg border bg-slate-100'>
                                        Недостаточно данных по выбранным
                                        отраслям
                                    </div>
                                ) : (
                                    <></>
                                )
                            ) : (
                                <></>
                            )}
                        </div>
                    </div>
                ) : data && !data.error ? (
                    <div className='min-h-[400px] grow overflow-auto'>
                        {impactMode === 'feature_importance' ? (
                            <Table
                                data={{
                                    head: [
                                        'Инфраструктурный сектор',
                                        'Важность в ИИ модели',
                                        'Приоритет',
                                    ],
                                    body: Object.keys(data).map((key, i) => [
                                        key,
                                        data[key].toFixed(2),
                                        i < Object.keys(data).length / 3 ? (
                                            <Badge color='green'>Высокий</Badge>
                                        ) : i <
                                          Object.keys(data).length * (2 / 3) ? (
                                            <Badge color='orange'>
                                                Средний
                                            </Badge>
                                        ) : (
                                            <Badge color='red'>Низкий</Badge>
                                        ),
                                    ]),
                                }}
                            />
                        ) : impactMode === 'auto_simulation' ? (
                            <Table
                                data={{
                                    head: [
                                        'Инфраструктурный сектор',
                                        'Прирост ВВП (в трлн. тенге)',
                                        'Эффективность инвестиции',
                                    ],
                                    body: Object.keys(data).map((key, i) => [
                                        key,
                                        (data[key] * 0.1).toFixed(2),
                                        i < Object.keys(data).length / 3 ? (
                                            <Badge color='green'>Высокая</Badge>
                                        ) : i <
                                          Object.keys(data).length * (2 / 3) ? (
                                            <Badge color='orange'>
                                                Средняя
                                            </Badge>
                                        ) : (
                                            <Badge color='red'>Низкая</Badge>
                                        ),
                                    ]),
                                }}
                            />
                        ) : (
                            <></>
                        )}
                    </div>
                ) : (
                    <Center>
                        <div className=''>
                            Выберите соответствующие параметры для отображения
                            данных
                        </div>
                    </Center>
                )}
            </div>
        </div>
    )
}

export default RatingTab
