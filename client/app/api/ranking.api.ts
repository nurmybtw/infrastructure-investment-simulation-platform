import api from '@/app/api/axios'

const getRegionalSectorImportance = async (params: any) => {
    try {
        const res = await api.get(`/ranking/`, {
            params,
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getRegionalAutoSimulation = async (params: any) => {
    try {
        const res = await api.get(`/ranking/simulation/`, {
            params,
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getRegionalManualSimulation = async (params: any) => {
    try {
        const res = await api.post(`/ranking/simulation/manual/`, {
            ...params,
        })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

export {
    getRegionalSectorImportance,
    getRegionalAutoSimulation,
    getRegionalManualSimulation,
}
