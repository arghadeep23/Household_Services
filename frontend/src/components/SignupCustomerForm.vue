<template>
    <div class="signup-form">
        <h2>Customer Signup</h2>
        <form @submit.prevent="handleRegister">
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
                <label for="address">Address</label>
                <input type="text" id="address" v-model="address" placeholder="Enter your address" />
            </div>
            <div class="form-group">
                <label for="pincode">Pin Code</label>
                <input type="text" id="pincode" v-model="pincode" placeholder="Enter your pin code" />
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
        <button @click="$router.push('/login')" class="btn btn-secondary">Already Registered? Proceed to Login</button>
    </div>
</template>

<script>
export default {
    name: "SignupCustomerForm",
    data() {
        return {
            email: '',
            password: '',
            name: '',
            address: '',
            pincode: ''
        };
    },
    methods: {
        handleRegister() {
            const userData = {
                email: this.email,
                password: this.password,
                name: this.name,
                address: this.address,
                pincode: this.pincode
            };
            console.log('User Data:', userData);
            this.$router.push('/login');
            // Add your registration logic here
        }
    }
};
</script>

<style src="../styles/SignupForm.css"></style>
