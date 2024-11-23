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
          <td>{{ service.name }}</td>
          <td>{{ service.basePrice }}</td>
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
          <td>{{ professional.name }}</td>
          <td>{{ professional.experience }}</td>
          <td>{{ professional.serviceName }}</td>
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
          <td>{{ request.professional || 'Not Assigned' }}</td>
          <td>{{ request.requestedDate }}</td>
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
export default {
  name: "AdminHome",
  components: { ServiceDetailsModal, ProfessionalDetailsModal, CreateServiceModal },
  data() {
    return {
      services: [
        { id: 1, name: "Plumbing", basePrice: 100 },
        { id: 2, name: "Gardening", basePrice: 200 },
        { id: 3, name: "Electrician", basePrice: 150 },
      ],
      selectedService: null,
      professionals: [
        {
          id: 1,
          name: "John Doe",
          experience: 5,
          serviceName: "Plumbing",
          email: "john.doe@example.com",
          address: "123 Main St, Springfield",
          pincode: "123456",
          document: "resume-john.pdf",
        },
        {
          id: 2,
          name: "Jane Smith",
          experience: 3,
          serviceName: "Gardening",
          email: "jane.smith@example.com",
          address: "456 Oak Lane, Gotham",
          pincode: "654321",
          document: "resume-jane.pdf",
        },
      ],
      serviceRequests: [
        {
          id: 101,
          professional: "John Doe",
          requestedDate: "2024-11-01",
          status: "Requested",
        },
        {
          id: 102,
          professional: null,
          requestedDate: "2024-11-05",
          status: "Accepted",
        },
        {
          id: 103,
          professional: "Jane Smith",
          requestedDate: "2024-11-10",
          status: "Closed",
        },
      ],
      selectedProfessional: null,
      showCreateServiceModal: false,
    };
  },
  methods: {
    viewServiceDetails(service) {
      this.selectedService = { ...service, description: "", subservices: [] };
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
    saveNewService(service) {
      const newService = { ...service, id: this.services.length + 1 };
      this.services.push(newService);
      this.showCreateServiceModal = false; // Close the modal
    },
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