<template>
    <div class="professional-home">
        <div class="container mt-4">
            <!-- Profile Navigation -->
            <div class="d-flex justify-content-end mb-3">
                <router-link :to="`/professional/${professionalId}/profile`" class="btn btn-primary">
                    Go to Profile
                </router-link>
            </div>

            <!-- Today's Services Table -->
            <h4>Today's Services</h4>
            <table class="table table-striped table-hover">
                <thead class="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Location (Pincode)</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in todaysServices" :key="service.id">
                        <td>{{ service.id }}</td>
                        <td>{{ service.customerName }}</td>
                        <td>{{ service.location }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-success btn-sm custom-btn" @click="acceptService(service.id)"
                                    style="opacity: 0.9;">
                                    Accept
                                </button>
                                <button class="btn btn-danger btn-sm custom-btn" @click="rejectService(service.id)"
                                    style="opacity: 0.9;">
                                    Reject
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- Closed Services Table -->
            <h4 class="mt-5">Closed Services</h4>
            <table class="table table-striped table-hover">
                <thead class="thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Contact Phone</th>
                        <th>Location (Pincode)</th>
                        <th>Date</th>
                        <th>Rating (out of 5)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in closedServices" :key="service.id">
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
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: "ProfessionalHome",
    data() {
        return {
            professionalId: 1, // Replace with dynamic value when integrated with backend
            todaysServices: [
                {
                    id: 1,
                    customerName: "John Doe",
                    location: "123 Main St, 560001",
                },
                {
                    id: 2,
                    customerName: "Jane Smith",
                    location: "45 Elm St, 400012",
                },
            ],
            closedServices: [
                {
                    id: 10,
                    customerName: "Alice Brown",
                    contactPhone: "9876543210",
                    location: "789 Maple St, 700015",
                    date: "2024-11-22",
                    rating: 4,
                },
                {
                    id: 11,
                    customerName: "Bob White",
                    contactPhone: "8765432109",
                    location: "56 Oak St, 500004",
                    date: "2024-11-20",
                    rating: 5,
                },
            ],
        };
    },
    methods: {
        acceptService(serviceId) {
            alert(`Service ${serviceId} accepted!`);
            // Add API call or logic here
        },
        rejectService(serviceId) {
            alert(`Service ${serviceId} rejected!`);
            // Add API call or logic here
        },
        getRatingClass(rating) {
            if (rating >= 4) return "text-success";
            if (rating >= 2) return "text-warning";
            return "text-danger";
        },
    },
};
</script>
<style scoped>
thead.thead-dark {
    background-color: #343a40;
    color: white;
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

.custom-btn {
    margin-right: 10px;
    /* Add horizontal space between buttons */
}

.custom-btn:last-child {
    margin-right: 0;
    /* Remove margin from the last button */
}
</style>
