
const users = {
    "user1": "password1",
    "user2": "password2"
};

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    if (users[username] && users[username] === password) {
        message.style.color = "green";
        message.textContent = "Login successful!";
        window.location.href = "/homepage/user"
    } else {
        message.style.color = "red";
        message.textContent = "Invalid username or password.";
    }
});
