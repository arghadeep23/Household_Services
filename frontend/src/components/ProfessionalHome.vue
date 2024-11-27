<template>
    <div class="professional-home">
        <div class="container mt-4">
            <!-- Profile Navigation -->
            <div class="d-flex justify-content-end mb-3">
                <router-link :to="`/professional/${this.$route.params.id}/profile`" class="btn btn-primary">
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
                        <td>{{ service.user.full_name }}</td>
                        <td>{{ service.user.address + ', ' + service.user.pincode }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-success btn-sm custom-btn" @click="acceptService(service.id)"
                                    style="opacity: 0.9;">
                                    Accept
                                </button>
                                <!-- <button class="btn btn-danger btn-sm custom-btn" @click="rejectService(service.id)"
                                    style="opacity: 0.9;">
                                    Reject
                                </button> -->
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
                        <th>Contact Email</th>
                        <th>Location (Pincode)</th>
                        <th>Date</th>
                        <th>Rating (out of 5)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in closedServices" :key="service.id">
                        <td>{{ service.id }}</td>
                        <td>{{ service.user.full_name }}</td>
                        <td>{{ service.user.email }}</td>
                        <td>{{ service.user.address + '(' + service.user.pincode + ')' }}</td>
                        <td>{{ service.created_at }}</td>
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
import { getApiUrl } from "@/utils/api";
export default {
    name: "ProfessionalHome",
    data() {
        return {
            todaysServices: [],
            closedServices: [],
        };
    },
    created() {
        Promise.all([this.fetchTodayServices(), this.fetchClosedServices()])
            .then(() => {
                console.log('Fetched today and closed services successfully');
            })
            .catch(error => {
                console.error('Error fetching services:', error);
            });
        // this.fetchTodayServices();
        // this.fetchClosedServices();
    },
    methods: {
        async fetchClosedServices() {
            // Add API call or logic here
            const response = await fetch(`${getApiUrl()}/api//professionals/closed-service-requests/${this.$route.params.id}`);
            if (response.ok) {
                this.closedServices = await response.json();
            }
            else {
                console.error('Failed to fetch closed services');
            }
        },
        async acceptService(serviceId) {
            alert(`Service ${serviceId} accepted!`);
            try {
                const request_id = serviceId
                const response = await fetch(`${getApiUrl()}/api/service_requests/${request_id}/assign_professional`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ // Ensure the body is a JSON string
                        "professional_id": this.$route.params.id
                    }),
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log(result);
                    // alert(`Service ${serviceId} accepted!`);
                    // Uncomment the following line if you want to fetch updated services
                    this.fetchTodayServices();
                } else {
                    const error = await response.json();
                    alert(`Failed to accept service ${serviceId}: ${error.error || 'Unknown error'}`);
                }
            } catch (err) {
                console.error("Error during API call:", err);
                alert(`An error occurred: ${err.message}`);
            }
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
        async fetchTodayServices() {
            const professionalId = this.$route.params.id;
            const response = await fetch(`${getApiUrl()}/api/professionals/service-requests/${professionalId}`);
            if (response.ok) {
                this.todaysServices = await response.json();
            }
            else {
                console.error('Failed to fetch today services');
            }
        }
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
