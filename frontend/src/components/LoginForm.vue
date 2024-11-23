<template>
  <div class="login-form">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" placeholder="Enter your email" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" placeholder="Enter your password" />
      </div>
      <div class="form-group">
        <label for="role">Role</label>
        <select id="role" v-model="role" class="form-control">
          <option value="customer">Customer</option>
          <option value="service_professional">Service Professional</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    </form>
    <div class="options">
      <button @click="$router.push('/signup-professional')" class="btn btn-secondary">
        Register as Professional
      </button>
      <button @click="$router.push('/signup-customer')" class="btn btn-secondary">
        Register as Customer
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      email: '',
      password: '',
      role: 'customer',
      error: null
    };
  },
  methods: {
    handleLogin() {
      // Placeholder for login logic
      console.log({
        email: this.email,
        password: this.password,
        role: this.role
      });

      // Simulate login failure
      this.error = "Invalid login credentials. Please try again.";
    }
  }
};
</script>

<style src="../styles/LoginForm.css"></style>