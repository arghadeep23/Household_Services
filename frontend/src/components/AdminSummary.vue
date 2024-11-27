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
    data() {
        return {
            ratings: [],
            serviceRequests: []
        };
    },
    mounted() {
        this.fetchRatings();
        this.fetchServiceRequests();
    },
    methods: {
        async fetchRatings() {
            try {
                const response = await fetch('http://localhost:5000/api/service_remarks');
                this.ratings = await response.json();
                this.renderRatingsChart();
            } catch (error) {
                console.error("Error fetching ratings:", error);
            }
        },
        async fetchServiceRequests() {
            try {
                const response = await fetch('http://localhost:5000/api/service_requests');
                this.serviceRequests = await response.json();
                this.renderServiceRequestChart();
            } catch (error) {
                console.error("Error fetching service requests:", error);
            }
        },
        renderRatingsChart() {
            const ratingsData = this.ratings.reduce((acc, rating) => {
                acc[Math.floor(rating.rating) - 1]++;
                return acc;
            }, [0, 0, 0, 0, 0]);
            console.log("Ratings Data:", ratingsData);

            const ctx = document.getElementById("ratingsChart").getContext("2d");
            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
                    datasets: [
                        {
                            label: "Ratings Distribution",
                            data: ratingsData,
                            backgroundColor: [
                                "#f44336", // Red 
                                "#ffc107", // Amber 
                                "#ffeb3b", // Yellow 
                                "#8bc34a", // Light Green 
                                "#4caf50", // Green
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
            const serviceRequestData = this.serviceRequests.reduce((acc, request) => {
                if (request.status === 'Requested') acc[0]++;
                if (request.status === 'Accepted') acc[1]++;
                if (request.status === 'Closed') acc[2]++;
                return acc;
            }, [0, 0, 0]);

            const ctx = document.getElementById("serviceRequestChart").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: ["Requested", "Assigned", "Closed"],
                    datasets: [
                        {
                            label: "Service Requests",
                            data: serviceRequestData,
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