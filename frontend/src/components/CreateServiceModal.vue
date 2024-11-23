<template>
    <div class="modal show" tabindex="-1" style="display: block;" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Create New Service</h5>
                    <button type="button" class="btn-close" aria-label="Close" @click="$emit('close')"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="saveService">
                        <div class="mb-3">
                            <label for="serviceName" class="form-label">Service Name</label>
                            <input type="text" class="form-control" id="serviceName" v-model="newService.name"
                                required />
                        </div>
                        <div class="mb-3">
                            <label for="serviceDescription" class="form-label">Description</label>
                            <textarea class="form-control" id="serviceDescription" v-model="newService.description"
                                required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="basePrice" class="form-label">Base Price</label>
                            <input type="number" class="form-control" id="basePrice"
                                v-model.number="newService.basePrice" required />
                        </div>
                        <div>
                            <h5>Subservices</h5>
                            <div v-for="(subservice, index) in newService.subservices" :key="index" class="mb-3">
                                <input type="text" class="form-control mb-2" placeholder="Subservice Name"
                                    v-model="subservice.name" required />
                                <input type="number" class="form-control" placeholder="Base Price"
                                    v-model.number="subservice.basePrice" required />
                                <button type="button" class="btn btn-danger mt-2" @click="removeSubservice(index)">
                                    Remove Subservice
                                </button>
                            </div>
                            <button type="button" class="btn btn-secondary mt-3" @click="addSubservice">
                                Add Subservice
                            </button>
                        </div>
                        <div class="modal-footer mt-4">
                            <button type="button" class="btn btn-secondary" @click="$emit('close')">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary">
                                Save Service
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CreateServiceModal",
    data() {
        return {
            newService: {
                name: "",
                description: "",
                basePrice: 0,
                subservices: [],
            },
        };
    },
    methods: {
        addSubservice() {
            this.newService.subservices.push({ name: "", basePrice: 0 });
        },
        removeSubservice(index) {
            this.newService.subservices.splice(index, 1);
        },
        saveService() {
            // Emit event to save the service
            this.$emit("save", this.newService);
        },
    },
};
</script>

<style scoped>
.modal {
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-dialog {
    max-width: 600px;
}

.modal-body {
    padding: 1.5rem;
}
</style>
