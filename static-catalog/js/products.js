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
    
    // Calculate discount percentage
    const discount = product.mrp ? Math.round(((product.mrp - product.price) / product.mrp) * 100) : 0;
    const discountBadge = discount > 0 ? `<span class="discount-badge">${discount}% OFF</span>` : '';
    
    return `
        <div class="product-card" data-product-id="${product.id}">
            <a href="product-detail.html?id=${product.id}" class="product-link">
                <div class="product-image">
                    ${discountBadge}
                    <img src="${product.image}" alt="${product.name}" loading="lazy" onerror="this.src='https://via.placeholder.com/400x300?text=No+Image'">
                </div>
                <div class="product-info">
                    <p class="product-category">${product.category}</p>
                    <h3 class="product-name">${product.name}</h3>
                    <div class="product-pricing">
                        ${product.mrp ? `<span class="product-mrp">₹${product.mrp.toLocaleString('en-IN')}</span>` : ''}
                        <span class="product-price">₹${product.price.toLocaleString('en-IN')}</span>
                    </div>
                    <p class="product-stock ${stockClass}">${stockText}</p>
                    <button class="btn btn-small">View Details</button>
                </div>
            </a>
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
