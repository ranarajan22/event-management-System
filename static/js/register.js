document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Collect form data
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        organization: document.getElementById('organization').value,
        jobTitle: document.getElementById('jobTitle').value,
        attendance: document.getElementById('attendance').value,
        registrationType: document.getElementById('registrationType').value,
        diet: document.getElementById('diet').value,
        comments: document.getElementById('comments').value,
    };

    // Show response message
    const responseMessage = document.getElementById('responseMessage');
    responseMessage.innerHTML = `<p>Thank you, ${formData.name}! Your registration has been submitted.</p>`;

    // Optionally, you could send this data to a server here
    console.log(formData); // For demonstration purposes
});
