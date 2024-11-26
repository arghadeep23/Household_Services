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
                        <h5 class="card-title">{{ service.service_name }}</h5>
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
                        <h5 class="modal-title">{{ selectedService?.service_name }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Description:</strong> {{ selectedService?.description }}</p>
                        <p><strong>Base Price:</strong> ₹{{ selectedService?.base_price }}</p>
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
                                    <td>₹{{ subservice.basePrice }}</td>
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
                    <th>Email</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in serviceHistory" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.service_name }}</td>
                    <td>{{ service.professional_name }}</td>
                    <td>{{ service.professional_email }}</td>
                    <td>
                        <span v-if="service.status !== 'Accepted'">{{ service.status }}</span>
                        <button v-else class=" btn btn-outline-primary btn-sm" @click="closeService(service)">
                            Accepted | Close It
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
                        <p><strong>Service Name:</strong> {{ closingService?.service_name }}</p>
                        <p><strong>Service Request ID:</strong> {{ closingService?.id }}</p>
                        <p><strong>Description:</strong> {{ closingService?.service_description }}</p>
                        <p><strong>Creation Date:</strong> {{ closingService?.created_at }}</p>
                        <p><strong>Professional ID:</strong> {{ closingService?.professional_id }}</p>
                        <p><strong>Professional Name:</strong> {{ closingService?.professional_name }}</p>
                        <p><strong>Contact:</strong> {{ closingService?.professional_email }}</p>
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
import { getApiUrl } from '@/utils/api';

export default {
    name: 'CustomerHome',
    data() {
        return {
            services: [],
            selectedService: null,
            selectedSubservices: [],
            serviceHistory: [],
            closingService: null,
            rating: 0,
            remarks: '',
            customerId: this.$route.params.id
        };
    },
    created() {
        this.fetchOpenServices();
        this.fetchServiceRequests();
    },
    methods: {
        async fetchOpenServices() {
            try {
                const response = await fetch(`${getApiUrl()}/api/services/open`);
                if (response.ok) {
                    this.services = await response.json();
                } else {
                    console.error('Failed to fetch open services');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
        async fetchServiceRequests() {
            const customerId = this.$route.params.id;
            try {
                const response = await fetch(`${getApiUrl()}/api/service_requests/customer/${customerId}`);
                if (response.ok) {
                    this.serviceHistory = await response.json();
                } else {
                    console.error('Failed to fetch service requests');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
        goToProfile() {
            this.$router.push(`/customer/${this.$route.params.id}/profile`);
        },
        viewServiceDetails(service) {
            this.selectedService = service;
            const modal = new Modal(document.getElementById('serviceDetailsModal'));
            modal.show();
        },
        proceedWithServices() {
            console.log('Selected subservices:', this.selectedSubservices);
            console.log('Selected service:', this.selectedService);
            // creating a new service request
            const customerId = this.$route.params.id;
            const response = fetch(`${getApiUrl()}/api/service_requests`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: customerId,
                    service_id: this.selectedService.id,
                    selected_subservices: this.selectedSubservices,
                }),
            });
            if (response.ok) {
                console.log('Service request created successfully');
                this.fetchServiceRequests();
            } else {
                console.error('Failed to create service request');
            }
        },
        closeService(service) {
            console.log('Closing service:', service);
            this.closingService = service;
            const modal = new Modal(document.getElementById('closeServiceModal'));
            modal.show();
        },
        async submitRating() {
            console.log('Rating submitted:', {
                rating: this.rating,
                remarks: this.remarks,
                service: this.closingService,
            });
            // create a service remark 
            try {
                const response = await fetch(`${getApiUrl()}/api/service_remarks`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        service_request_id: this.closingService.id,
                        professional_id: this.closingService.professional_id,
                        user_id: this.$route.params.id,
                        service_description: this.closingService.service_description,
                        rating: this.rating,
                        user_remark: this.remarks,
                        professional_contact: this.closingService.professional_email
                    }),
                });
                if (response.ok) {
                    console.log('Service remark submitted successfully');
                } else {
                    console.error('Failed to submit service remark');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
    },
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
