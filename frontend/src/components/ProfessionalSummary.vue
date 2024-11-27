<template>
    <div class="professional-summary">
        <div class="container mt-4">
            <h3 class="text-center mb-4">Professional Summary</h3>

            <div class="row">
                <!-- Reviews Chart -->
                <div class="col-md-6">
                    <div class="card p-3 mb-4">
                        <h5 class="text-center">Customer Reviews (Out of 5)</h5>
                        <canvas id="reviewsChart"></canvas>
                    </div>
                </div>

                <!-- Services Chart -->
                <div class="col-md-6">
                    <div class="card p-3 mb-4">
                        <h5 class="text-center">Services Overview</h5>
                        <canvas id="servicesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
    name: "ProfessionalSummary",
    data() {
        return {
            reviewsData: [],
            servicesData: []
        };
    },
    mounted() {
        const professionalId = this.$route.params.id;
        this.fetchRatings(professionalId);
        this.fetchServiceRequests(professionalId);
    },
    methods: {
        async fetchRatings(professionalId) {
            try {
                const response = await fetch(`http://localhost:5000/api/professionals/closed-service-requests/${professionalId}`);
                const data = await response.json();
                this.reviewsData = data.map(item => item.rating);
                this.renderReviewsChart();
            } catch (error) {
                console.error("Error fetching ratings:", error);
            }
        },
        async fetchServiceRequests(professionalId) {
            try {
                const response = await fetch(`http://localhost:5000/api/service_requests/professional/${professionalId}`);
                const data = await response.json();
                this.servicesData = data.filter(item => item.status !== "Rejected");
                this.renderServicesChart();
            } catch (error) {
                console.error("Error fetching service requests:", error);
            }
        },
        renderReviewsChart() {
            const ctx = document.getElementById("reviewsChart").getContext("2d");
            const reviewCounts = [0, 0, 0, 0, 0];
            this.reviewsData.forEach(rating => {
                const index = Math.floor(rating) - 1;
                if (index >= 0 && index < 5) {
                    reviewCounts[index]++;
                }
            });
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
                    datasets: [
                        {
                            label: "Number of Reviews",
                            data: reviewCounts,
                            backgroundColor: [
                                "#f44336", // Red for 1 Star
                                "#ff9800", // Orange for 2 Stars
                                "#ffc107", // Yellow for 3 Stars
                                "#4caf50", // Green for 4 Stars
                                "#2196f3", // Blue for 5 Stars
                            ],
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            enabled: true,
                        },
                    },
                },
            });
        },
        renderServicesChart() {
            const ctx = document.getElementById("servicesChart").getContext("2d");
            const serviceCounts = { Accepted: 0, Closed: 0 };
            this.servicesData.forEach(service => {
                if (service.status === "Accepted" || service.status === "Closed") {
                    serviceCounts[service.status]++;
                }
            });
            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: ["Accepted", "Closed"],
                    datasets: [
                        {
                            label: "Service Status",
                            data: [serviceCounts.Accepted, serviceCounts.Closed],
                            backgroundColor: ["#2196f3", "#4caf50"],
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                        tooltip: {
                            enabled: true,
                        },
                    },
                },
            });
        },
    },
};
</script>

<style scoped>
.card {
    border-radius: 8px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

h3 {
    font-weight: bold;
    color: #333;
}

h5 {
    font-weight: bold;
    margin-bottom: 20px;
}

canvas {
    max-height: 400px;
}
</style>