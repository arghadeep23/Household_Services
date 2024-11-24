<template>
  <div class="login-form">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="role">Role:</label>
        <select v-model="role" id="role" class="form-control" required>
          <option value="Customer">Customer</option>
          <option value="Professional">Professional</option>
          <option value="Admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Login</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { getApiUrl } from '../utils/api';

export default {
  data() {
    return {
      email: '',
      password: '',
      role: 'Customer',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch(`${getApiUrl()}/api/sso/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            role: this.role
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.errorMessage = errorData.error;
          return;
        }

        const data = await response.json();
        const id = data.entity.id;
        if (this.role === 'Customer') {
          localStorage.setItem('customer', JSON.stringify(data.token));
        } else if (this.role === 'Professional') {
          localStorage.setItem('professional', JSON.stringify(data.token));
        } else if (this.role === 'Admin') {
          localStorage.setItem('admin', JSON.stringify(data.token));
        }
        // Navigate to the appropriate page based on the role
        if (this.role === 'Customer') {
          this.$router.push(`/customer/${id}`);
        } else if (this.role === 'Professional') {
          this.$router.push(`/professional/${id}`);
        } else if (this.role === 'Admin') {
          this.$router.push('/admin');
        }
      } catch (error) {
        this.errorMessage = 'An error occurred while logging in. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
.error-message {
  color: red;
}
</style>