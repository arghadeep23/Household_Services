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
    mounted() {
        this.renderReviewsChart();
        this.renderServicesChart();
    },
    methods: {
        renderReviewsChart() {
            const ctx = document.getElementById("reviewsChart").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
                    datasets: [
                        {
                            label: "Number of Reviews",
                            data: [2, 5, 10, 20, 15], // Dummy review counts
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
            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: ["Rejected", "Accepted", "Closed"],
                    datasets: [
                        {
                            label: "Service Status",
                            data: [3, 12, 8], // Dummy service status counts
                            backgroundColor: ["#f44336", "#2196f3", "#4caf50"],
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
