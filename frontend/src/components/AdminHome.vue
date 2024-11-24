<template>
  <div class="container mt-5">
    <h1 class="mb-4">Services</h1>
    <button class="btn btn-success mb-4" @click="openCreateServiceModal">
      Create New Service
    </button>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Service ID</th>
          <th>Service Name</th>
          <th>Base Price</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>
            <a href="#" @click.prevent="viewServiceDetails(service)">{{ service.id }}</a>
          </td>
          <td>{{ service.service_name }}</td>
          <td>{{ service.base_price }}</td>
          <td>
            <button class="btn btn-primary btn-sm" @click="editService(service)">
              Edit
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h1 class="mb-4 mt-4">Professionals</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Professional ID</th>
          <th>Name</th>
          <th>Experience (Years)</th>
          <th>Service</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in professionals" :key="professional.id">
          <td>
            <a href="#" @click.prevent="viewProfessionalDetails(professional)">
              {{ professional.id }}
            </a>
          </td>
          <td>{{ professional.full_name }}</td>
          <td>{{ professional.experience }}</td>
          <td>{{ professional.service }}</td>
          <td>
            <div class="btn-group" role="group">
              <button class="btn btn-success btn-sm custom-btn" @click="approveProfessional(professional)">
                Approve
              </button>
              <button class="btn btn-warning btn-sm custom-btn" @click="rejectProfessional(professional)">
                Reject
              </button>
              <button class="btn btn-danger btn-sm custom-btn" @click="deleteProfessional(professional.id)">
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <h1 class="mb-4 mt-4">Service Requests</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Request ID</th>
          <th>Assigned Professional</th>
          <th>Requested Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in serviceRequests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ request.professional_id || 'Not Assigned' }}</td>
          <td>{{ request.created_at }}</td>
          <td>
            <span :class="{
              'badge bg-primary': request.status === 'Requested',
              'badge bg-success': request.status === 'Accepted',
              'badge bg-secondary': request.status === 'Closed',
            }">
              {{ request.status }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Modal -->
    <!-- Modal for Professional Details -->
    <ProfessionalDetailsModal v-if="selectedProfessional" :professional="selectedProfessional"
      @close="selectedProfessional = null" />
    <ServiceDetailsModal v-if="selectedService" :service="selectedService" @close="selectedService = null"
      @save="saveServiceDetails" />
    <CreateServiceModal v-if="showCreateServiceModal" @close="showCreateServiceModal = false" @save="saveNewService" />
  </div>
</template>
<script>
import ServiceDetailsModal from "@/components/ServiceDetailsModal.vue";
import ProfessionalDetailsModal from "@/components/ProfessionalDetailsModal.vue";
import CreateServiceModal from "@/components/CreateServiceModal.vue";
import { getApiUrl } from "@/utils/api";

export default {
  name: "AdminHome",
  components: { ServiceDetailsModal, ProfessionalDetailsModal, CreateServiceModal },
  data() {
    return {
      services: [],
      selectedService: null,
      professionals: [],
      serviceRequests: [],
      selectedProfessional: null,
      showCreateServiceModal: false,
    };
  },
  created() {
    this.fetchServices();
    this.fetchProfessionals();
    this.fetchServiceRequests();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch(`${getApiUrl()}/api/services`);
        if (response.ok) {
          this.services = await response.json();
        } else {
          console.error('Failed to fetch services');
        }
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    async fetchProfessionals() {
      try {
        const response = await fetch(`${getApiUrl()}/api/professionals`);
        if (response.ok) {
          this.professionals = await response.json();
        } else {
          console.error('Failed to fetch professionals');
        }
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    },
    async fetchServiceRequests() {
      try {
        const response = await fetch(`${getApiUrl()}/api/service_requests`);
        if (response.ok) {
          this.serviceRequests = await response.json();
        } else {
          console.error('Failed to fetch service requests');
        }
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },
    viewServiceDetails(service) {
      this.selectedService = { ...service };
    },
    editService(service) {
      this.viewServiceDetails(service); // Reuse the same logic for now
    },
    saveServiceDetails(updatedService) {
      const index = this.services.findIndex((s) => s.id === updatedService.id);
      if (index !== -1) this.services.splice(index, 1, updatedService);
      this.selectedService = null; // Close the modal
    },
    // View Professional Details
    viewProfessionalDetails(professional) {
      this.selectedProfessional = professional;
    },

    // Approve Professional
    approveProfessional(professional) {
      alert(`Professional ${professional.name} has been approved!`);
      // Logic to approve professional (e.g., API call) goes here
    },

    // Reject Professional
    rejectProfessional(professional) {
      alert(`Professional ${professional.name} has been rejected!`);
      // Logic to reject professional (e.g., API call) goes here
    },

    // Delete Professional
    deleteProfessional(id) {
      const confirmDelete = confirm("Are you sure you want to delete this professional?");
      if (confirmDelete) {
        this.professionals = this.professionals.filter((professional) => professional.id !== id);
        alert("Professional has been deleted.");
      }
    },
    openCreateServiceModal() {
      this.showCreateServiceModal = true;
    },
    async saveNewService(service) {
      console.log("Received service data in parent component:", service);
      try {
        const response = await fetch(`${getApiUrl()}/api/services`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            service_name: service.name,
            description: service.description,
            base_price: service.basePrice,
            subservices: service.subservices
          })
        });
        if (response.ok) {
          console.log('Service created successfully');
          // Add any additional logic here, like updating the list of services
        } else {
          console.log('Failed to create service');
        }
      } catch (error) {
        console.error('Error:', error);
      }
      this.showCreateServiceModal = false; // Close modal after save attempt
    }
  },
};
</script>

<style scoped>
.custom-btn {
  margin-right: 10px;
  /* Add horizontal space between buttons */
  opacity: 0.8;
  /* Change opacity for a minimalistic look */
}

.custom-btn:last-child {
  margin-right: 0;
  /* Remove margin from the last button */
}

.custom-btn:hover {
  opacity: 1;
  /* Restore full opacity on hover */
}
</style>