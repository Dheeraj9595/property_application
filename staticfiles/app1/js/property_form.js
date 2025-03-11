
        document.getElementById("propertyForm").addEventListener("submit", async function(event) {
            event.preventDefault(); // Prevent form submission

            const title = document.getElementById("title").value;
            const owner = document.getElementById("owner").value;
            const area = document.getElementById("area").value;
            const property_type = document.getElementById("property_type").value;
            const property_subtype = document.getElementById("property_subtype").value;

            const data = {
                title,
                owner,
                area,
                property_type,
                property_subtype
            };

            try {
                const response = await fetch("http://127.0.0.1:8000/api/create-property/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                });

                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById("message").innerText = "Property Created Successfully!";
                    document.getElementById("message").style.color = "green";
                    document.getElementById("propertyForm").reset(); // Reset form
                } else {
                    document.getElementById("message").innerText = "Error: " + JSON.stringify(result);
                    document.getElementById("message").style.color = "red";
                }

            } catch (error) {
                document.getElementById("message").innerText = "Error: " + error.message;
                document.getElementById("message").style.color = "red";
            }
        });

        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("propertyForm").addEventListener("submit", async function (event) {
                event.preventDefault();
        
                const formData = new FormData(this);
                const response = await fetch("http://127.0.0.1:8000/api/create-property/", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });
        
                const result = await response.json();
        
                const messageElement = document.getElementById("message");
                if (response.ok) {
                    messageElement.innerText = "Property Created Successfully!";
                    messageElement.style.color = "green";
                    this.reset();
                } else {
                    messageElement.innerText = "Error: " + JSON.stringify(result.errors);
                    messageElement.style.color = "red";
                }
            });
        });
        
