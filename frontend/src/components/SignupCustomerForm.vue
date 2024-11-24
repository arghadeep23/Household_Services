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
        <button @click="$router.push('/login')" class="btn btn-secondary options">Already Registered? Proceed to
            Login</button>
    </div>
</template>

<script>
import { getApiUrl } from '../utils/api';
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
        async handleRegister() {
            // const userData = {
            //     email: this.email,
            //     password: this.password,
            //     name: this.name,
            //     address: this.address,
            //     pincode: this.pincode
            // };
            // console.log('User Data:', userData);
            // this.$router.push('/login');
            // Add your registration logic here
            console.log({
                email: this.email,
                password: this.password,
                full_name: this.name,
                address: this.address,
                pincode: this.pincode

            })
            try {
                const response = await fetch(`${getApiUrl()}/api/customer/signup`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                        full_name: this.name,
                        address: this.address,
                        pincode: this.pincode
                    })
                });
                if (response.ok) {
                    console.log('Registration successful');
                    const data = await response.json();
                    // set token in local storage
                    localStorage.setItem('customer', data.token);
                    this.$router.push(`/customer/${data.id}`); // Redirect to customer home
                } else {
                    console.log('Registration failed');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    }
};

</script>

<style src="../styles/SignupForm.css"></style>

<style scoped>
.options {
    margin-top: 10px;
}
</style>
