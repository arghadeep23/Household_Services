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
                            <td v-for="column in columns" :key="column">{{ item[column.toLowerCase()] }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
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
                customers: [
                    { id: 1, name: "Alice", email: "alice@example.com", address: "123 Main St", pincode: "123456" },
                    { id: 2, name: "Bob", email: "bob@example.com", address: "456 Oak St", pincode: "654321" },
                ],
                professionals: [
                    { id: 1, name: "John", serviceName: "Plumbing", status: "Approved" },
                    { id: 2, name: "Jane", serviceName: "Gardening", status: "Rejected" },
                ],
                services: [
                    { id: 1, name: "Plumbing", basePrice: 100, description: "General plumbing work." },
                    { id: 2, name: "Gardening", basePrice: 200, description: "Lawn care and maintenance." },
                ],
                serviceRequests: [
                    { id: 101, professional: "John", requestedDate: "2024-11-10", status: "Requested" },
                    { id: 102, professional: "Jane", requestedDate: "2024-11-15", status: "Closed" },
                ],
            },
        };
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
                services: ["ID", "Name", "Base Price", "Description"],
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