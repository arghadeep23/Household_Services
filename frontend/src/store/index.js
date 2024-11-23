import { createStore } from 'vuex'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

export default createStore({
    state: {
        services: []
    },
    mutations: {
        SET_SERVICES(state, services) {
            state.services = services
        },
        ADD_SERVICE(state, service) {
            state.services.push(service)
        },
        UPDATE_SERVICE(state, updatedService) {
            const index = state.services.findIndex(s => s.id === updatedService.id)
            if (index !== -1) {
                state.services.splice(index, 1, updatedService)
            }
        },
        DELETE_SERVICE(state, serviceId) {
            state.services = state.services.filter(s => s.id !== serviceId)
        }
    },
    actions: {
        async fetchServices({ commit }) {
            try {
                const response = await axios.get(`${API_URL}/services`)
                commit('SET_SERVICES', response.data)
            } catch (error) {
                console.error('Error fetching services:', error)
            }
        },
        async createService({ commit }, serviceData) {
            try {
                const response = await axios.post(`${API_URL}/services`, serviceData)
                commit('ADD_SERVICE', response.data)
            } catch (error) {
                console.error('Error creating service:', error)
            }
        },
        async updateService({ commit }, { id, serviceData }) {
            try {
                const response = await axios.put(`${API_URL}/services/${id}`, serviceData)
                commit('UPDATE_SERVICE', response.data)
            } catch (error) {
                console.error('Error updating service:', error)
            }
        },
        async deleteService({ commit }, serviceId) {
            try {
                await axios.delete(`${API_URL}/services/${serviceId}`)
                commit('DELETE_SERVICE', serviceId)
            } catch (error) {
                console.error('Error deleting service:', error)
            }
        }
    },
    modules: {
    }
})