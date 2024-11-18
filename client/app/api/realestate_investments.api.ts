import api from '@/app/api/axios'

const getHistoricalData = async (params: any) => {
    try {
        const res = await api.get(`/real-estate-investments/`, {
            params: {
                region: params.region,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const get5YearPrediction = async (params: any) => {
    try {
        const res = await api.get(`/real-estate-investments/forecast/`, {
            params: {
                region: params.region,
            },
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

export { getHistoricalData, get5YearPrediction }
