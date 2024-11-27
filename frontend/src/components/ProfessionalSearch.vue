<template>
    <div class="professional-search">
        <div class="container mt-4">
            <div class="row">
                <!-- Filters Section -->
                <div class="col-md-3">
                    <div class="card p-3">
                        <h5>Filters</h5>
                        <form @submit.prevent="applyFilters">
                            <div class="mb-3">
                                <label for="searchDate" class="form-label">Date</label>
                                <input type="date" id="searchDate" v-model="filters.date" class="form-control" />
                            </div>
                            <div class="mb-3">
                                <label for="searchLocation" class="form-label">Location Name</label>
                                <input type="text" id="searchLocation" v-model="filters.locationName"
                                    class="form-control" placeholder="Enter location name" />
                            </div>
                            <div class="mb-3">
                                <label for="searchPin" class="form-label">Pincode</label>
                                <input type="text" id="searchPin" v-model="filters.pincode" class="form-control"
                                    placeholder="Enter pincode" />
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Apply Filters</button>
                        </form>
                    </div>
                </div>

                <!-- Results Section -->
                <div class="col-md-9">
                    <h4>Closed Requests - Search Results</h4>
                    <table class="table table-striped table-hover mt-3">
                        <thead class="thead-dark">
                            <tr>
                                <th>ID</th>
                                <th>Customer Name</th>
                                <th>Contact Phone</th>
                                <th>Location (Pincode)</th>
                                <th>Date</th>
                                <th>Rating</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="service in filteredResults" :key="service.id">
                                <td>{{ service.id }}</td>
                                <td>{{ service.customerName }}</td>
                                <td>{{ service.contactPhone }}</td>
                                <td>{{ service.location }}</td>
                                <td>{{ service.date }}</td>
                                <td>
                                    <span :class="getRatingClass(service.rating)">
                                        {{ service.rating }}
                                    </span>
                                </td>
                            </tr>
                            <tr v-if="filteredResults.length === 0">
                                <td colspan="6" class="text-center">No results found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ProfessionalSearch",
    data() {
        return {
            services: [],
            filters: {
                date: "",
                locationName: "",
                pincode: "",
            },
        };
    },
    computed: {
        filteredResults() {
            return this.services.filter((service) => {
                const { date, locationName, pincode } = this.filters;
                const matchesDate = date ? service.date === date : true;
                const matchesLocation = locationName
                    ? service.location.toLowerCase().includes(locationName.toLowerCase())
                    : true;
                const matchesPincode = pincode
                    ? service.location.includes(pincode)
                    : true;

                return matchesDate && matchesLocation && matchesPincode;
            });
        },
    },
    methods: {
        applyFilters() {
            // For now, the computed property handles filtering.
            console.log("Filters applied:", this.filters);
        },
        getRatingClass(rating) {
            if (rating >= 4) return "text-success";
            if (rating >= 2) return "text-warning";
            return "text-danger";
        },
        async fetchServices() {
            try {
                const professionalId = this.$route.params.id;
                const response = await fetch(`http://localhost:5000/api/professionals/closed-service-requests/${professionalId}`);
                const data = await response.json();
                this.services = data.map(service => ({
                    id: service.id,
                    customerName: service.user.full_name,
                    contactPhone: service.user.email,
                    location: `${service.user.address}, ${service.user.pincode}`,
                    date: new Date(service.created_at).toISOString().split('T')[0],
                    rating: service.rating,
                }));
            } catch (error) {
                console.error("Error fetching services:", error);
                this.services = [];
            }
        }
    },
    mounted() {
        this.fetchServices();
    },
};
</script>

<style scoped>
thead.thead-dark {
    background-color: #343a40;
    color: white;
}

.card {
    border-radius: 8px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}

.text-success {
    font-weight: bold;
    color: #4caf50 !important;
}

.text-warning {
    font-weight: bold;
    color: #ffc107 !important;
}

.text-danger {
    font-weight: bold;
    color: #f44336 !important;
}
</style>