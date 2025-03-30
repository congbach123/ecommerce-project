// Constants
const API_URL = "http://localhost:8000/api";
const TOKEN_KEY = "auth_token";

// Helper Functions
function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function getAuthHeaders() {
  const token = getToken();
  return token ? { Authorization: `Token ${token}` } : {};
}

async function fetchAPI(endpoint, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...getAuthHeaders(),
    ...options.headers,
  };

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API Request Failed:", error);
    return null;
  }
}

// Load Categories
async function loadCategories() {
  const categories = await fetchAPI("/products/categories/");
  const dropdown = document.getElementById("category-dropdown");

  if (categories && dropdown) {
    dropdown.innerHTML = "";

    categories.forEach((category) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.classList.add("dropdown-item");
      a.href = `/products?category=${category.id}`;
      a.textContent = category.name;
      li.appendChild(a);
      dropdown.appendChild(li);
    });
  }
}

// Load Cart Count
async function loadCartCount() {
  if (!getToken()) return;

  const cart = await fetchAPI("/cart/");
  const cartCount = document.getElementById("cart-count");

  if (cart && cartCount) {
    const count = cart.items ? cart.items.length : 0;
    cartCount.textContent = count;
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  loadCategories();
  loadCartCount();
  updateUserNav();
});

// Update User Navigation
function updateUserNav() {
  const userDropdown = document.getElementById("user-dropdown");
  const token = getToken();

  if (userDropdown) {
    if (token) {
      userDropdown.innerHTML = `
        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
          <i class="fas fa-user"></i> Account
        </a>
        <ul class="dropdown-menu dropdown-menu-end">
          <li><a class="dropdown-item" href="/profile">Profile</a></li>
          <li><a class="dropdown-item" href="/orders">Orders</a></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item" href="#" id="logout-link">Logout</a></li>
        </ul>
      `;

      document.getElementById("logout-link").addEventListener("click", (e) => {
        e.preventDefault();
        localStorage.removeItem(TOKEN_KEY);
        window.location.href = "/";
      });
    } else {
      userDropdown.innerHTML = `
        <a class="nav-link" href="/login">
          <i class="fas fa-sign-in-alt"></i> Login
        </a>
      `;
    }
  }
}

// Record Product Interaction
async function recordInteraction(productId, interactionType, rating = null) {
  if (!getToken()) return;

  const data = {
    product_id: productId,
    interaction_type: interactionType,
    rating: rating,
  };

  await fetchAPI("/recommendations/interactions/record_interaction/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
