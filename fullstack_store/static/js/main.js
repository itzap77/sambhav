function toggleCart() {
    document.getElementById('cart-sidebar').classList.toggle('open');
}

function showToast(message) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.className = "show";
    setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 3000);
}

async function loadProducts() {
    const response = await fetch('/api/products');
    const products = await response.json();
    const container = document.getElementById('product-list');
    container.innerHTML = '';
    
    products.forEach(p => {
        container.innerHTML += `
            <div class="product-card">
                <img class="product-img" src="${p.image_url}" alt="${p.name}">
                <div class="product-info">
                    <div class="product-title">${p.name}</div>
                    <div class="product-price">₹${p.price.toLocaleString('en-IN')}</div>
                    <div class="product-stock">Available Stock: ${p.stock_qty}</div>
                    <button onclick="addToCart(${p.product_id})">Add to Cart</button>
                </div>
            </div>
        `;
    });
}

async function addToCart(productId) {
    const response = await fetch('/api/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
    });
    const data = await response.json();
    if(data.status === 'success') {
        showToast("Item added to cart!");
        loadCart();
    } else {
        showToast(data.message);
    }
}

async function loadCart() {
    const response = await fetch('/api/cart');
    const cart = await response.json();
    
    document.getElementById('cart-count').innerText = cart.count || 0;
    const container = document.getElementById('cart-contents');
    
    if (cart.items.length === 0) {
        container.innerHTML = '<p style="text-align:center; color:#888; margin-top:20px;">Cart is empty.</p>';
        document.getElementById('cart-total').innerText = '₹0';
        return;
    }

    container.innerHTML = '';
    cart.items.forEach(item => {
        container.innerHTML += `
            <div class="cart-item">
                <img src="${item.image_url}" alt="${item.name}">
                <div class="cart-item-details">
                    <div class="cart-item-title">${item.name}</div>
                    <div class="cart-item-price">${item.qty} x ₹${item.price.toLocaleString('en-IN')}</div>
                </div>
            </div>
        `;
    });
    document.getElementById('cart-total').innerText = `₹${cart.total.toLocaleString('en-IN')}`;
}

// NEW: Open the Modal
function openCheckoutModal() {
    const cartTotalText = document.getElementById('cart-total').innerText;
    if (cartTotalText === '₹0') {
        alert('Your cart is empty! Please add items before checking out.');
        return;
    }
    document.getElementById('pay-amount').innerText = '(' + cartTotalText + ')';
    document.getElementById('checkout-modal').classList.add('show');
    toggleCart(); // Close the sidebar cart so it isn't in the way
}

// NEW: Close the Modal
function closeCheckout() {
    document.getElementById('checkout-modal').classList.remove('show');
}

// NEW: Simulate payment processing before calling backend API
async function processPayment(event) {
    event.preventDefault(); // Stop form from reloading the page
    
    const payBtn = document.querySelector('.pay-btn');
    payBtn.innerText = 'Processing Transaction...';
    payBtn.disabled = true;

    // Simulate a 1.5-second delay to make it feel like a real bank API call
    setTimeout(async () => {
        const response = await fetch('/api/checkout', { method: 'POST' });
        const data = await response.json();
        
        if (data.status === 'success') {
            closeCheckout();
            alert(`Payment Authorized Successfully!\nOrder Reference ID: ${data.order_id}\nThank you for shopping at Sambhav's Store.`);
            loadCart(); 
            loadProducts(); 
            document.getElementById('payment-form').reset();
        } else {
            alert(`Checkout failed: ${data.message}`);
        }
        
        payBtn.innerText = 'Pay Now';
        payBtn.disabled = false;
    }, 1500);
}

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    loadCart();
});
