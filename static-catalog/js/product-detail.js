// Product Detail Page JavaScript

let currentProduct = null;
let allProducts = [];
let currentImageIndex = 0;

// Load product data on page load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Get product ID from URL
        const urlParams = new URLSearchParams(window.location.search);
        const productId = parseInt(urlParams.get('id'));

        if (!productId) {
            window.location.href = 'products.html';
            return;
        }

        // Fetch products data
        const response = await fetch('data/products.json');
        allProducts = await response.json();

        // Find the current product
        currentProduct = allProducts.find(p => p.id === productId);

        if (!currentProduct) {
            alert('Product not found');
            window.location.href = 'products.html';
            return;
        }

        // Display product details
        displayProduct(currentProduct);
        displayRelatedProducts(currentProduct);

        // Initialize tab functionality
        initializeTabs();

        // Initialize image gallery
        initializeImageGallery();

    } catch (error) {
        console.error('Error loading product:', error);
        alert('Error loading product details');
    }
});

// Display product information
function displayProduct(product) {
    // Breadcrumb
    document.getElementById('breadcrumbCategory').textContent = product.category;
    document.getElementById('breadcrumbProduct').textContent = product.name;

    // Product Info
    document.getElementById('productCategory').textContent = product.category;
    document.getElementById('productTitle').textContent = product.name;
    
    // Price with MRP and Discount
    const priceSection = document.getElementById('productPrice');
    const discount = product.mrp ? Math.round(((product.mrp - product.price) / product.mrp) * 100) : 0;
    
    if (product.mrp && discount > 0) {
        priceSection.innerHTML = `
            <div class="price-container">
                <span class="current-price">₹${product.price.toLocaleString('en-IN')}</span>
                <span class="original-price">₹${product.mrp.toLocaleString('en-IN')}</span>
                <span class="discount-percentage">${discount}% OFF</span>
            </div>
        `;
    } else {
        priceSection.innerHTML = `<span class="current-price">₹${product.price.toLocaleString('en-IN')}</span>`;
    }
    
    // Stock status
    const stockBadge = document.getElementById('productStock');
    stockBadge.textContent = product.inStock ? '✓ In Stock' : '✗ Out of Stock';
    stockBadge.className = `product-stock ${product.inStock ? 'in-stock' : 'out-of-stock'}`;

    // Description
    document.getElementById('productDescription').innerHTML = `<p>${product.description}</p>`;

    // Features
    const featuresList = document.getElementById('featuresList');
    featuresList.innerHTML = product.features.map(feature => `<li>${feature}</li>`).join('');

    // Specifications
    if (product.specifications) {
        const specsTable = document.getElementById('specsTable');
        specsTable.innerHTML = Object.entries(product.specifications)
            .map(([key, value]) => `
                <tr>
                    <td class="spec-label">${key}</td>
                    <td class="spec-value">${value}</td>
                </tr>
            `).join('');
    } else {
        document.getElementById('productSpecifications').style.display = 'none';
    }

    // Image Gallery
    const images = product.images || [product.image];
    const mainImage = document.getElementById('mainImage');
    mainImage.src = images[0];
    mainImage.alt = product.name;

    // Thumbnails
    const thumbnailContainer = document.getElementById('thumbnailContainer');
    thumbnailContainer.innerHTML = images.map((img, index) => `
        <img src="${img}" alt="${product.name} - Image ${index + 1}" 
             class="thumbnail ${index === 0 ? 'active' : ''}" 
             onclick="changeMainImage(${index})">
    `).join('');

    // Details tab content
    document.getElementById('detailsContent').innerHTML = `
        <h3>About This Product</h3>
        <p>${product.description}</p>
        ${product.detailedDescription ? `<p>${product.detailedDescription}</p>` : ''}
    `;

    // Care Instructions
    if (product.careInstructions) {
        const careList = document.getElementById('careInstructions');
        careList.innerHTML = product.careInstructions.map(instruction => `<li>${instruction}</li>`).join('');
    } else {
        // Default care instructions
        const careList = document.getElementById('careInstructions');
        careList.innerHTML = `
            <li>Machine wash cold with similar colors</li>
            <li>Use mild detergent, no bleach</li>
            <li>Tumble dry on low heat</li>
            <li>Iron on low temperature if needed</li>
            <li>Do not dry clean</li>
        `;
    }

    // Action buttons
    document.getElementById('whatsappBtn').onclick = () => sendWhatsAppInquiry(product);
    document.getElementById('emailBtn').onclick = () => sendEmailInquiry(product);
}

// Change main image when clicking thumbnail
function changeMainImage(index) {
    const images = currentProduct.images || [currentProduct.image];
    currentImageIndex = index;
    
    const mainImage = document.getElementById('mainImage');
    mainImage.src = images[index];

    // Update active thumbnail
    document.querySelectorAll('.thumbnail').forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
}

// Initialize image gallery and modal
function initializeImageGallery() {
    const mainImage = document.getElementById('mainImage');
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalClose = document.getElementById('modalClose');
    const modalPrev = document.getElementById('modalPrev');
    const modalNext = document.getElementById('modalNext');

    // Open modal on image click
    mainImage.onclick = () => {
        modal.style.display = 'flex';
        modalImage.src = mainImage.src;
    };

    // Close modal
    modalClose.onclick = () => {
        modal.style.display = 'none';
    };

    // Close modal on outside click
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    };

    // Navigate images in modal
    modalPrev.onclick = (e) => {
        e.stopPropagation();
        const images = currentProduct.images || [currentProduct.image];
        currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        modalImage.src = images[currentImageIndex];
        changeMainImage(currentImageIndex);
    };

    modalNext.onclick = (e) => {
        e.stopPropagation();
        const images = currentProduct.images || [currentProduct.image];
        currentImageIndex = (currentImageIndex + 1) % images.length;
        modalImage.src = images[currentImageIndex];
        changeMainImage(currentImageIndex);
    };

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (modal.style.display === 'flex') {
            if (e.key === 'Escape') {
                modal.style.display = 'none';
            } else if (e.key === 'ArrowLeft') {
                modalPrev.click();
            } else if (e.key === 'ArrowRight') {
                modalNext.click();
            }
        }
    });
}

// Initialize tabs functionality
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to clicked button and corresponding pane
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Display related products
function displayRelatedProducts(currentProduct) {
    const relatedProductsGrid = document.getElementById('relatedProductsGrid');
    
    // Get products from same category, excluding current product
    const relatedProducts = allProducts
        .filter(p => p.category === currentProduct.category && p.id !== currentProduct.id)
        .slice(0, 4); // Show max 4 related products

    if (relatedProducts.length === 0) {
        relatedProductsGrid.innerHTML = '<p class="text-muted">No related products available.</p>';
        return;
    }

    relatedProductsGrid.innerHTML = relatedProducts.map(product => {
        const discount = product.mrp ? Math.round(((product.mrp - product.price) / product.mrp) * 100) : 0;
        const discountBadge = discount > 0 ? `<span class="discount-badge">${discount}% OFF</span>` : '';
        
        return `
        <div class="product-card">
            <a href="product-detail.html?id=${product.id}" class="product-link">
                <div class="product-image">
                    ${discountBadge}
                    <img src="${product.image}" alt="${product.name}" loading="lazy">
                    ${!product.inStock ? '<span class="badge badge-out">Out of Stock</span>' : ''}
                </div>
                <div class="product-details">
                    <span class="product-category-badge">${product.category}</span>
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-desc">${product.description.substring(0, 80)}...</p>
                    <div class="product-footer">
                        <div class="product-pricing">
                            ${product.mrp ? `<span class="product-mrp">₹${product.mrp.toLocaleString('en-IN')}</span>` : ''}
                            <span class="product-price">₹${product.price.toLocaleString('en-IN')}</span>
                        </div>
                        <button class="btn btn-small">View Details</button>
                    </div>
                </div>
            </a>
        </div>
    `;
    }).join('');
}

// Send WhatsApp inquiry
function sendWhatsAppInquiry(product) {
    const message = `Hi LUVORA! I'm interested in:\n\n*${product.name}*\nPrice: ₹${product.price.toLocaleString('en-IN')}\nCategory: ${product.category}\n\nCan you provide more details?`;
    const phoneNumber = '918920215965'; // Your WhatsApp number (remove + and spaces)
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

// Send email inquiry
function sendEmailInquiry(product) {
    const subject = `Inquiry about ${product.name}`;
    const body = `Hi LUVORA,\n\nI'm interested in the following product:\n\nProduct: ${product.name}\nPrice: ₹${product.price.toLocaleString('en-IN')}\nCategory: ${product.category}\n\nPlease provide more information including:\n- Availability\n- Bulk pricing (if applicable)\n- Delivery timeline\n- Any other variants available\n\nThank you!`;
    
    const mailtoUrl = `mailto:luvorahomes25@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailtoUrl;
}
