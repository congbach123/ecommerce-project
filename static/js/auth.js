// Auth Functions
async function login(username, password) {
  const response = await fetch(`${API_URL}/users/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();

  if (response.ok && data.token) {
    localStorage.setItem(TOKEN_KEY, data.token);
    return true;
  }

  return false;
}

// async function register(userData) {
//   const response = await fetch(`${API_URL}/users/register/`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(userData),
//   });

//   return response.ok;
// }
async function register(userData) {
  // Get the CSRF token from the cookie
  const csrftoken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  const response = await fetch(`${API_URL}/users/register/`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify(userData),
  });

  return response.ok;
}
// Login Form Handler
if (document.getElementById("login-form")) {
  document
    .getElementById("login-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      const success = await login(username, password);

      if (success) {
        window.location.href = "/";
      } else {
        document.getElementById("login-error").textContent =
          "Invalid credentials";
      }
    });
}

// Register Form Handler
if (document.getElementById("register-form")) {
  document
    .getElementById("register-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const userData = {
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        password2: document.getElementById("password2").value,
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        phone_number: document.getElementById("phone").value,
        address: document.getElementById("address").value,
      };

      const success = await register(userData);

      if (success) {
        window.location.href = "/login?registered=true";
      } else {
        document.getElementById("register-error").textContent =
          "Registration failed";
      }
    });
}
