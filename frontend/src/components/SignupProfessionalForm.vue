<template>
  <div class="signup-form">
    <h2>Professional Signup</h2>
    <form @submit.prevent="handleSignUp">
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" placeholder="Enter your email" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" placeholder="Enter your password" />
      </div>
      <div class="form-group">
        <label for="name">Full Name</label>
        <input type="text" id="name" v-model="name" placeholder="Enter your full name" />
      </div>
      <div class="form-group">
        <label for="service">Service</label>
        <select id="service" v-model="service_id">
          <option v-for="service in services" :key="service.id" :value="service.id">{{ service.service_name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="experience">Experience (Years)</label>
        <input type="number" id="experience" v-model="experience" min="0" />
      </div>
      <div class="form-group">
        <label for="document">Attach Document (PDF)</label>
        <input type="file" id="document" accept="application/pdf" @change="validateFile" />
        <div v-if="fileError" class="alert alert-danger mt-3">{{ fileError }}</div>
      </div>
      <div class="form-group">
        <label for="address">Address</label>
        <input type="text" id="address" v-model="address" placeholder="Enter your address" />
      </div>
      <div class="form-group">
        <label for="pincode">Pin Code</label>
        <input type="text" id="pincode" v-model="pincode" placeholder="Enter your pin code" />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <button @click="$router.push('/login')" class="btn btn-secondary options">Already Registered ? Proceed to
      Login</button>
  </div>
</template>

<script>
import { getApiUrl } from '../utils/api';

export default {
  name: "SignupProfessionalForm",
  data() {
    return {
      email: '',
      password: '',
      name: '',
      service_id: '',
      services: [],
      experience: '',
      address: '',
      pincode: '',
      file: null,
      fileError: null,
    };
  },
  created() {
    this.fetchServices();
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
        console.error('Error:', error);
      }
    },
    validateFile(event) {
      const file = event.target.files[0];
      if (!file) {
        this.fileError = "Please select a file.";
        return;
      }
      if (file.type !== "application/pdf") {
        this.fileError = "Please select a PDF file.";
        return;
      }
      this.fileError = null;
      this.file = file;
    },
    async handleSignUp() {
      if (!this.file) {
        this.fileError = "Please attach a document.";
        return;
      }

      try {
        const formData = new FormData();
        formData.append('file', this.file);
        formData.append('cloud_name', 'dnfmbxrli');
        formData.append('upload_preset', 'arghaCloud');

        const uploadResponse = await fetch('https://api.cloudinary.com/v1_1/dnfmbxrli/image/upload', {
          method: 'POST',
          body: formData
        });

        const uploadData = await uploadResponse.json();

        const response = await fetch(`${getApiUrl()}/api/professional/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            full_name: this.name,
            service_id: this.service_id, // Send the service ID to the backend
            experience: this.experience,
            address: this.address,
            pincode: this.pincode,
            document_url: uploadData.url,
            cover_photo_url: null
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.log('Error:', errorData);
          return;
        }

        const data = await response.json();
        // setting the token and other details in local storage
        localStorage.setItem('professional', data.token);
        localStorage.setItem('professional_id', data.professional_id);
        localStorage.setItem('professional_service_id', data.service_id);
        // redirecting to the dashboard
        this.$router.push(`/professional/${data.professional_id}`);
      } catch (error) {
        this.fileError = 'An error occurred while signing up. Please try again.';
      }
    }
  }
};
</script>

<style src="../styles/SignupForm.css"></style>

<style scoped>
.options {
  margin-top: 1rem;
}
</style>
