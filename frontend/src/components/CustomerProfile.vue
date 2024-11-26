<template>
    <div class="customer-profile container mt-4">
        <h3 class="text-center mb-4">Customer Profile</h3>

        <div class="card p-4 mx-auto">
            <form @submit.prevent="saveProfile">
                <!-- Name -->
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" id="name" class="form-control" v-model="profile.full_name"
                        :disabled="!isEditing" />
                </div>

                <!-- Email -->
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" id="email" class="form-control" v-model="profile.email"
                        :disabled="!isEditing" />
                </div>

                <!-- Pincode -->
                <div class="mb-3">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input type="text" id="pincode" class="form-control" v-model="profile.pincode"
                        :disabled="!isEditing" />
                </div>

                <!-- Address -->
                <div class="mb-3">
                    <label for="address" class="form-label">Address</label>
                    <textarea id="address" class="form-control" rows="2" v-model="profile.address"
                        :disabled="!isEditing"></textarea>
                </div>

                <!-- Action Buttons -->
                <div class="d-flex justify-content-end">
                    <button type="button" class="btn btn-warning me-2" @click="toggleEdit" v-if="!isEditing">
                        Edit
                    </button>

                    <button type="submit" class="btn btn-success" v-if="isEditing">
                        Save Changes
                    </button>
                    <button type="button" class="btn btn-secondary cancel-button" @click="cancelEdit" v-if="isEditing">
                        Cancel
                    </button>

                </div>
            </form>
            <div v-if="errorMessages.profile">
                <div class="alert alert-danger mt-3">{{ errorMessages.profile }}</div>
            </div>
        </div>
    </div>
</template>

<script>
import { getApiUrl } from '@/utils/api';
export default {
    name: "CustomerProfile",
    data() {
        return {
            isEditing: false,
            profile: {},
            errorMessages: {
                profile: null,
            },
        };
    },
    created() {
        this.fetchProfile();
    },
    methods: {
        toggleEdit() {
            this.isEditing = true;
        },
        cancelEdit() {
            this.isEditing = false;
        },
        async saveProfile() {
            // Simulate saving changes to the backend
            const customerId = this.$route.params.id;
            const response = await fetch(`${getApiUrl()}/api/users/${customerId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.profile),
            });
            if (response.ok) {
                console.log('Profile updated successfully');
                this.isEditing = false;
            } else {
                console.error('Failed to update profile');
                this.errorMessages.profile = 'Failed to update profile';
            }
            this.isEditing = false;

        },
        async fetchProfile() {
            // Simulate fetching profile data from the backend
            const customerId = this.$route.params.id;
            if (!customerId || customerId === 'undefined') {
                console.error('Customer ID not found');
                // proceed to login 
                this.$router.push('/login');
            }
            const response = await fetch(`${getApiUrl()}/api/users/${customerId}`);
            const data = await response.json();
            if (response.ok) {
                this.profile = data;
            } else {
                console.error('Failed to fetch customer profile');
                // error message 
                this.errorMessages.profile = 'Failed to fetch customer profile';
            }
        }
    },
};
</script>

<style scoped>
.customer-profile {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.card {
    border-radius: 8px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    max-width: 600px;
    width: 100%;
}

h3 {
    font-weight: bold;
    color: #333;
}

.btn {
    min-width: 100px;
    height: 40px;
    line-height: 1.5;
}

.d-flex {
    display: flex;
    gap: 10px;
    /* width: auto; */
    /* Add gap between buttons */
}

.d-flex2 {
    width: auto;
    display: flex;
    padding: 6px 8px;
}

.cancel-button {
    border-radius: 8px;
    margin-top: 0px;
}
</style>