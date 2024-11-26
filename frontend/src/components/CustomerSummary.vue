<template>
    <div class="customer-summary container mt-4">
        <h3 class="mb-4">Customer Service Summary</h3>
        <div class="chart-container" style="height: 400px; width: 600px;">
            <canvas id="serviceSummaryChart"></canvas>
        </div>
    </div>
</template>

<script>
import { getApiUrl } from "@/utils/api";
import Chart from "chart.js/auto";

export default {
    name: "CustomerSummary",
    data() {
        return {
            chart: null,
        };
    },
    mounted() {
        this.fetchDataAndRenderChart();
    },
    methods: {
        async fetchDataAndRenderChart() {
            try {
                const response = await fetch(`${getApiUrl()}/api/service_requests/customer/${this.$route.params.id}`);
                const data = await response.json();

                const statusCounts = data.reduce((acc, item) => {
                    acc[item.status] = (acc[item.status] || 0) + 1;
                    return acc;
                }, {});

                const chartData = {
                    labels: ["Requested", "Closed", "Assigned"],
                    datasets: [
                        {
                            label: "Number of Services",
                            data: [
                                statusCounts["Requested"] || 0,
                                statusCounts["Closed"] || 0,
                                statusCounts["Accepted"] || 0,
                            ],
                            backgroundColor: ["#007bff", "#28a745", "#ffc107"],
                            borderColor: ["#0056b3", "#1e7e34", "#e0a800"],
                            borderWidth: 1,
                        },
                    ],
                };

                this.renderChart(chartData);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        },
        renderChart(chartData) {
            const ctx = document.getElementById("serviceSummaryChart").getContext("2d");

            this.chart = new Chart(ctx, {
                type: "bar", // Using a bar chart
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: "top",
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "Number of Services",
                            },
                        },
                        x: {
                            title: {
                                display: true,
                                text: "Service Status",
                            },
                        },
                    },
                },
            });
        },
    },
    beforeUnmount() {
        if (this.chart) {
            this.chart.destroy(); // Clean up the chart instance
        }
    },
};
</script>

<style scoped>
.chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>