'use client'

import React from 'react'
import { Text } from '@mantine/core'

const SatteliteTab = ({ region }: { region: any }) => {
    const spatialData = {
        region_id: 13,
        cracks_count: 1,
        agriculture: 0,
        road: 1146.3000000000002,
        methane: 0,
        old_road: 0,
        damage: 786.3000000000001,
        water: 0,
    }
    return (
        <div className='p-8'>
            {spatialData.region_id === region.id ? (
                <div className=''>
                    <Text mb={4}>
                        <span className='font-semibold'>
                            Number of road cracks detected:{' '}
                        </span>
                        {spatialData.cracks_count}
                    </Text>
                    <Text mb={4}>
                        <span className='font-semibold'>
                            Normal roads area:{' '}
                        </span>
                        {spatialData.road} m<sup>2</sup>
                    </Text>
                    <Text mb={4}>
                        <span className='font-semibold'>Old roads area: </span>
                        {spatialData.old_road} m<sup>2</sup>
                    </Text>
                    <Text mb={4}>
                        <span className='font-semibold'>Damaged areas: </span>
                        {spatialData.damage} m<sup>2</sup>
                    </Text>
                    <Text mb={4}>
                        <span className='font-semibold'>Water areas:</span>
                        {spatialData.water} m<sup>2</sup>
                    </Text>
                    <Text mb={4}>
                        <span className='font-semibold'>Methane area: </span>
                        {spatialData.methane} m<sup>2</sup>
                    </Text>
                    <Text mb={4}>
                        <span className='font-semibold'>
                            Unusued areas for agriculture:{' '}
                        </span>
                        {spatialData.agriculture} m<sup>2</sup>
                    </Text>
                </div>
            ) : (
                <div className=''>
                    There are no available data yet for this region.
                </div>
            )}
        </div>
    )
}

export default SatteliteTab
