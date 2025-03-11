const token = "f4ad3dfd3ff6a4bc3424bcaf80a4b23e4c25db43"; // Replace with dynamic token storage (localStorage/sessionStorage)
        const profileUrl = "http://localhost:8000/profile/";

                function getCSRFToken() {
            let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
            return csrfToken ? csrfToken.split('=')[1] : '';
        }
        async function fetchProfile() {
            try {
                const response = await fetch(profileUrl, {
                    headers: { 'Authorization': `Token ${token}` }
                });
                if (!response.ok) throw new Error("Failed to fetch profile");

                const data = await response.json();
                document.getElementById("username").value = data.username;
                document.getElementById("email").value = data.email;
                document.getElementById("first_name").value = data.first_name || "";
                document.getElementById("last_name").value = data.last_name || "";
            } catch (error) {
                document.getElementById("message").textContent = "Error fetching profile.";
                console.error(error);
            }
        }

        async function updateProfile() {
            const updatedData = {
                email: document.getElementById("email").value,
                first_name: document.getElementById("first_name").value,
                last_name: document.getElementById("last_name").value
            };

            try {
                const response = await fetch(profileUrl, {
                    method: "PATCH", // Use PATCH instead of PUT to match your API
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify(updatedData)
                });

                const responseData = await response.json();

                if (response.ok) {
                    document.getElementById("message").textContent = "Profile updated successfully!";
                } else {
                    document.getElementById("message").textContent = responseData.detail || "Failed to update profile.";
                }
            } catch (error) {
                document.getElementById("message").textContent = "Error updating profile.";
                console.error(error);
            }
        }

        fetchProfile();