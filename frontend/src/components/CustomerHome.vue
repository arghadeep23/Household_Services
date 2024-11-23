<template>
    <div class="customer-home container mt-4">
        <!-- Profile Button -->
        <div class="d-flex justify-content-end mb-3">
            <router-link :to="`/customer/${customerId}/profile`" class="btn btn-primary">
                Go to Profile
            </router-link>
        </div>

        <!-- Service Cards -->
        <h3 class="mt-3">Available Services</h3>
        <div class="row g-4">
            <div v-for="service in services" :key="service.id" class="col-md-4">
                <div class="card service-card">
                    <div class="card-body">
                        <h5 class="card-title">{{ service.name }}</h5>
                        <p class="card-text">{{ service.description }}</p>
                        <button class="btn btn-outline-primary" @click="viewServiceDetails(service)">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Service Details Modal -->
        <div class="modal fade" id="serviceDetailsModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ selectedService?.name }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Description:</strong> {{ selectedService?.description }}</p>
                        <p><strong>Base Price:</strong> ₹{{ selectedService?.basePrice }}</p>
                        <h6>Subservices</h6>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Price</th>
                                    <th>Select</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="subservice in selectedService?.subservices || []" :key="subservice.id">
                                    <td>{{ subservice.name }}</td>
                                    <td>₹{{ subservice.price }}</td>
                                    <td>
                                        <input type="checkbox" :value="subservice" v-model="selectedSubservices" />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" @click="proceedWithServices" data-bs-dismiss="modal">
                            Proceed
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Service History Table -->
        <h3 class="mt-5">Service History</h3>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Service Name</th>
                    <th>Professional Name</th>
                    <th>Phone Number</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in serviceHistory" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.name }}</td>
                    <td>{{ service.professionalName }}</td>
                    <td>{{ service.phone }}</td>
                    <td>
                        <span v-if="service.status !== 'Assigned'">{{ service.status }}</span>
                        <button v-else class="btn btn-outline-primary btn-sm" @click="closeService(service)">
                            Close It
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- Close Service Modal -->
        <div class="modal fade" id="closeServiceModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Rate Service</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Service Name:</strong> {{ closingService?.name }}</p>
                        <p><strong>Service ID:</strong> {{ closingService?.id }}</p>
                        <p><strong>Description:</strong> {{ closingService?.description }}</p>
                        <p><strong>Creation Date:</strong> {{ closingService?.creationDate }}</p>
                        <p><strong>Professional ID:</strong> {{ closingService?.professionalId }}</p>
                        <p><strong>Professional Name:</strong> {{ closingService?.professionalName }}</p>
                        <p><strong>Contact:</strong> {{ closingService?.phone }}</p>
                        <h6>Rate the Service</h6>
                        <div class="rating">
                            <span v-for="n in 5" :key="n" class="star" :class="{ selected: n <= rating }"
                                @click="rating = n">★</span>
                        </div>
                        <textarea class="form-control mt-3" rows="3" placeholder="Add your remarks here"
                            v-model="remarks"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" @click="submitRating" data-bs-dismiss="modal">
                            Submit
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { Modal } from 'bootstrap';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
export default {
    name: 'CustomerHome',
    customerId: 1,
    data() {
        return {
            services: [{ id: 1, name: "Plumbing", description: "Fixing leaks and pipes.", basePrice: 500, subservices: [{ id: 101, name: "Leak Repair", price: 300 }, { id: 102, name: "Pipe Replacement", price: 800 },], }, { id: 2, name: "Electrical", description: "Electrical installations and repairs.", basePrice: 700, subservices: [{ id: 201, name: "Wiring", price: 500 }, { id: 202, name: "Lighting Installation", price: 1000 },], }, { id: 3, name: "Gardening", description: "Lawn and garden maintenance.", basePrice: 400, subservices: [{ id: 301, name: "Lawn Mowing", price: 200 }, { id: 302, name: "Hedge Trimming", price: 300 },], }, { id: 4, name: "Painting", description: "House and office painting services.", basePrice: 1200, subservices: [{ id: 401, name: "Interior Painting", price: 1500 }, { id: 402, name: "Exterior Painting", price: 2000 },], }, { id: 5, name: "Cleaning", description: "Residential and commercial cleaning services.", basePrice: 600, subservices: [{ id: 501, name: "Deep Cleaning", price: 800 }, { id: 502, name: "Carpet Cleaning", price: 600 },], },], selectedService: null, selectedSubservices: [], serviceHistory: [{ id: 201, name: "Cleaning", professionalName: "John Smith", phone: "9876543210", status: "Assigned", description: "Kitchen Cleaning", creationDate: "2024-11-15", professionalId: "P101", }, { id: 202, name: "Electrical", professionalName: "Jane Doe", phone: "1234567890", status: "Completed", description: "Wiring Installation", creationDate: "2024-10-25", professionalId: "P102", }, { id: 203, name: "Plumbing", professionalName: "Robert Brown", phone: "1122334455", status: "Pending", description: "Pipe Replacement", creationDate: "2024-11-18", professionalId: "P103", }, { id: 204, name: "Gardening", professionalName: "Emily Green", phone: "5566778899", status: "In Progress", description: "Lawn Mowing", creationDate: "2024-11-20", professionalId: "P104", }, { id: 205, name: "Painting", professionalName: "Michael White", phone: "6677889900", status: "Completed", description: "Interior Painting", creationDate: "2024-11-22", professionalId: "P105", },],
            closingService: null,
            rating: 0,
            remarks: "",
        };
    },
    methods: { goToProfile() { this.$router.push(`/customer/${this.$route.params.id}/profile`); }, viewServiceDetails(service) { this.selectedService = service; const modal = new Modal(document.getElementById("serviceDetailsModal")); modal.show(); }, proceedWithServices() { console.log("Selected subservices:", this.selectedSubservices); }, closeService(service) { this.closingService = service; const modal = new Modal(document.getElementById("closeServiceModal")); modal.show(); }, submitRating() { console.log("Rating submitted:", { rating: this.rating, remarks: this.remarks, service: this.closingService, }); }, },
};
</script>
<style scoped>
.service-card {
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    cursor: pointer;
}

.rating {
    display: flex;
    gap: 5px;
    font-size: 24px;
}

.star {
    cursor: pointer;
    color: #ccc;
}

.star.selected {
    color: #ffd700;
}

/* Custom styling for the profile button container */
.profile-button-container {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1030;
    /* Ensure it is above other content */
}
</style>
