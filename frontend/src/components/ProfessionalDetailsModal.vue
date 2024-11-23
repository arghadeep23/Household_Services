<template>
    <div class="modal fade show d-block" tabindex="-1" aria-labelledby="professionalModalLabel">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Professional Details</h5>
                    <button type="button" class="btn-close" @click="$emit('close')"></button>
                </div>
                <div class="modal-body">
                    <p><strong>Full Name:</strong> {{ professional.name }}</p>
                    <p><strong>Email:</strong> {{ professional.email }}</p>
                    <p><strong>Service:</strong> {{ professional.serviceName }}</p>
                    <p><strong>Experience:</strong> {{ professional.experience }} years</p>
                    <p><strong>Address:</strong> {{ professional.address }}</p>
                    <p><strong>Pincode:</strong> {{ professional.pincode }}</p>
                    <p>
                        <strong>Document:</strong>
                        <a :href="'/path/to/documents/' + professional.document" download>
                            Download {{ professional.document }}
                        </a>
                    </p>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="$emit('close')">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ProfessionalDetailsModal",
    props: ["professional"],
};
</script>

<style>
.modal-backdrop {
    display: none;
}
</style>
