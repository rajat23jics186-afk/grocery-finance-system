/* Dashboard JavaScript */

const API_BASE = "http://localhost:8000/api";
let currentUser = null;
let currentToken = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadPage('dashboard');
});

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        currentToken = token;
        currentUser = JSON.parse(user);
        document.getElementById('userName').textContent = currentUser.username;
    } else {
        // Redirect to login
        window.location.href = '/login';
    }
}

// Load page content
function loadPage(page) {
    const content = document.getElementById('content');
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.closest('.nav-link').classList.add('active');
    
    switch(page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'products':
            loadProducts();
            break;
        case 'orders':
            loadOrders();
            break;
        case 'payments':
            loadPayments();
            break;
        case 'reports':
            loadReports();
            break;
        case 'analytics':
            loadAnalytics();
            break;
    }
}

// Load Dashboard
function loadDashboard() {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="fas fa-chart-line"></i> Dashboard</h2>
        </div>
        
        <div class="row" id="metricsRow">
            <div class="col-md-3">
                <div class="metric-card">
                    <i class="fas fa-shopping-cart" style="color: #3498db; font-size: 2rem;"></i>
                    <div class="metric-value" id="totalOrders">0</div>
                    <div class="metric-label">Total Orders</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card success">
                    <i class="fas fa-dollar-sign" style="color: #27ae60; font-size: 2rem;"></i>
                    <div class="metric-value" id="totalRevenue">$0</div>
                    <div class="metric-label">Total Revenue</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <i class="fas fa-users" style="color: #9b59b6; font-size: 2rem;"></i>
                    <div class="metric-value" id="totalCustomers">0</div>
                    <div class="metric-label">Total Customers</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card warning">
                    <i class="fas fa-hourglass-half" style="color: #f39c12; font-size: 2rem;"></i>
                    <div class="metric-value" id="pendingOrders">0</div>
                    <div class="metric-label">Pending Orders</div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Sales by Category</div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="categoryChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Payment Status</div>
                    <div class="card-body">
                        <div class="chart-container">
                            <canvas id="paymentChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Load metrics
    fetch(`${API_BASE}/reports/dashboard-summary`, {
        headers: {'Authorization': `Bearer ${currentToken}`}
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById('totalOrders').textContent = data.total_orders;
        document.getElementById('totalRevenue').textContent = `$${data.total_revenue.toFixed(2)}`;
        document.getElementById('totalCustomers').textContent = data.total_customers;
        document.getElementById('pendingOrders').textContent = data.pending_orders;
    });
    
    // Load charts
    loadCharts();
}

// Load Products
function loadProducts() {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="fas fa-box"></i> Products</h2>
            <button class="btn btn-primary" onclick="showAddProductModal()">
                <i class="fas fa-plus"></i> Add Product
            </button>
        </div>
        
        <div class="card">
            <div class="card-body">
                <table class="table table-hover" id="productsTable">
                    <thead>
                        <tr>
                            <th>Product ID</th>
                            <th>Name</th>
                            <th>Category</th>
                            <th>Retail Price</th>
                            <th>Stock</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    // Load products data
    fetch(`${API_BASE}/products/`, {
        headers: {'Authorization': `Bearer ${currentToken}`}
    })
    .then(r => r.json())
    .then(data => {
        const tbody = document.querySelector('#productsTable tbody');
        data.forEach(product => {
            const row = `
                <tr>
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.category}</td>
                    <td>$${product.retail_price.toFixed(2)}</td>
                    <td>${product.quantity_in_stock}</td>
                    <td>
                        <button class="btn btn-sm btn-primary">Edit</button>
                        <button class="btn btn-sm btn-danger">Delete</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    });
}

// Load Orders
function loadOrders() {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="fas fa-shopping-cart"></i> Orders</h2>
            <button class="btn btn-primary" onclick="showAddOrderModal()">
                <i class="fas fa-plus"></i> New Order
            </button>
        </div>
        
        <div class="card">
            <div class="card-body">
                <table class="table table-hover" id="ordersTable">
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Customer</th>
                            <th>Total</th>
                            <th>Status</th>
                            <th>Payment</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    // Load orders
    fetch(`${API_BASE}/orders/`, {
        headers: {'Authorization': `Bearer ${currentToken}`}
    })
    .then(r => r.json())
    .then(data => {
        const tbody = document.querySelector('#ordersTable tbody');
        data.forEach(order => {
            const statusBadge = `<span class="badge badge-${order.order_status}">${order.order_status}</span>`;
            const row = `
                <tr>
                    <td>#${order.id}</td>
                    <td>Customer ${order.customer_id}</td>
                    <td>$${order.total_amount.toFixed(2)}</td>
                    <td>${statusBadge}</td>
                    <td><span class="badge badge-${order.payment_status}">${order.payment_status}</span></td>
                    <td>${new Date(order.order_date).toLocaleDateString()}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    });
}

// Load Payments
function loadPayments() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h2><i class="fas fa-credit-card"></i> Payments</h2>
        <div class="alert alert-info">Payment management interface - Coming soon</div>
    `;
}

// Load Reports
function loadReports() {
    const content = document.getElementById('content');
    
    content.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="fas fa-file-chart-line"></i> Reports</h2>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Retail vs Wholesale Sales</div>
                    <div class="card-body">
                        <div id="retailVsWholesale"></div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">Sales by Category</div>
                    <div class="card-body">
                        <div id="categoryReport"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Load retail vs wholesale
    fetch(`${API_BASE}/reports/retail-vs-wholesale`, {
        headers: {'Authorization': `Bearer ${currentToken}`}
    })
    .then(r => r.json())
    .then(data => {
        const html = `
            <p><strong>Retail Revenue:</strong> $${data.retail_revenue.toFixed(2)}</p>
            <p><strong>Wholesale Revenue:</strong> $${data.wholesale_revenue.toFixed(2)}</p>
            <p><strong>Total:</strong> $${data.total_revenue.toFixed(2)}</p>
        `;
        document.getElementById('retailVsWholesale').innerHTML = html;
    });
}

// Load Analytics
function loadAnalytics() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <h2><i class="fas fa-brain"></i> AI Analytics Dashboard</h2>
        <div class="alert alert-info">
            <strong>AI Models Available:</strong>
            <ul>
                <li>Customer Segmentation (K-Means)</li>
                <li>Demand Forecasting (Neural Network)</li>
                <li>Fraud Detection (Autoencoder)</li>
                <li>Time Series Forecasting (LSTM)</li>
            </ul>
        </div>
        <div class="alert alert-warning">
            <strong>Streamlit Dashboard:</strong> Run <code>streamlit run dashboards/streamlit_app.py</code><br>
            <strong>Gradio Dashboard:</strong> Run <code>python dashboards/gradio_app.py</code>
        </div>
    `;
}

// Load Charts
function loadCharts() {
    // Category Chart
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'bar',
            data: {
                labels: ['Produce', 'Dairy', 'Meat', 'Bakery'],
                datasets: [{
                    label: 'Sales',
                    data: [1200, 1900, 800, 2500],
                    backgroundColor: ['#3498db', '#27ae60', '#e74c3c', '#f39c12']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Payment Status Chart
    const paymentCtx = document.getElementById('paymentChart');
    if (paymentCtx) {
        new Chart(paymentCtx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Pending', 'Failed'],
                datasets: [{
                    data: [65, 25, 10],
                    backgroundColor: ['#27ae60', '#f39c12', '#e74c3c']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

// Logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}
