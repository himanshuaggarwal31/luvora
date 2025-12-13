// Catalog page functionality with filtering and search

let currentProducts = [];
let filteredProducts = [];

// Initialize catalog page
if (window.location.pathname.includes('products.html')) {
    document.addEventListener('DOMContentLoaded', async function() {
        // Load products
        currentProducts = await loadProducts();
        filteredProducts = [...currentProducts];
        
        // Display all products initially
        displayCatalogProducts();
        
        // Setup event listeners
        setupFilters();
        setupSearch();
        setupSort();
    });
}

function displayCatalogProducts() {
    const grid = document.getElementById('productsGrid');
    const noProducts = document.getElementById('noProducts');
    const productsCount = document.getElementById('productsCount');
    
    if (!grid) return;
    
    if (filteredProducts.length === 0) {
        grid.style.display = 'none';
        noProducts.style.display = 'block';
        productsCount.textContent = 'No products found';
    } else {
        grid.style.display = 'grid';
        noProducts.style.display = 'none';
        productsCount.textContent = `Showing ${filteredProducts.length} product${filteredProducts.length !== 1 ? 's' : ''}`;
        grid.innerHTML = filteredProducts.map(product => createProductCard(product)).join('');
    }
}

function setupFilters() {
    // Category filter
    const categoryFilters = document.querySelectorAll('input[name="category"]');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', applyFilters);
    });
    
    // Price filter
    const priceFilters = document.querySelectorAll('input[name="price"]');
    priceFilters.forEach(filter => {
        filter.addEventListener('change', applyFilters);
    });
    
    // Stock filter
    const stockFilter = document.getElementById('inStockOnly');
    if (stockFilter) {
        stockFilter.addEventListener('change', applyFilters);
    }
    
    // Clear filters button
    const clearBtn = document.getElementById('clearFilters');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearFilters);
    }
    
    // Reset filters button (in no products message)
    const resetBtn = document.getElementById('resetFilters');
    if (resetBtn) {
        resetBtn.addEventListener('click', clearFilters);
    }
}

function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', applyFilters);
    }
}

function setupSort() {
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            sortProducts(this.value);
            displayCatalogProducts();
        });
    }
}

function applyFilters() {
    let products = [...currentProducts];
    
    // Apply category filter
    const selectedCategory = document.querySelector('input[name="category"]:checked');
    if (selectedCategory && selectedCategory.value !== 'all') {
        products = products.filter(p => p.category === selectedCategory.value);
    }
    
    // Apply price filter
    const selectedPrice = document.querySelector('input[name="price"]:checked');
    if (selectedPrice && selectedPrice.value !== 'all') {
        const [min, max] = selectedPrice.value.split('-').map(Number);
        products = products.filter(p => p.price >= min && p.price <= max);
    }
    
    // Apply stock filter
    const inStockOnly = document.getElementById('inStockOnly');
    if (inStockOnly && inStockOnly.checked) {
        products = products.filter(p => p.inStock);
    }
    
    // Apply search filter
    const searchInput = document.getElementById('searchInput');
    if (searchInput && searchInput.value.trim()) {
        const searchTerm = searchInput.value.toLowerCase();
        products = products.filter(p => 
            p.name.toLowerCase().includes(searchTerm) ||
            p.description.toLowerCase().includes(searchTerm) ||
            p.category.toLowerCase().includes(searchTerm)
        );
    }
    
    filteredProducts = products;
    
    // Apply current sort
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortProducts(sortSelect.value);
    }
    
    displayCatalogProducts();
}

function sortProducts(sortBy) {
    switch(sortBy) {
        case 'price-low':
            filteredProducts.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            filteredProducts.sort((a, b) => b.price - a.price);
            break;
        case 'name':
            filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
            break;
        default:
            // Default order (by id)
            filteredProducts.sort((a, b) => a.id - b.id);
    }
}

function clearFilters() {
    // Reset category
    const allCategory = document.querySelector('input[name="category"][value="all"]');
    if (allCategory) allCategory.checked = true;
    
    // Reset price
    const allPrice = document.querySelector('input[name="price"][value="all"]');
    if (allPrice) allPrice.checked = true;
    
    // Reset stock
    const inStockOnly = document.getElementById('inStockOnly');
    if (inStockOnly) inStockOnly.checked = false;
    
    // Reset search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.value = '';
    
    // Reset sort
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) sortSelect.value = 'default';
    
    // Reapply filters (which will show all)
    applyFilters();
}
