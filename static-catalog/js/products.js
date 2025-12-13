// Products data management and display

let allProducts = [];

// Load products from JSON
async function loadProducts() {
    try {
        const response = await fetch('data/products.json');
        allProducts = await response.json();
        return allProducts;
    } catch (error) {
        console.error('Error loading products:', error);
        return [];
    }
}

// Create product card HTML
function createProductCard(product) {
    const stockClass = product.inStock ? 'in-stock' : 'out-of-stock';
    const stockText = product.inStock ? '✓ In Stock' : '✗ Out of Stock';
    
    return `
        <div class="product-card" data-product-id="${product.id}">
            <div class="product-image">
                <span>🛏️</span>
            </div>
            <div class="product-info">
                <p class="product-category">${product.category}</p>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-price">₹${product.price.toLocaleString('en-IN')}</p>
                <p class="product-stock ${stockClass}">${stockText}</p>
            </div>
        </div>
    `;
}

// Display products in grid
function displayProducts(products, containerId = 'featuredProducts') {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (products.length === 0) {
        container.innerHTML = '<p class="text-center">No products available.</p>';
        return;
    }

    container.innerHTML = products.map(product => createProductCard(product)).join('');
}

// Initialize products on homepage
if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/') {
    loadProducts().then(products => {
        // Show first 3 products on homepage
        displayProducts(products.slice(0, 3), 'featuredProducts');
    });
}
