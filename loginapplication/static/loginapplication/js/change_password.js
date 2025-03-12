const token = "f4ad3dfd3ff6a4bc3424bcaf80a4b23e4c25db43"; // Replace with dynamic token storage
const changePasswordUrl = "http://localhost:8000/change-password/"; // Your actual API endpoint

function getCSRFToken() {
    let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : '';
}

async function updatePassword() {
    const oldPassword = document.getElementById("oldpassword").value;
    const newPassword = document.getElementById("newpassword").value;

    if (!oldPassword || !newPassword) {
        document.getElementById("message").textContent = "Please enter both old and new passwords.";
        return;
    }

    try {
        const response = await fetch(changePasswordUrl, {
            method: "POST",  // Use POST for password change requests
            headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });

        const responseData = await response.json();

        if (response.ok) {
            document.getElementById("message").textContent = "Password updated successfully!";
        } else {
            document.getElementById("message").textContent = responseData.detail || "Failed to update password.";
        }
    } catch (error) {
        document.getElementById("message").textContent = "Error updating password.";
        console.error(error);
    }
}
