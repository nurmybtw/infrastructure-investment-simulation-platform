import api from '@/app/api/axios'

const getCountryRating = async () => {
    try {
        const res = await api.get(`/rating/country/`, {})
        return res.data
    } catch (err) {
        console.log(err)
    }
}

const getRegionRating = async (region: any) => {
    try {
        const res = await api.get(`/rating/region/`, { params: { region } })
        return res.data
    } catch (err) {
        console.log(err)
    }
}

export { getCountryRating, getRegionRating }
