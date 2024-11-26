<template>
    <div class="admin-search">
        <div class="row">
            <!-- Sidebar for Filters -->
            <div class="col-md-3 bg-light p-3">
                <h4>Search Filters</h4>
                <div class="mb-4">
                    <label for="entitySelect" class="form-label">Search By</label>
                    <select v-model="selectedEntity" id="entitySelect" class="form-select">
                        <option value="customers">Customers</option>
                        <option value="professionals">Professionals</option>
                        <option value="services">Services</option>
                        <option value="serviceRequests">Service Requests</option>
                    </select>
                </div>
                <!-- Dynamic Filters -->
                <div v-if="selectedEntity === 'professionals'" class="mb-4">
                    <h5>Professional Filters</h5>
                    <div class="form-check">
                        <input type="checkbox" id="approvedFilter" v-model="filters.approved"
                            class="form-check-input" />
                        <label for="approvedFilter" class="form-check-label">Approved</label>
                    </div>
                    <div class="form-check">
                        <input type="checkbox" id="rejectedFilter" v-model="filters.rejected"
                            class="form-check-input" />
                        <label for="rejectedFilter" class="form-check-label">Rejected</label>
                    </div>
                </div>
                <div v-if="selectedEntity === 'serviceRequests'" class="mb-4">
                    <h5>Service Request Filters</h5>
                    <select v-model="filters.status" class="form-select">
                        <option value="">All</option>
                        <option value="Requested">Requested</option>
                        <option value="Accepted">Accepted</option>
                        <option value="Closed">Closed</option>
                    </select>
                </div>
            </div>

            <!-- Main Content Area -->
            <div class="col-md-9 p-3">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h4>{{ entityDisplayName }} List</h4>
                    <input type="text" v-model="searchQuery" placeholder="Search..." class="form-control w-50" />
                </div>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th v-for="column in columns" :key="column">{{ column }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in filteredResults" :key="item.id">
                            <td v-for="column in columns" :key="column">{{ getItemValue(item, column) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import { getApiUrl } from '../utils/api';

export default {
    name: "AdminSearch",
    data() {
        return {
            selectedEntity: "customers", // Default entity
            searchQuery: "",
            filters: {
                approved: false,
                rejected: false,
                status: "", // For service requests
            },
            entities: {
                customers: [],
                professionals: [],
                services: [],
                serviceRequests: [],
            },
        };
    },
    created() {
        this.fetchAllData();
    },
    methods: {
        async fetchAllData() {
            try {
                const [customers, professionals, services, serviceRequests] = await Promise.all([
                    fetch(`${getApiUrl()}/api/users`).then(res => res.json()),
                    fetch(`${getApiUrl()}/api/professionals`).then(res => res.json()),
                    fetch(`${getApiUrl()}/api/services`).then(res => res.json()),
                    fetch(`${getApiUrl()}/api/service_requests`).then(res => res.json())
                ]);

                this.entities.customers = customers;
                this.entities.professionals = professionals;
                this.entities.services = services;
                this.entities.serviceRequests = serviceRequests;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        getItemValue(item, column) {
            const columnMapping = {
                "Name": "full_name",
                "Service Name": "service_name",
                "Base Price": "base_price",
                "Assigned Professional": "assigned_professional",
                "Requested Date": "created_at",
                "Status": "status",
                "Email": "email",
                "Address": "address",
                "Pincode": "pincode",
                "ID": "id"
            };
            return item[columnMapping[column]] || item[column.toLowerCase()];
        }
    },
    computed: {
        entityDisplayName() {
            const names = {
                customers: "Customer",
                professionals: "Professional",
                services: "Service",
                serviceRequests: "Service Request",
            };
            return names[this.selectedEntity];
        },
        columns() {
            const columnMapping = {
                customers: ["ID", "Name", "Email", "Address", "Pincode"],
                professionals: ["ID", "Name", "Service Name", "Status"],
                services: ["ID", "Service Name", "Base Price", "Description"],
                serviceRequests: ["ID", "Assigned Professional", "Requested Date", "Status"],
            };
            return columnMapping[this.selectedEntity];
        },
        filteredResults() {
            let data = this.entities[this.selectedEntity];
            // Filter by search query
            if (this.searchQuery) {
                data = data.filter((item) =>
                    Object.values(item).some((value) =>
                        String(value).toLowerCase().includes(this.searchQuery.toLowerCase())
                    )
                );
            }
            // Apply additional filters
            if (this.selectedEntity === "professionals") {
                if (this.filters.approved) {
                    data = data.filter((item) => item.status === "Approved");
                }
                if (this.filters.rejected) {
                    data = data.filter((item) => item.status === "Rejected");
                }
            } else if (this.selectedEntity === "serviceRequests") {
                if (this.filters.status) {
                    data = data.filter((item) => item.status === this.filters.status);
                }
            }
            return data;
        },
    },
};
</script>

<style scoped>
.options {
    margin-top: 1rem;
}
</style>