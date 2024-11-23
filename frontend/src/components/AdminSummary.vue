<template>
    <div class="admin-summary">
        <div class="container mt-4">
            <h2 class="text-center mb-4">A-Z Household Services - Customer Feedback Analysis</h2>

            <div class="row">
                <!-- Customer Ratings Chart -->
                <div class="col-md-6">
                    <div class="card p-3 mb-4">
                        <h5 class="text-center">Overall Customer Service Ratings</h5>
                        <canvas id="ratingsChart"></canvas>
                    </div>
                </div>

                <!-- Service Request Summary Chart -->
                <div class="col-md-6">
                    <div class="card p-3 mb-4">
                        <h5 class="text-center">Service Request Summary</h5>
                        <canvas id="serviceRequestChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
    name: "AdminSummary",
    mounted() {
        this.renderRatingsChart();
        this.renderServiceRequestChart();
    },
    methods: {
        renderRatingsChart() {
            const ctx = document.getElementById("ratingsChart").getContext("2d");
            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"],
                    datasets: [
                        {
                            label: "Ratings Distribution",
                            data: [50, 30, 10, 5, 5],
                            backgroundColor: [
                                "#4caf50", // Green
                                "#8bc34a", // Light Green
                                "#ffeb3b", // Yellow
                                "#ffc107", // Amber
                                "#f44336", // Red
                            ],
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                    },
                },
            });
        },
        renderServiceRequestChart() {
            const ctx = document.getElementById("serviceRequestChart").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["Requested", "Approved", "Closed"],
                    datasets: [
                        {
                            label: "Service Requests",
                            data: [40, 30, 50],
                            backgroundColor: [
                                "#2196f3", // Blue
                                "#4caf50", // Green
                                "#f44336", // Red
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
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "Number of Requests",
                            },
                        },
                        x: {
                            title: {
                                display: true,
                                text: "Status",
                            },
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

h2 {
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