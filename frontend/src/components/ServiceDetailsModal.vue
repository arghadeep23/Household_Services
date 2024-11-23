<template>
  <div class="modal fade show d-block" tabindex="-1" aria-labelledby="serviceModalLabel">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Service Details</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="serviceName" class="form-label">Service Name</label>
              <input
                type="text"
                class="form-control"
                id="serviceName"
                v-model="editableService.name"
              />
            </div>
            <div class="mb-3">
              <label for="serviceDescription" class="form-label">Service Description</label>
              <textarea
                class="form-control"
                id="serviceDescription"
                v-model="editableService.description"
                rows="3"
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="servicePrice" class="form-label">Base Price</label>
              <input
                type="number"
                class="form-control"
                id="servicePrice"
                v-model="editableService.basePrice"
              />
            </div>

            <h5>Subservices</h5>
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Price</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(subservice, index) in editableService.subservices" :key="index">
                  <td><input type="text" class="form-control" v-model="subservice.name" /></td>
                  <td><input type="number" class="form-control" v-model="subservice.price" /></td>
                  <td>
                    <button
                      class="btn btn-danger btn-sm"
                      @click.prevent="removeSubservice(index)"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
                <tr>
                  <td colspan="3">
                    <button class="btn btn-success btn-sm" @click.prevent="addSubservice">
                      Add Subservice
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </form>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="$emit('close')">Close</button>
          <button class="btn btn-primary" @click="saveChanges">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ServiceDetailsModal",
  props: ["service"],
  data() {
    return {
      editableService: { ...this.service, subservices: [...(this.service.subservices || [])] },
    };
  },
  methods: {
    addSubservice() {
      this.editableService.subservices.push({ name: "", price: 0 });
    },
    removeSubservice(index) {
      this.editableService.subservices.splice(index, 1);
    },
    saveChanges() {
      this.$emit("save", this.editableService);
    },
  },
};
</script>

<style>
.modal-backdrop {
  display: none;
}
</style>
