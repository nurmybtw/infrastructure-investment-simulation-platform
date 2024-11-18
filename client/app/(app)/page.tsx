import React from 'react'
import Stats from './components/Stats'
import { Title } from '@mantine/core'

const page = () => {
    return (
        <div className='w-screen h-screen flex flex-col bg-slate-100 p-5 overflow-x-hidden'>
            <div className='text-2xl font-semibold mb-5 flex-none'>
                Datathon'24
            </div>
            <div className='flex-grow overflow-auto flex flex-col'>
                <Stats />
            </div>
        </div>
    )
}

export default page
